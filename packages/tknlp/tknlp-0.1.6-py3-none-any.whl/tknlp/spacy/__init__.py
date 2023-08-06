"""
pipeline:
    trf_vectors:        obtain    
    ner_token_score
    ner_pos
"""
import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy.util import registry
from spacy.training import Example
from spacy.scorer import PRFScore
from . import depress 

import numpy as np
from functools import partial
from typing import Optional, Iterable, Dict, Set, List, Any, Callable, Tuple, Iterator
from collections import defaultdict

import torch

def install_extensions(ext:str) -> None:
    if not Doc.has_extension(ext):
        Doc.set_extension(ext, default=None)

@Language.factory(
    'trf_vectors',
)
class TrfContextualVectors:
    "reference: https://gist.github.com/yeus/a4d7cc6c97485597eb1e0d7fd720b4e3"
    def __init__(self, nlp: Language, name: str):
        self.name = name
        install_extensions('trf_token_vecs')
    def __call__(self, sdoc):
        install_extensions('trf_token_vecs')
        if isinstance(sdoc, str): sdoc = self._nlp(sdoc)
        # calculate groups for spacy token boundaries in the trf vectors
        vec_idx_splits = np.cumsum(sdoc._.trf_data.align.lengths)
        # get transformer vectors and reshape them into one large continous tensor
        trf_vecs = sdoc._.trf_data.tensors[0].reshape(-1, 768)
        # calculate mapping groups from spacy tokens to transformer vector indices
        vec_idxs = np.split(sdoc._.trf_data.align.dataXd, vec_idx_splits)
        # take sum of mapped transformer vector indices for spacy vectors (some token has more than one idx)
        vecs = np.stack([trf_vecs[idx].sum(0) for idx in vec_idxs[:-1]])
        sdoc._.trf_token_vecs = vecs
        sdoc.user_token_hooks["vector"] = self.vector
        sdoc.user_token_hooks["has_vector"] = self.has_vector
        return sdoc
    def vector(self, token):
        return token.doc._.trf_token_vecs[token.i]
    def has_vector(self, token):
        return True

@registry.augmenters("spacy.change_label.v1")
def create_different_label(name: str = None) -> Callable[["Language", Example], Iterator[Example]]:
    return partial(different_label, name=name)

def different_label(nlp: "Language", example: Example, *, name: str
) -> Iterator[Example]:
    if not name: yield example
    example_dict = example.to_dict()
    doc = nlp.make_doc(example.text)
    def f(x, *y): return '%s-%s'%(x,name) if y else x
    labels = [f(*e.split('-')) for e in example_dict['doc_annotation']['entities']]
    example_dict['doc_annotation']['entities'] = labels
    yield example.from_dict(doc, example_dict)

    
def ner_score(examples: Iterable[Example], **kwargs) -> Dict[str, Any]:
    """Compute micro-PRF and per-entity PRF scores for a sequence of examples."""
    score_per_type = defaultdict(PRFScore)
    def eq(pred, label): return torch.tensor([x==label for x in pred])
    def nq(pred, label): return torch.tensor([x!=label for x in pred])
    for eg in examples:
        if not eg.y.has_annotation("ENtorch.IOB"): continue
        target = [t.ent_type_ for t in map(eg.y.__getitem__, eg.alignment.x2y.dataXd)]
        pred   = [t.ent_type_ for t in eg.x]
        (target_symbol := set(target)).discard('')
        for label in target_symbol:
            score_per_type[label].tp += torch.sum(eq(pred, label).long().masked_fill(nq(target, label), 0)).item()
            score_per_type[label].fp += torch.sum(eq(pred,label).long().masked_fill(eq(target, label), 0)).item()
            score_per_type[label].fn += torch.sum(nq(pred, label).long().masked_fill(nq(target, label), 0)).item()
    totals = PRFScore()
    for prf in score_per_type.values():
        totals += prf
    if len(totals) > 0:
        return {
            "ents_p": totals.precision,
            "ents_r": totals.recall,
            "ents_f": totals.fscore,
            "ents_per_type": {k: v.to_dict() for k, v in score_per_type.items()},
        }
    else:
        return {
            "precision": None,
            "recall": None,
            "f1": None,
            "ents_per_type": None,
        }


@registry.scorers("spacy.ner_token_score.v1")
def make_ner_scorer():
    return ner_score


