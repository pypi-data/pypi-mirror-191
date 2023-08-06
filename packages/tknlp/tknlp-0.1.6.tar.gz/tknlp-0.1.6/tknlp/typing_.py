from typing import List, Union, Literal, Optional, Tuple, Callable, Dict, Any, Iterable, Mapping, Generator, overload, TypeVar
from pathlib import Path
from abc import ABC
from dataclasses import dataclass
from collections import Counter, defaultdict
from os import PathLike

class CanItemDataType(ABC):
    @classmethod
    def __subclasshook__(cls, subclass: Any) -> Union[bool, Any]:
        if cls is CanItemDataType:
            item = getattr(subclass, 'item', None)
            return callable(item)
        return NotImplemented
    

_T = TypeVar("_T")

IntList = List[int] # A list of token_ids
StrList = List[str] # A list of string

@dataclass
class NerSample:
    input_ids: IntList
    attention_masks: IntList
    labels: IntList
    words: StrList
