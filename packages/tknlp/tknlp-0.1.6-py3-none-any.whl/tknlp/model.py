import numpy as np, functools
from functools import reduce
from fastNLP.embeddings.torch.utils import get_embeddings, get_sinusoid_encoding_table
from typing import List, Dict

import inspect
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils import rnn

def make_optim_helper(module, **lr_settings):
    # input: backbone.alpha
    all_param = {k: p for k,p in module.named_parameters() if p.requires_grad==True}
    lr_paramd = []
    for module_name, lr in lr_settings.items():
        params = [p for k,p in all_param.items() if k.startswith(module_name)]
        all_param = {k: v for k,v in all_param.items() if not k.startswith(module_name)}
        lr_paramd.append({'params': params, 'lr': lr, 'name': module_name})
    lr_paramd.append({'params': [p for k, p in all_param.items()], 'name': 'rest'})
    return lr_paramd

def make_optim(model, lr, optim_name='AdamW', add_lr={}, weight_decay=1e-2):
    if optim_name == 'Adam':
        optim = torch.optim.Adam
    elif optim_name == 'SGD':
        optim = functools.partial(torch.optim.SGD, momentum=0.9, weight_decay=0)
    elif optim_name == 'AdamW':
        optim = torch.optim.AdamW
    else:
        raise ValueError('optim not defined')
    # scheduler = torch.optim.lr_scheduler.StepLR(optim, step_size=30, gamma=0.1)
    return optim(make_optim_helper(model, **add_lr), lr=lr)

def get_pos_embed(embed_type, max_position, embed_dim):
    if embed_type == 'sin':
        return nn.Embedding.from_pretrained(
            get_sinusoid_encoding_table(max_position + 1, embed_dim, padding_idx=0),
            freeze=True) 
    elif embed_type == 'learned':
        return get_embeddings((max_position + 1, embed_dim), padding_idx=0)
    else:
        return None


def tween(lst, item, add_last=False):
    """
    >>> a, b = [1,2,3], ['#','$']
    >>> tween(a,b)
    [1, '#', '$', 2, '#', '$', 3]
    >>> tween(a,b,True)
    [1, '#', '$', 2, '#', '$', 3, '#', '$']
    """
    if not isinstance(item, list):
        item = [item]
    if add_last:
        return reduce(lambda r,v: r+[v]+item, lst, [])
    else:
        return reduce(lambda r,v: r+item+[v], lst[1:], lst[:1])

def build_args(func, **kwargs):
    spect = inspect.getfullargspec(func)
    if spect.varkw is not None: 
        return kwargs
    needed_args = set(spect.args)
    if spect.defaults is not None:
        defaults = [arg for arg in spect.defaults]
    else:
        defaults = []
    start_idx = len(spect.args) - len(defaults)
    output = {name: default for name, default in zip(spect.args[start_idx:], defaults)}
    output.update({name: val for name, val in kwargs.items() if name in needed_args})
    return output

def match_args(func, *args, **kwargs) -> dict:
    spect = inspect.signature(func)
    parameters = spect.parameters
    parameters = {
        k:v for k,v in spect.parameters.items() if k not in ('self', 'kwargs')
    }
    spect._parameters = parameters
    args = (*args, *kwargs.pop('args', ()))
    kwargs = {k: v for k,v in kwargs.items() if k in parameters}
    args = spect.bind_partial(*args, **kwargs)
    args.apply_defaults()
    return dict(args.arguments)

class xpack:

    def __init__(self, data, length, batch_first=True, enforce_sorted=False):
        if length.is_cuda: length = length.cpu()
        self.length = length
        self.data, self.batch_sizes, self.sorted_indices, self.unsorted_indices = rnn.pack_padded_sequence(data, length, batch_first=batch_first, enforce_sorted=enforce_sorted)
        self.extra = {}   # to help memorizing other stuff
    
    @property
    def sequence(self):
        return rnn.PackedSequence(
            data=self.data, batch_sizes=self.batch_sizes,
            sorted_indices=self.sorted_indices, unsorted_indices=self.unsorted_indices
        )
    
    def pad(self, data=None, batch_first=True, padding_value=0, total_length=None, **kwargs):
        if data is None: data = self.data
        if not isinstance(data, rnn.PackedSequence):
            batch_sizes = kwargs.get('batch_sizes', self.batch_sizes)
            sorted_indices = kwargs.get('sorted_indices', self.sorted_indices)
            unsorted_indices = kwargs.get('unsorted_indices', self.unsorted_indices)
            data = rnn.PackedSequence(
                data, batch_sizes, sorted_indices, unsorted_indices
            )
        rtn, _ = rnn.pad_packed_sequence(
            data, batch_first=batch_first, padding_value=padding_value, total_length=total_length
        )
        return rtn

    def pack(self, data, batch_first=True, enforce_sorted=False, return_sequence=False):
        seq =  rnn.pack_padded_sequence(data, self.length, batch_first=batch_first, enforce_sorted=enforce_sorted)
        return seq if return_sequence else seq.data

    def repeat(self, data):
        idx = torch.cat([self.sorted_indices[:i] for i in self.batch_sizes])
        if not isinstance(data, torch.Tensor):
            idx = idx.cpu().numpy()
        return data[idx]
    
    def np_pack(self, data):
        idx, size = self.sorted_indices.cpu().numpy(), self.batch_sizes.numpy()
        rtn = []
        for i, size in enumerate(self.batch_sizes):
            rtn.extend(data[idx[:size],i])
        return np.array(rtn)

class Model(nn.Module):

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        instance._init_params_d = match_args(instance.__init__, *args, **kwargs)
        return instance

    @property
    def init_parms_d(self):
        return self._init_params_d

    @classmethod
    def restore_from_checkpoint(cls, checkpoint):
        try:
            ckpt = torch.load(checkpoint)
            model = cls(**ckpt['init_params'])
            model.load_state_dict(ckpt['state_dict'], strict=False)
            return model
        except OSError: 
            pass # start training from scratch
    
    def save_to_checkpoint(self, ckpt_fp, **metadata):
        torch.save({
            'metadata': metadata,
            'state_dict': self.state_dict(),
            'init_params': self.init_parms_d
        }, ckpt_fp)

    def forward(self, **kwargs):
        """return output"""
        raise NotImplementedError
    
    def train_step(self, x, y):
        pred = self(x)
        return {"loss": self.loss_fn(pred, y)}

    def evaluate_step(self, x, y):
        pred = self(x)
        pred = torch.max(pred, dim=-1)[1]
        return {"pred": pred, "target": y}
    
    
def seq_len_to_mask(seq_len, max_len=None):
    """
    >>> size = torch.randint(3, 10, (3,)) # e.g., [3,6,6]
    >>> seq_len_to_mask(size).shape == torch.Size([3,size.max()])
    True
    >>> seq_len_to_mask(size, 10).shape   # True/False matrix
    torch.Size([3, 10])
    """
    if isinstance(seq_len, np.ndarray):
        assert len(np.shape(seq_len)) == 1, f"seq_len can only have one dimension, got {len(np.shape(seq_len))}."
        max_len = int(max_len) if max_len else int(seq_len.max())
        broad_cast_seq_len = np.tile(np.arange(max_len), (len(seq_len), 1))
        mask = broad_cast_seq_len < seq_len.reshape(-1, 1)

    elif isinstance(seq_len, torch.Tensor):
        assert seq_len.dim() == 1, f"seq_len can only have one dimension, got {seq_len.dim() == 1}."
        batch_size = seq_len.size(0)
        max_len = int(max_len) if max_len else seq_len.max().long()
        broad_cast_seq_len = torch.arange(max_len).expand(batch_size, -1).to(seq_len)
        mask = broad_cast_seq_len.lt(seq_len.unsqueeze(1))
        
    else:
        raise TypeError("Only support 1-d numpy.ndarray or 1-d torch.Tensor.")

    return mask

    
def xpad(arr, *shape, pad_value=0, dtype=float, rtn_type='numpy'):
    def helper(arr, *shape):
        if not shape: return 
        if len(shape) == 1: return np.array(arr, dtype=dtype)
        _arr = np.full(shape, fill_value=pad_value, dtype=dtype)
        for i, x in enumerate(arr):
            if isinstance(x, np.ndarray):
                size = min(shape[1], len(x))
                _arr[i, :size] = x[:size]
            else:
                rtn = helper(x, *shape[1:])
                _arr[i, :len(rtn)] = rtn
        return _arr
    if not shape:
        if hasattr(arr, 'shape'): shape = arr.shape
        else: shape = [len(arr)]
    out = helper(arr, *shape)
    if rtn_type == 'tensor':
        return torch.from_numpy(out)
    return out

def xmove(args, device):
    if not torch.cuda.is_available() or device is None:
        return
    if isinstance(args, list):
        for arg in args: xmove(arg, device)
    elif isinstance(args, dict):
        for key, value in args.items():
            if isinstance(value, torch.Tensor):
                args[key] = value.to(device)
    else:
        raise TypeError("only dictionary inputs are supported, please change your collate function")

def xgroup(iterable, ndigits=None):
    from collections import defaultdict
    def rd(num, digit=None):
        if digit: num = round(num, digit)
        return num
    out = defaultdict(dict)
    for key in iterable:
        if '|' in key:
            left,right = key.rsplit('|',1)
            out[right][left] = rd(iterable[key], ndigits)
            if '|' in left:
                out[right] = xgroup(out[right])
        else:
            out[key] = rd(iterable[key], ndigits)
    return out

class MyLoss(nn.Module):
    def __init__(self, samples_per_cls=[10,1], no_of_classes=2, loss_type='focal', re_weight=False):
        super(MyLoss, self).__init__()
        self.loss_type = loss_type
        beta, self.gamma = 0.9999, 2.0
        if re_weight:
            if not samples_per_cls:
                samples_per_cls = [1] * no_of_classes
            samples_per_cls = torch.tensor(samples_per_cls)
            effective_num = 1.0 - torch.pow(beta, samples_per_cls)
            weights = (1.0 - beta) / effective_num
            self.weights = nn.Parameter(weights.softmax(-1) * no_of_classes, requires_grad=False)
        else:
            self.weights = None
        self.n_cls = no_of_classes

    def forward(self, pred, target, seq_len=None, is_training=True):
        n = len(pred)
        # 1. prepare weight: weight_ (batch-size, n-class)
        if self.weights is not None:
            weight_ = self.weights.expand(n, self.n_cls)       
            weight_ = weight_[torch.arange(n), target]
            weight_ = weight_[:,None].repeat(1, self.n_cls)
        else:
            weight_ = None
        # 2. prepare inputs (label has to be fload!)
        target_ = F.one_hot(target, self.n_cls).float()
        loss_type, gamma = self.loss_type, self.gamma
        if loss_type == "focal":
            loss = focal_loss(target_, pred, weight_, gamma)
        elif loss_type == "sigmoid":
            loss = F.binary_cross_entropy_with_logits(pred,target_,weight_)
        elif loss_type == "softmax":
            pred = pred.softmax(dim = 1)
            loss = F.binary_cross_entropy(pred, target_, weight_)
        return loss



def focal_loss(labels, logits, alpha, gamma):
    """Compute the focal loss between `logits` and `labels`
    """    
    BCLoss = F.binary_cross_entropy_with_logits(logits, labels, reduction = "none")

    if gamma == 0.0:
        modulator = 1.0
    else:
        modulator = torch.exp(-gamma * labels * logits - gamma * torch.log(1 + 
            torch.exp(-1.0 * logits)))
             
    weighted_loss = alpha * modulator * BCLoss
    focal_loss = weighted_loss.sum()/labels.sum()
    return focal_loss


def f1_loss(y_true:torch.Tensor, y_pred:torch.Tensor, is_training=False, epsilon=1e-7) -> torch.Tensor:
    """Compute the f1 loss between `logits` and `labels`
    """
    if y_pred.ndim == 2: y_pred = y_pred.argmax(dim=1)
    tp = (y_true * y_pred).sum().to(torch.float32)
    fp = ((1 - y_true) * y_pred).sum().to(torch.float32)
    fn = (y_true * (1 - y_pred)).sum().to(torch.float32)
    precision = tp / (tp + fp + epsilon)
    recall = tp / (tp + fn + epsilon)
    f1 = 2* (precision*recall) / (precision + recall + epsilon)
    f1.requires_grad = is_training
    return f1

    
def make_fc(input_dim, hidden_sizes):
    r"""Returns a ModuleList of fully connected layers. 
    
    .. note::
    
        All submodules can be automatically tracked because it uses nn.ModuleList. One can
        use this function to generate parameters in :class:`BaseNetwork`. 
    
    Example::
    
        >>> make_fc(3, [4, 5, 6])
        ModuleList(
          (0): Linear(in_features=3, out_features=4, bias=True)
          (1): Linear(in_features=4, out_features=5, bias=True)
          (2): Linear(in_features=5, out_features=6, bias=True)
        )
    
    Args:
        input_dim (int): input dimension in the first fully connected layer. 
        hidden_sizes (list): a list of hidden sizes, each for one fully connected layer. 
    
    Returns:
        nn.ModuleList: A ModuleList of fully connected layers.     
    """
    assert isinstance(hidden_sizes, list), f'expected list, got {type(hidden_sizes)}'
    
    hidden_sizes = [input_dim] + hidden_sizes
    
    fc = []
    for in_features, out_features in zip(hidden_sizes[:-1], hidden_sizes[1:]):
        fc.append(nn.Linear(in_features=in_features, out_features=out_features))
    
    fc = nn.ModuleList(fc)
    
    return fc

def make_dnn(input_dim: int, hidden_sizes: List[int], hidden_units: List[str] = 'relu', dropouts: List[float] = 0.0, bias=True, init_weight=True, last_act=False):
    return DNN(
        input_dim, hidden_sizes, hidden_units, dropouts, bias, init_weight, last_act
    )

class DNN(nn.Sequential):
    def __init__(
        self, input_dim: int, hidden_sizes: List[int], hidden_units: List[str] = 'relu', dropouts: List[float] = 0.0,  bias=True, init_weight=True, last_act='identity'
    ):
        n = len(hidden_sizes)
        hidden_sizes = self.check_list(hidden_sizes, n)
        hidden_units = self.activate(*(
            self.check_list(hidden_units, n-1) + self.check_list(last_act)
        ))
        dropouts = self.check_list(dropouts, n)
        hidden_sizes = [input_dim] + hidden_sizes
        fc = []
        for i,(in_dim, out_dim) in enumerate(zip(hidden_sizes[:-1], hidden_sizes[1:])):
            try:
                act_unit = [hidden_units[i]]
            except IndexError:
                act_unit = []
            fc.extend([
                nn.Dropout(p=dropouts[i]),
                nn.Linear(
                    in_features=in_dim, out_features=out_dim, bias=bias
                )] + act_unit
            )
        super(DNN, self).__init__(*fc)
        if init_weight: self.apply(make_weight)

    @property
    def output_dim(self):
        return self[-2].out_features

    @staticmethod
    def activate(*units):
        def f(unit):
            if unit == 'relu': return nn.ReLU(True)
            elif unit == 'prelu': return nn.PReLU()
            elif unit == 'lrelu': return nn.LeakyReLU(0.2, True)
            elif unit == 'tanh': return nn.Tanh()
            elif unit == 'sigmoid': return nn.Sigmoid()
            elif unit == 'identity': return nn.Identity()
        return list(map(f, filter(None, units)))

    @staticmethod
    def check_list(x, n=1):
        if not isinstance(x, (tuple, list)):
            x = [x] * n
        return x[:n]
        

def clip_weight(layer, min_value=0.0, max_value=1.0):
    def func(m):
        cls = m.__class__.__name__
        if cls.find('Linear') != -1:
            with torch.no_grad():
                m.weight.clamp_(min_value, max_value)
    layer.apply(func)

def make_weight(m):
    cls = m.__class__.__name__
    if cls.find('Conv') != -1:
        nn.init.normal_(m.weight, 0.0, 0.02)
    elif cls.find('BatchNorm') != -1:
        nn.init.normal_(m.weight, 1.0, 0.02)
        if m.bias is not None: nn.init.zeros_(m.bias)
    elif cls.find('Linear') != -1:
        nn.init.kaiming_uniform_(m.weight, a=1)
        if m.bias is not None: nn.init.constant_(m.bias, 0)


def make_cnn(input_channel, channels, kernels, strides, paddings):
    r"""Returns a ModuleList of 2D convolution layers. 
    
    .. note::
    
        All submodules can be automatically tracked because it uses nn.ModuleList. One can
        use this function to generate parameters in :class:`BaseNetwork`. 
        
    Example::
    
        >>> make_cnn(input_channel=3, channels=[16, 32], kernels=[4, 3], strides=[2, 1], paddings=[1, 0])
        ModuleList(
          (0): Conv2d(3, 16, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1))
          (1): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1))
        )
    
    Args:
        input_channel (int): input channel in the first convolution layer. 
        channels (list): a list of channels, each for one convolution layer.
        kernels (list): a list of kernels, each for one convolution layer.
        strides (list): a list of strides, each for one convolution layer. 
        paddings (list): a list of paddings, each for one convolution layer. 
    
    Returns:
        nn.ModuleList: A ModuleList of 2D convolution layers.
    """
    N = len(channels)
    
    for item in [channels, kernels, strides, paddings]:
        assert isinstance(item, list), f'expected as list, got {type(item)}'
        assert len(item) == N, f'expected length {N}, got {len(item)}'
    
    channels = [input_channel] + channels
    
    cnn = []
    for i in range(N):
        cnn.append(nn.Conv2d(in_channels=channels[i], 
                             out_channels=channels[i+1], 
                             kernel_size=kernels[i], 
                             stride=strides[i], 
                             padding=paddings[i], 
                             dilation=1, 
                             groups=1))
    
    cnn = nn.ModuleList(cnn)
    
    return cnn


def make_transposed_cnn(input_channel, channels, kernels, strides, paddings, output_paddings):
    r"""Returns a ModuleList of 2D transposed convolution layers. 
    
    .. note::
    
        All submodules can be automatically tracked because it uses nn.ModuleList. One can
        use this function to generate parameters in :class:`BaseNetwork`. 
        
    Example::
    
        make_transposed_cnn(input_channel=3, 
                            channels=[16, 32], 
                            kernels=[4, 3], 
                            strides=[2, 1], 
                            paddings=[1, 0], 
                            output_paddings=[1, 0])
        ModuleList(
          (0): ConvTranspose2d(3, 16, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), output_padding=(1, 1))
          (1): ConvTranspose2d(16, 32, kernel_size=(3, 3), stride=(1, 1))
        )
    
    Args:
        input_channel (int): input channel in the first transposed convolution layer. 
        channels (list): a list of channels, each for one transposed convolution layer.
        kernels (list): a list of kernels, each for one transposed convolution layer.
        strides (list): a list of strides, each for one transposed convolution layer. 
        paddings (list): a list of paddings, each for one transposed convolution layer. 
        output_paddings (list): a list of output paddings, each for one transposed convolution layer. 
    
    Returns:
        nn.ModuleList: A ModuleList of 2D transposed convolution layers.
    """
    N = len(channels)
    
    for item in [channels, kernels, strides, paddings, output_paddings]:
        assert isinstance(item, list), f'expected as list, got {type(item)}'
        assert len(item) == N, f'expected length {N}, got {len(item)}'
    
    channels = [input_channel] + channels
    
    transposed_cnn = []
    for i in range(N):
        transposed_cnn.append(nn.ConvTranspose2d(in_channels=channels[i], 
                                                 out_channels=channels[i+1], 
                                                 kernel_size=kernels[i], 
                                                 stride=strides[i], 
                                                 padding=paddings[i], 
                                                 output_padding=output_paddings[i],
                                                 dilation=1, 
                                                 groups=1))
    
    transposed_cnn = nn.ModuleList(transposed_cnn)
    
    return transposed_cnn