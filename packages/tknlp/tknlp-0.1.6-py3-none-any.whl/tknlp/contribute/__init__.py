from pathlib import Path
from operator import itemgetter, attrgetter
from collections import OrderedDict
from tqdm import tqdm
from ..utils import oexists, omake, color_str
from ..typing_ import Mapping, List
from .mongo import MongoDB

import cloudpickle
import pickle
import yaml
import os
import logging
import numpy as np 
import pandas as pd

os.environ['ANSI_COLORS_DISABLED'] = "True"
from wasabi import Printer

def get_pbar(size: int, title: str = ''):
    pbar = tqdm(total=size)
    pbar.set_description(title)
    return lambda *args: pbar.update()

def get_num_gpu():
    with os.popen('nvidia-smi --list-gpus | wc -l') as proc:
        output = proc.read()
    return int(output)

def is_cur_env_distributed():
    return "FASTNLP_GLOBAL_RANK" in os.environ

class Logger:
    _name,_path,_logger = None, None, {}

    @staticmethod
    def get(**kwargs):
        return get_logger(name=kwargs.pop('name', Logger._name), **kwargs)

    @staticmethod
    def clear():
        Logger._name = None

    def __init__(self, name=None, message_only=True, formatter=None, level='INFO', path=''):
        self.log = get_logger(name, message_only, formatter, level, path)
        if is_cur_env_distributed() and os.getenv('FASTNLP_GLOBAL_RANK') != '0':
            self.log.setLevel(logging.ERROR)
            print("Experiment logging is saved in %s"%(color_str(path)))
        else:
            print("Experiment logging is saved in %s"%(color_str(path)))
        Logger._name = name
        Logger._path = path
        Logger.get(name='fastNLP').setLevel('WARNING')

    def info(self, msg, *args, **kwargs):
        self.log.info( msg, *args, **kwargs)

def get_logger(name=None, message_only=True, formatter=None, level='INFO', path=''):
    loggers = Logger._logger
    if name in loggers: return loggers.get(name)
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging._nameToLevel[level])
    if message_only:
        if formatter is not None:
            formatter = logging.Formatter(formatter)
        else:
            formatter = logging.Formatter('%(name)s :: %(asctime)s ::  %(message)s', "%H:%M")
        if path:
            log = logging.FileHandler(path,mode='w')
        else:
            log = logging.StreamHandler()
        log.setFormatter(formatter)
        logger.addHandler(log)
        # propagate=False: disable message spawned by child logger pass to parent logger
        logger.propagate = False        
        loggers[name] = logger
    return logger

log = Logger.get()

class Recorder:
    r"""Log the information in a dictionary. 
    
    If a key is logged more than once, then the new value will be appended to a list. 
    
    .. note::
    
        It uses pickle to serialize the data. Empirically, ``pickle`` is 2x faster than ``numpy.save``
        and other alternatives like ``yaml`` is too slow and ``JSON`` does not support numpy array. 
    
    .. warning::
    
        It is discouraged to store hierarchical structure, e.g. list of dict of list of ndarray.
        Because pickling such complex and large data structure is extremely slow. Put dictionary
        only at the topmost level. Large numpy array should be saved separately. 
    
    Example:
    
    * Default::
    
        >>> logger = Recorder()
        >>> logger('iteration', 1)
        >>> logger('train_loss', 0.12)
        >>> logger('iteration', 2)
        >>> logger('train_loss', 0.11)
        >>> logger('iteration', 3)
        >>> logger('train_loss', 0.09)
        
        >>> logger
        OrderedDict([('iteration', [1, 2, 3]), ('train_loss', [0.12, 0.11, 0.09])])
        
        >>> if i == 0 or (i+1) % self.config.log_freq == 0:
        >>>     logger.dump(keys=None, index=-1, indent=0, border='-'*50)
        Iteration: [1, 2, 3]
        Train Loss: [0.12, 0.11, 0.09]
        
    * With indentation::
    
        >>> logger.dump(indent=1)
            Iteration: [1, 2, 3]
            Train Loss: [0.12, 0.11, 0.09]
        
    * With specific keys::
    
        >>> logger.dump(keys=['iteration'])
        Iteration: [1, 2, 3]
        
    * With specific index::
    
        >>> logger.dump(index=0)
        Iteration: 1
        Train Loss: 0.12
        
    * With specific list of indices::
    
        >>> logger.dump(index=[0, 2])
        Iteration: [1, 3]
        Train Loss: [0.12, 0.09]
    
    """
    def __init__(self):
        # TODO: wait for popularity of Python 3.7 which dict preserves the order, then drop OrderedDict()
        self.logs = OrderedDict()

    def average(self, key=None):
        if key: 
            return np.mean(self.logs[key])
        else:
            for key in self.logs:
                self.logs[key] = [self.average(key)]

    @property
    def KEYS(self):
        # return set(x.split('_')[-1] for x in self.logs.keys() if x != 'epoch')
        return set(x for x in self.logs.keys() if x != 'epoch')

    def __iter__(self):
        for key in self.KEYS:
            yield key, self.logs[key]
        
    def __call__(self, key, value):
        r"""Log the information with given key and value. 
        
        .. note::
        
            The key should be semantic and each word is separated by ``_``. 
        
        Args:
            key (str): key of the information
            value (object): value to be logged
        """
        if key not in self.logs:
            self.logs[key] = []
        
        self.logs[key].append(value)

    def __getitem__(self, key):
        return self.logs[key]
        
    def dump(self, keys=None, index=None, indent=0, border=''):
        r"""Dump the loggings to the screen.
        
        Args:
            keys (list, optional): a list of selected keys. If ``None``, then use all keys. Default: ``None``
            index (int/list, optional): the index of logged values. It has following use cases:
                
                - ``scalar``: a specific index. If ``-1``, then use last element.
                - ``list``: a list of indicies. 
                - ``None``: all indicies.
                
            indent (int, optional): the number of tab indentation. Default: ``0``
            border (str, optional): the string to print as header and footer
        """
        if keys is None:
            keys = list(self.logs.keys())
        assert isinstance(keys, list), f'expected list, got {type(keys)}'
        
        if index is None:
            index = 'all'
        
        print(border)
        for key in keys:
            if indent > 0:
                print('\t'*indent, end='')  # do not create a new line
            
            if index == 'all':
                value = self.logs[key]
            elif isinstance(index, int):
                value = self.logs[key][index]
            elif isinstance(index, list):
                value = list(itemgetter(*index)(self.logs[key]))
            
            # Polish key string
            key = key.strip().replace('_', ' ').title()
            
            print(f'{key}: {value}')
        print(border)

    def save(self, f):
        r"""Save loggings to a file. 
        
        Args:
            f (str): file path
        """
        with open(f, 'wb') as file:
            if f.endswith('pkl'):
                pickle.dump(self.logs, file)
            elif f.endswith('csv'):
                pd.DataFrame.from_dict(self.logs).to_csv(f, index=False)
            else:
                print(self.logs, file=file)
        
    def clear(self):
        r"""Remove all loggings in the dictionary. """
        self.logs.clear()
        
    def __repr__(self):
        return repr(self.logs)

    def __str__(self):
        return ','.join(set(x.split('_')[-1] for x in self.logs.keys()))

def pickle_load(f, ext='.pkl', encode="ASCII"):
    r"""Read a pickled data from a file. 
    """
    if not f: raise FileNotFoundError()
    if isinstance(f, Path):
        f = f.as_posix() 
        f += [ext,''][f[-4:]==ext]

    with open(f, 'rb') as file:
        return cloudpickle.load(file, encoding=encode)

def pickle_loads(*f):
    for sf in f: 
        yield pickle_load(sf)

def pickle_dump(obj, f, ext='.pkl'):
    r"""Serialize an object using pickling and save in a file. 
    
    Args:
        obj (object): a serializable object
        f (str/Path): file path
        ext (str, optional): file extension. Default: .pkl
    """
    if isinstance(f, Path):
        f = f.as_posix()
        f += [ext,''][f[-4:]==ext]
    
    with open(f, 'wb') as file:
        return cloudpickle.dump(obj=obj, file=file, protocol=pickle.HIGHEST_PROTOCOL)


def yaml_load(f):
    r"""Read the data from a YAML file. 
    """
    if isinstance(f, Path):
        f = f.as_posix()
    
    with open(f, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def yaml_dump(obj, f, ext='.yml'):
    r"""Serialize a Python object using YAML and save in a file. 
    
    Args:
        obj (object): a serializable object
        f (str/Path): file path
        ext (str, optional): file extension. Default: .yml
        
    """
    if isinstance(f, Path):
        f = f.as_posix()
    with open(f+ext, 'w') as file:
        return yaml.dump(obj, file, sort_keys=False)

def cache_results( _refresh=False, **_cache_fp):
    r""" a decorator to cache function results
    @reference: FastNLP::core::utils
    :param str `_cache_fp`:     where to read the cache from
    :param bool `_refresh`:     whether to regenerate cache
    """
    def wrapper_(func):
        def wrapper(*args, **kwargs):
            refresh = kwargs.pop('_refresh', _refresh)
            cache_fp = kwargs.pop('_cache_fp', _cache_fp)
            if kwargs.pop('_skipit', False):
                return func(*args, **kwargs)
            assert isinstance(cache_fp, dict), "_cache_fp must be a dict data structure"
            cond = cache_fp and not refresh and oexists(**cache_fp)
            if not cond:
                omake(**cache_fp)
                results = func(*args, **kwargs)
                if not results:
                    raise RuntimeError("The return value is None. Delete the decorator.")
                for name, data in results.items():
                    pickle_dump(data, cache_fp.get(name))
            else:
                for _,fp in cache_fp.items(): 
                    log.info(f'read cache from {color_str(fp)}')
            for _, fp in cache_fp.items():
                yield pickle_load(fp)
        return wrapper
    return wrapper_


class FileLog:
    def __init__(self, path, overwrite=False):
        self.path = path
        self.msg = Printer(no_print=True, pretty=True)
        overwrite and open(path, 'w').close()
    def __call__(self, msg, mode='a'):
        with open(self.path, mode) as f:
            print(msg, file=f)
    def divider(self, msg, **kwargs):
        text = self.msg.divider(msg, **kwargs)
        self(text[4:-4])
    def seperate(self):
        self('-'*self.msg.line_max)
    def table(self, data, header=None, divider=True, **kwargs):
        self(self.msg.table(
            data=data, header=header, divider=divider, **kwargs
        )[1:-1])