import os
import sys
import hashlib
import torch
import numpy as np
import random

from datetime import timedelta, datetime
from time import perf_counter
from contextlib import contextmanager
from functools import reduce, wraps
from colorama import Fore, Style
from itertools import zip_longest, groupby

from .typing_ import (
    Mapping, Dict, Callable, Union, Path, Generator, defaultdict, Iterable, List, Any
)
from .model import seq_len_to_mask


# -------------------------- General Utility Function ----------------------------------
# seed_all: fix random seet to make experiment replicable
# one_time: set a timer to make sure function is run only one time
# encodes: turn long string into shortened sha256 hexdigits 
# timeit: return running time of callbed function
# color_str: style a string with color

# -------------------------- Xtools on Data Structure ----------------------------------
# flatten_dict: flatten a nested dictionary
# filter_empty: filter out entries in list with rules and indices
# xrank: retrieve {topk} {mode: max/min} element in {dim}, with max {seq_len} on each {dim}
# xlen: infer the shape of a nested list after padding
# xpad: pad array {arr} into a predetermined shape, with {pad_value}
# xmove: move all data in {args} to {device}

# -------------------------- O/I Related Function --------------------------------------
# get_dir: get execute directory of main program
# set_directory: set working directory
# find_dotenv: find .env file recursively from current to root
# ojoin: take a list of dir-name and concatenate them to make a path 
# omake: create directory for each input arguments
# oexits: do all input paths exist, return False if any input argument isn't a path
# opath: return absolute path
# oreplace: replace filename only in the same directory
# owalk: walk through a directory
# CloudpickleWrapper: serialize/picklize contents


def seed_all(seed: int) -> None:
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    generator = torch.Generator()
    generator.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    
def one_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if not wrapper.has_been_run:
            wrapper.has_been_run = True
            return func(*args, **kwargs)
    wrapper.has_been_run = False
    return wrapper

def find_dotenv(path_name: str='', file_name: str='.env') -> Union[None, Path]:
    """find .env in current and all its parent"""
    path = path_name or get_dir(); path = Path(path).absolute()
    while path.as_posix() != path.root:
        attempt = path/file_name
        if attempt.exists(): return attempt
        path = path.parent
    return None

def get_dir() -> Path:
    if check_in_ipython():
        return os.getcwd()
    return odir(sys.argv[0])

@contextmanager
def set_directory(path = None, start_from_home = False):
    if not path: path = get_dir()
    elif start_from_home: path = Path.home()/path
    origin = Path().absolute()
    try: 
        os.chdir(path); yield
    finally:
        os.chdir(origin)

def check_in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def odir(path, has_extension=True):
    _root, _ext = os.path.splitext(path)
    if has_extension and _ext != '':
        _root = os.path.dirname(_root)
    return _root

def find_dotenv(path_name='', file_name='.env'):
    """find .env in current and all its parent"""
    path = path_name or get_dir(); path = Path(path).absolute()
    while path.as_posix() != path.root:
        attempt = path/file_name
        if attempt.exists(): return attempt
        path = path.parent
    return None

def get_dir():
    """get execute directory of main program """
    if check_in_ipython():
        return os.getcwd()
    return odir(sys.argv[0])

def _flatten_dict(dct, prefix=''):
    if isinstance(dct, (Mapping, Dict)):
        if prefix: prefix += '.'
        for k, v in dct.items():
            yield from _flatten_dict(v, prefix+str(k))
    else:
        yield prefix, dct
    
def flatten_dict(dct: Dict, rtn_dct=True) -> Generator:
    if rtn_dct:
        return dict(_flatten_dict(dct))
    else:
        return _flatten_dict(dct)

def filter_empty(*lst, empty=None, remove_index=[]):
    idx, rtn = zip(*filter(lambda c: c[1] != empty and c[0] not in remove_index, enumerate(lst[0])))
    rtn_lst = [list(rtn)]
    for l in lst[1:]: rtn_lst.append([l[i] for i in idx])
    return rtn_lst

def ojoin(*args, create_if_not_exist=False) -> Path:
    path = os.path.join(*args)
    if create_if_not_exist: 
        omake(path)
    return path

def oreplace(path, toreplace: str, create_if_not_exist=False):
    parent = odir(path)
    return ojoin(parent, toreplace, create_if_not_exist=create_if_not_exist)

def owalk(*args, limit=-1, ext=None, start=None):
    for path in args:
        for name in sorted(os.listdir(path)):
            if ext and not name.endswith(ext): continue
            if start and not name.startswith(start): continue
            yield path, name
            if limit > 0: limit -= 1
            if limit == 0: break 
        else: continue  # only execute if inner loop not break
        break

def omake(*args, **kwargs):
    def omake_helper(path):
        dir = odir(path)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
    args and [omake_helper(p) for p in args]
    kwargs and [omake_helper(p) for k,p in kwargs.items()]

def oexists(*path, **paths) -> bool:
    def check_exist(path):
        return os.path.exists(path)
    if path and not all(check_exist(p) for p in path):
        return False
    if paths and not all(check_exist(p) for k,p in paths.items()):
        return False
    return True

def opath(path):
    return os.path.abspath(path)    

def obase(path):
    filename, file_extension =os.path.splitext(os.path.basename(path))
    return filename

def encodes(long_str):
    "encode a long string in a consistent and determiistic manner"
    return hashlib.sha256(long_str.encode()).hexdigest()


class CloudpickleWrapper(object):
    r"""Uses cloudpickle to serialize contents (multiprocessing uses pickle by default)
    
    This is useful when passing lambda definition through Process arguments.
    """
    def __init__(self, x):
        self.x = x
        
    def __call__(self, *args, **kwargs):
        return self.x(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(self.x, name)
    
    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)
    
    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)
        
def timeit(_func=None, *, color='green', bold=False):
    def decorator_timeit(f):
        r"""Print the runtime of the decorated function. """
        @wraps(f)
        def wrapper_timeit(*args, **kwargs):
            t = perf_counter()
            out = f(*args, **kwargs)
            total_time = timedelta(seconds=round(perf_counter() - t))
            timestamp = datetime.now().isoformat(' ', 'seconds')
            print(color_str(string=f'\nTotal time: {total_time} at {timestamp}', color=color, bold=bold))
            return out
        return wrapper_timeit
    if _func is None:
        return decorator_timeit
    else:
        return decorator_timeit(_func)

def color_str(string, color='cyan', bold=True):
    if isinstance(string, Path): string = string.as_posix()
    elif isinstance(string, (float, int)): string = str(string)
    colors = {'red': Fore.RED, 'green': Fore.GREEN, 'blue': Fore.BLUE, 'cyan': Fore.CYAN, 
              'magenta': Fore.MAGENTA, 'black': Fore.BLACK, 'white': Fore.WHITE}
    style = colors[color]
    if bold:
        style += Style.BRIGHT
    out = style + string + Style.RESET_ALL
    return out

def xrank(tensor, dim=0, topk=0, mode='max', pad=0., seq_len=None):
    if mode == 'max':
        try:
            attn, idx = tensor.max(dim=dim)
        except IndexError:
            pass
        largest, invalid =True, float('-inf')
    else:
        attn, idx = tensor.min(dim=dim)
        largest, invalid =False, float('inf')
    if topk <= 0 or attn.size(-1) <= topk: 
        return attn, idx
    if seq_len is not None:
        mask = seq_len_to_mask(seq_len) 
        attn.masked_fill_(~mask, invalid)
    else:
        mask = torch.ones_like(attn).bool()
    _, i = attn.topk(topk, largest=largest, dim=-1)
    attn.masked_fill_(mask.scatter(-1,i,False), pad)
    return attn, i

def xtable(
    dicts: List[Dict], 
    keys: List[str] = None, 
    pads: List[str] = None, 
    fcodes: List[str] = None, 
    convert_headers: Dict[str, Callable] = None, 
    header_names: List[str] = None, 
    skip_none_lines: bool = False, 
    skip_head_lines: bool = False,
    replace_values: Dict[str, Any] = None, index: List[str] = None
):
    """ Generate ascii table from dictionary
        Copyright: https://stackoverflow.com/questions/40056747/print-a-list-of-dictionaries-in-table-form
    dicts: input dictionary list; empty lists make keys OR header_names mandatory
    keys: order list of keys to generate columns for; no key/dict-key should suffix with '____' else adjust code-suffix
    pads: indicate padding direction and size, eg <10 to right pad alias left-align
    fcodes: formating codes for respective column type, eg .3f
    convert_headers: apply converters(dict) on column keys k, eg timestamps
    header_names: supply for custom column headers instead of keys
    skip_none_lines: skip line if contains None
    replace_values: specify per column keys k a map from seen value to new value;
                    new value must comply with the columns fcode; CAUTION: modifies input (due speed)
    """
    # optional arg prelude
    def infer_type(v):
        if isinstance(v, float): return ('.4f', '>8') 
        elif isinstance(v, int): return ('d', '>6')
        else: return ('s', '<8')
    if index is not None:
        dicts = [{'index': y, **x} for x,y in zip(dicts, index)]
    if keys is None:
        if len(dicts) > 0:
            keys = dicts[0].keys()
        elif header_names is not None:
            keys = header_names
        else:
            raise ValueError('keys or header_names mandatory on empty input list')
    if pads is None  and fcodes is None:
        fcodes, pads = zip(*map(infer_type, dicts[0].values()))
    N_keys, N_pads, N_codes = len(keys), len(pads), len(fcodes)
    if N_pads != N_keys:
        raise ValueError(f'bad pad length {len(pads)}, expected: {N_keys}')
    elif N_codes != N_keys:
        raise ValueError(f'bad fcodes length {len(fcodes)}, expected: {N_keys}')
    if convert_headers is None: convert_headers = {}
    if header_names is None: header_names = keys
    if replace_values is None: replace_values = {}
    # build header
    headline = '│'.join(f"{v:{pad}}" for v, pad in zip_longest(header_names, pads))
    underline = '─' * len(headline)
    # suffix special keys to apply converters to later on
    marked_keys = [h + '____' if h in convert_headers else h for h in keys]
    marked_values = {}
    s = '│'.join(f"{{{h}:{pad}{fcode}}}" for h, pad, fcode in zip_longest(marked_keys, pads, fcodes))
    if skip_head_lines:
        lines = []
    else:
        lines = [headline, underline, ]
    for d in dicts:
        none_keys = [k for k, v in d.items() if v is None]
        if skip_none_lines and none_keys:
            continue
        elif replace_values:
            for k in d.keys():
                if k in replace_values and d[k] in replace_values[k]:
                    d[k] = replace_values[k][d[k]]
                if d[k] is None:
                    raise ValueError(f"bad or no mapping for key '{k}' is None. Use skip or change replace mapping.")
        elif none_keys:
            raise ValueError(f'keys {none_keys} are None in {d}. Do skip or use replace mapping.')
        for h in convert_headers:
            if h in keys:
                converter = convert_headers[h]
                marked_values[h + '____'] = converter(d)
        line = s.format(**d, **marked_values)
        lines.append(line)
    return '\n'.join(lines)

def _isnested(arr):
    """whether `arr` is nested iterable object
    >>> _isnested([1,2,3]) #should be False
    """
    try:
        return any(len(x) > 1 for x in arr)
    except TypeError:
        return False
    
def xlen(arr):
    """infer shape of nested list
    >>> lst = [[1,], [2,3], [2]]
    >>> xlen(lst) # [3,2]
    """
    if isinstance(arr, str) or not isinstance(arr, Iterable) or not _isnested(arr):
        return len(arr)
    carr = [xlen(x) for x in arr]    
    if not _isnested(carr):
        return [len(arr), max(carr)]
    else:
        return [len(arr)] + list(map(max, zip_longest(*carr, fillvalue=0)))

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
        else: 
            shape = xlen(arr)
    out = helper(arr, *shape)
    if rtn_type == 'tensor':
        return torch.from_numpy(out)
    return out

def xmove(args, device):
    if not torch.cuda.is_available() or device is None:
        return
    if isinstance(args, list):
        for arg in args: xmove(arg, device)
    elif isinstance(args, Mapping):
        for key, value in args.items():
            if isinstance(value, torch.Tensor):
                args[key] = value.to(device)
    else:
        raise TypeError("only dictionary inputs are supported, please change your collate function")

def xgroup(iterable: Iterable, ndigits=None) -> Dict:
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

def import_file(fpath: str, fkey: str, identifier = '='*5):
    flag = False
    codes = ""
    with open(fpath, 'r') as f:
        for key, group in groupby(f,lambda line: line.startswith(identifier)):
            line = list(group)
            if key and fkey in line[0]:
                flag = True
            elif key and fkey not in line[0]:
                flag = False
            elif flag:
                codes += ''.join(line)
    return codes

    
