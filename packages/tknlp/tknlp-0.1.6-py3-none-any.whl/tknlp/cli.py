import argparse
import re
import sys
from operator import attrgetter, itemgetter
from pprint import pformat
from copy import deepcopy
from .typing_ import Mapping, Any, Callable, Dict, Path
from .utils import flatten_dict

def search_api(key, obj):
    if key in obj: return obj.get(key)
    for nested in filter(lambda _: isinstance(_, (Args, Dict)), obj.values()):
        if (y := search_api(key, nested)) is not None:
            return y
    return None

def to_dict(args):
    rtn_dict = {}
    for k, v in args.items():
        if isinstance(v, Path):
            rtn_dict[k] = str(v)
        elif isinstance(v, Args):
            rtn_dict[k] = to_dict(v)
        rtn_dict[k] = v
    return rtn_dict


class Args(Mapping):

    def __init__(self, level=1, **kwargs):
        for key, value in kwargs.items():
            self.set(key, self.init_helper(value, level=level))
        if kwargs.pop('_post_init_', False):
            self.post_init()

    def to_string(self):
        return '_'.join([f'{k}={v}' for k,v in sorted(self.items())])
    
    @classmethod
    def init_helper(cls, value, level=1):
        if level > 1 and isinstance(value, (Dict, cls)):
            value = cls(level=level-1, **value)
        return value

    def search(self, key): #recursively find key in obj
        return search_api(key, self)

    def set(self, __name, __value):
        key, *subkey = __name.split('.', 1)
        if not subkey:
            setattr(self, key, __value)
        else:
            rtn_value = self.pop(key, Args())
            rtn_value.set(subkey[0], __value)
            setattr(self, key, rtn_value)

    def update(self, override=True, **kwargs):
        for k,v in kwargs.items(): 
            if not override and k in self:
                continue
            self.set(k, v)
        
    def pop(self,__name, __default=None) -> Any:
        return self.__dict__.pop(__name, __default)
    
    def pops(self, *__names, input_mappings={}):
        return {input_mappings.get(n, n): self.pop(n) for n in __names}

    def copy(self):
        return deepcopy(self)

    def __add__(self, other):
        return Args(**self, **other)

    def __contains__(self, item): return hasattr(self, item)
    
    def __iter__(self): yield from self.__dict__

    def get(self, item, *default): 
        if default: return getattr(self, item, default[0])
        else: return getattr(self, item)
    
    def __getitem__(self, item): return getattr(self, item)
    
    def __setitem__(self, item, value): setattr(self, item, value)

    def __len__(self): return len(self.__dict__)

    def post_init(self):
        parser = argparse.ArgumentParser()
        def f(args, prefix=''):
            flag = False
            for k,v in args.items():
                prefix_k = prefix + '.' + k
                if isinstance(v, (Args, dict)): f(v, prefix_k)
                elif v is None or v == 'None': args[k] = None
                elif isinstance(v, str) and v.startswith('$'):
                    if v.startswith('$$'): args[k] = v[1:]
                    else: args[k] = attrgetter(v.lstrip('$'))(self)
                elif isinstance(v, str) and v.startswith('--'):
                    if (match := re.match('--(\w+):\s*(.*)', v)):
                        _type, _value = match.groups()
                        preargs = [f"--{prefix_k[1:]}", f"-{k}"]
                        if _type == 'bool':
                            default = eval(_type)(_value)
                            parser.add_argument(*preargs, action='store_true' if default else 'store_false', default=not default)
                        elif _type in ['str', 'int', 'float']:
                            _type = eval(_type)
                            parser.add_argument(*preargs, type=_type, default=_type(_value))
                        elif _type.startswith('list'):
                            parser.add_argument(*preargs, nargs='*', default=eval(_value), type=eval(_type[5:]))
                        flag = True
                    else:
                        raise AttributeError("please make sure your argument follows --{type}:{default_value}")
            return flag
        if f(self):
            args, unknown = parser.parse_known_args()
            self.update(**vars(args))

    def __repr__(self):
        return pformat(self.to_dict())

    def to_dict(self):
        return to_dict(self.copy())

    def __str__(self):
        choice = r"^(choice|interval|range|sort|shuffle|tag|glob)\(.*\)"
        def show(x):
            if x is None or x == 'null':
                return 'null'
            elif isinstance(x, str) and not re.match(choice, x): 
                return f'"{x}"'
            elif not isinstance(x, Mapping):
                return x
            return '{' + ', '.join(f"{k}: {show(v)}" for (k, v) in x.items()) + '}'
        return show(self)

    def hydra_prepare(self, sweep=False):
        """treat arg as sys.argv to be read by hydra"""
        if sweep: 
            sys.argv.extend(["--multirun", "hydra/sweeper=example"])
        for k,v in flatten_dict(self).items():  # type: ignore
            sys.argv.append("%s=%s"%(k, v))
    
    def parse_args(self, sep='', eql='=', ignore=[]):
        if sep != '':
            return sep.join([f'{k}{eql}{v}' for k,v in flatten_dict(self).items() if not k in ignore])
        from hydra.core.override_parser.overrides_parser import ( OverridesParser, create_functions,)
        rules = create_functions()
        parser = OverridesParser(rules)
        return parser.parse_rule(str(self), 'dictContainer')