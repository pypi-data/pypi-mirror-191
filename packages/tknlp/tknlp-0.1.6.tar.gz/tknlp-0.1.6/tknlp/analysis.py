from .typing_ import PathLike, defaultdict, Callable
from .utils import owalk, ojoin
from fitlog.fastlog import LogReader
from joblib import Parallel, delayed, cpu_count
from tqdm import tqdm

import pandas as pd


def gather_func(df: pd.DataFrame):
    e_df = df.query('data__nw==2 & ind=="test"')
    best_epoch = e_df.loc[e_df.groupby('seed')['f1'].idxmax(), ['seed','epoch']]
    df_ = df[df.ind=='test'].groupby('data__nw').apply(lambda x : best_epoch.merge(x, on=['seed','epoch'], how='left'))
    return df_
    
def gather_prep():

class Analysis:
    """
    :param log_path:        e.g., clf_

    :logic flow:
    1) gather all result under ${log_path}
    2) 
    """
    
    def __init__(self, log_path: PathLike):
        self.log_path = log_path
        self.reader = LogReader()
        self.refresh()
        
    def refresh(self, log_path=None):
        """extract all hyperparameters of experiments        
        """
        self.reader.set_log_dir(log_path or self.log_path)
        data = self.reader.read_logs()
        self._data = {x['id']: {'hyper': x.pop('hyper')} for x in data if 'hyper' in x}
    
    def gather(self, func: Callable = None, metric: str='f', n_jobs=cpu_count(), ind: str = 'test', dir: str = 'max'):
        """apply function to the following dataframe
        
        epoch       ind     metric@1    metric@2    metric@3    ...
        1           train   0.2         0.3         0.4         ...
        """
        def gather_helper(log_name):
            log_path = ojoin(self.log_path, log_name, 'result.csv')
            df = pd.read_csv(log_path, index_col=0)
            df.columns = df.columns.str.split('.', expand=True, n=1)
            index_name = df.index.names[:-1]
            if df.columns.nlevels > 1: df = df.stack(0)
            df = df.rename_axis(index_name + ['epoch', 'ind']).reset_index()
            if func:
                return func(df)
            # gather row w.r.t. best value determiend by ${metric}
            df_ = df.query(f'ind=="{ind}"')[metric]
            if dir == 'max': 
                epoch = df.loc[df_.idxmax()]['epoch']
            elif dir == 'min':
                epoch = df.loc[df_.idxmin()]['epoch']
            elif dir == 'last':
                epoch = df.epoch.max()
            return df.query(f'epoch=="{epoch}"').drop(columns='epoch').set_index('ind').to_dict('index')

        output = Parallel(n_jobs=n_jobs)( delayed(gather_helper)(p) for p in tqdm(self._data))
        
        data = {}
        for dir, fname in owalk(self.log_path, start='log'):
            data[fname] = read_hyper(ojoin(dir, fname, 'hyper.log'))
                        

        

    @property 
    def data(self): return self._data

    def gather_data(self, best_metric: str):
        pass
        

