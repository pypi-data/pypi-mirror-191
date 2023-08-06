# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tknlp', 'tknlp.contribute', 'tknlp.spacy']

package_data = \
{'': ['*']}

install_requires = \
['FastNLP==1.0.1',
 'Unidecode>=1.3.6,<2.0.0',
 'cloudpickle==2.2.0',
 'contractions>=0.1.73,<0.2.0',
 'emoji==1.7.0',
 'fitlog==0.9.15',
 'ftfy==6.1.1',
 'hydra-core==1.2.0',
 'ipython==8.7.0',
 'lemminflect>=0.2.3,<0.3.0',
 'numpy==1.23.5',
 'optuna>=3.0.5,<4.0.0',
 'pandas==1.5.1',
 'pyspellchecker==0.7.0',
 'python-dotenv==0.19.2',
 'scikit-learn==1.1.3',
 'scipy==1.8.1',
 'sentence-transformers==2.2.2',
 'torchmetrics>=0.11.0,<0.12.0',
 'transformers==4.25.1']

setup_kwargs = {
    'name': 'tknlp',
    'version': '0.1.6',
    'description': '',
    'long_description': '# TKNLP\n\n\nRun NLP tools in an easier manner\n\n## Installation\n\n```bash\npip install tknlp\n```\n',
    'author': 'dennislblog',
    'author_email': 'dennisl@udel.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
