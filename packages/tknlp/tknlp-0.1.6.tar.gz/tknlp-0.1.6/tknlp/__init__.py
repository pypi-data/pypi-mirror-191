from .utils import one_time, find_dotenv, get_dir, ojoin, oexists, obase
from .spacy import make_ner_scorer
from .cli import Args
from .contribute import color_str, pickle_dump, pickle_load, get_num_gpu
from dotenv import load_dotenv

@one_time
def load_env():
    load_dotenv(find_dotenv(get_dir()))
load_env()