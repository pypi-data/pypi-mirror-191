import sys
import csv
import numpy as np
from dataclasses import dataclass
from torch.utils.data import Dataset, DataLoader
from torch import Tensor, tensor
import torch.nn.functional as F
from typing import Generator, Optional

from fastNLP.core.dataloaders import MixDataLoader, utils
from fastNLP.core.metrics import Metric, ClassifyFPreRecMetric
from torchmetrics.classification.auroc import BinaryAUROC
from torchmetrics import Metric
from typing import Callable
from collections import Counter

csv.field_size_limit(sys.maxsize)


class Concat(MixDataLoader):

    def __init__(self, **dl):
        ds, collate_fn = {}, {}
        for name, loader in dl.items():
            ds[name] = loader.dataset
            collate_fn[name] = collate_helper(loader._get_collator())
        super(Concat, self).__init__(datasets=ds, mode='sequential', collate_fn=collate_fn, batch_size=loader.batch_size, drop_last=loader.drop_last)
    
    
def collate_helper(collate_fn: Callable):
    def collate_batch(batch):
        idx, rtn = utils.indice_collate_wrapper(collate_fn)(batch)
        return rtn
    return collate_batch


class Data:
    keys = ['train', 'val', 'test', 'aug']
    def apply(self, func, **data):
        for mode, old_data in data.items():
            assert mode in self.keys, "%s must be one of %s"%(mode, self.keys)
            new_data = func(old_data or getattr(self, mode))
            if isinstance(new_data, Generator):
                setattr(self, mode, list(zip(*new_data)))
            else:
                setattr(self, mode, new_data)
    def __iter__(self):
        for mode in self.keys: 
            yield getattr(self, mode)
            
@dataclass
class Datasets(Data):
    """Class for keeping track of datasets"""
    train: Optional[Dataset] = None
    test: Optional[Dataset] = None
    val: Optional[Dataset] = None
    aug: Optional[Dataset] = None

@dataclass
class Dataloaders(Data):
    """Class for keeping track of dataloaders"""
    train: DataLoader
    test: DataLoader 
    val: Optional[DataLoader] = None
    aug: Optional[Dataset] = None

class ClassifyMetric(ClassifyFPreRecMetric):

    def __init__(self, only_gross=True, f_type='macro', beta=1, verbose=True, num_class=2, aggregate_when_get_metric=None, **kwargs):
        """
        Args
        ----
        @verbose                control whether including tp/fp/tn/fn
        """
        assert num_class == 2, "It works in two-class classification problem only !!!"
        super(ClassifyMetric, self).__init__(only_gross=only_gross, f_type=f_type, beta=beta, aggregate_when_get_metric=aggregate_when_get_metric)
        self.verbose = verbose

    def get_metric(self) -> dict: 
        result = super(ClassifyMetric, self).get_metric()
        tps, fps = zip(*self.all_gather_object([self._tp, self._fp]))
        tps, fps = sum(tps, Counter()), sum(fps, Counter())
        if self.verbose:
            result.update(
                tp=tps[1], fn=fps[0], fp=fps[1], tn=tps[0], 
                # binary=2*tps[1]/(2*tps[1] + fps[0] + fps[1])
            )
        return result


class ClassifyAUC(BinaryAUROC):

    def update(self, pred: Tensor, target: Tensor) -> None:  # type: ignore
        super(ClassifyAUC, self).update(pred, target)

    def compute(self): # convert tensor to number
        result = super(ClassifyAUC, self).compute()
        return {'auc': result.item()}


class ClassifyFunc(Metric):
    is_differentiable: bool = True
    higher_is_better: bool = False
    full_state_update: bool = False
    sum_measure: Tensor
    total_count: Tensor
    def __init__(self, func: Callable, name: str = '', **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.name = name or 'measure'
        self.add_state("sum_measure", default=tensor(0.0), dist_reduce_fx="sum")
        self.add_state("total_count", default=tensor(0), dist_reduce_fx="sum")
    
    def update(self, pred: Tensor, target: Tensor) -> None:  # type: ignore
        n = len(target)
        self.sum_measure += self.func(pred.float(), target.float()) * n
        self.total_count += n

    def compute(self) -> Tensor:
        return {self.name: (self.sum_measure / self.total_count).item()}

        
class CrossEntropy(Metric):
    """Torchmetrics cross entropy loss implementation.
    This class implements cross entropy loss as a :class:`torchmetrics.Metric` so that it can be returned by the
    :meth:`~.ComposerModel.metrics`.
    Args:
        ignore_index (int, optional): Specifies a target value that is ignored
            and does not contribute to the input gradient. ``ignore_index`` is only applicable when the target
            contains class indices. Default: ``-100``.
        dist_sync_on_step (bool, optional): sync distributed metrics every step. Default: ``False``.
    """
    full_state_update = False

    def __init__(self, name: str = '', ignore_index: int = -100, aggregate_when_get_metric: bool = False, loss_type='sigmoid'):
        super().__init__(dist_sync_on_step=aggregate_when_get_metric)
        self.ignore_index = ignore_index
        self.name = name or 'loss'
        self.loss_type = loss_type
        self.add_state('sum_loss', default=tensor(0.), dist_reduce_fx='sum')
        self.add_state('total_batches', default=tensor(0), dist_reduce_fx='sum')

    def update(self, logit: Tensor, target: Tensor) -> None:
        """Update the state with new predictions and targets."""
        # Loss calculated over samples/batch, accumulate loss over all batches
        target_ = F.one_hot(target, 2).float()
        if self.loss_type == 'sigmoid':
            self.sum_loss += F.cross_entropy(logit, target, ignore_index=self.ignore_index)
        elif self.loss_type == 'softmax':
            prob = logit.softmax(dim = 1)
            self.sum_loss += F.binary_cross_entropy(prob, target_)
        assert isinstance(self.total_batches, Tensor)
        self.total_batches += 1

    def compute(self) -> Tensor:
        """Aggregate state over all processes and compute the metric."""
        # Return average loss over entire validation dataset
        assert isinstance(self.total_batches, Tensor)
        assert isinstance(self.sum_loss, Tensor)
        return {self.name: (self.sum_loss / self.total_batches).item()}