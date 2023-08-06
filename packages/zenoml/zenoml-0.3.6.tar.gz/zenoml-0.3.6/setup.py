# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeno', 'zeno.classes', 'zeno.data_pipeline']

package_data = \
{'': ['*'],
 'zeno': ['frontend/*', 'frontend/build/*', 'frontend/build/assets/*']}

install_requires = \
['fastapi>=0.75,<0.90',
 'inquirerpy>=0.3.4,<0.4.0',
 'methodtools>=0.4.5,<0.5.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'opentsne>=0.6.2,<0.7.0',
 'pandas>=1.4.0,<2.0.0',
 'pathos>=0.3.0,<0.4.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools>=67.0.0,<68.0.0',
 'tomli>=2.0.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'types-requests>=2.28.11,<3.0.0',
 'types-setuptools>=65.4,<68.0',
 'types-tqdm>=4.64.7,<5.0.0',
 'uvicorn>=0.17.5,<0.21.0',
 'websockets>=10.2,<11.0']

entry_points = \
{'console_scripts': ['zeno = zeno.runner:command_line']}

setup_kwargs = {
    'name': 'zenoml',
    'version': '0.3.6',
    'description': 'Interactive Evaluation Framework for Machine Learning',
    'long_description': '<img src="./zeno.png" width="250px"/>\n\n[![PyPI version](https://badge.fury.io/py/zenoml.svg)](https://badge.fury.io/py/zenoml)\n![Github Actions CI tests](https://github.com/zeno-ml/zeno/actions/workflows/test.yml/badge.svg)\n![Github Actions Docs build](https://github.com/zeno-ml/zenoml.com/actions/workflows/docs.yml/badge.svg)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Join the chat at https://gitter.im/zeno-ml-eval/community](https://badges.gitter.im/zeno-ml-eval/community.svg)](https://gitter.im/zeno-ml-eval/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\nZeno is a general-purpose framework for evaluating machine learning models.\nIt combines a **Python API** with an **interactive UI** to allow users to discover, explore, and analyze the performance of their models across diverse use cases.\nZeno can be used for any data type or task with [modular views](https://zenoml.com/docs/views/) for everything from object detection to audio transcription.\n\n## Quickstart\n\nInstall the Zeno Python package from PyPI:\n\n```bash\npip install zenoml\n```\n\n### Command Line\n\nTo get started, run the following command to initialize a Zeno project. It will walk you through creating the `zeno.toml` configuration file:\n\n```bash\nzeno init\n```\n\nTake a look at the [configuration documentation](https://zenoml.com/docs/configuration) for additional `toml` file options like adding model functions.\n\nStart Zeno with `zeno zeno.toml`.\n\n### Jupyter Notebook\n\nYou can also run Zeno directly from Jupyter notebooks or lab. The `zeno` command takes a dictionary of configuration options as input. See [the docs](https://zenoml.com/docs/configuration) for a full list of options. In this example we pass the minimum options for exploring a non-tabular dataset:\n\n```python\nimport pandas as pd\nfrom zeno import zeno\n\ndf = pd.read_csv("/path/to/metadata/file.csv")\n\nzeno({\n    "metadata": df, # Pandas DataFrame with a row for each instance\n    "view": "audio-transcription", # The type of view for this data/task\n    "data_path": "/path/to/raw/data/", # The folder with raw data (images, audio, etc.)\n    "data_column": "id" # The column in the metadata file that contains the relative paths of files in data_path\n})\n\n```\n\nYou can pass a list of decorated function references directly Zeno as you add models and metrics.\n\n## Citation\n\nPlease reference our [CHI\'22 paper](https://cabreraalex.com/zeno.pdf)\n\n```bibtex\n@inproceedings{cabrera23zeno,\n  author = {Cabrera, Ángel Alexander and Fu, Erica and Bertucci, Donald and Holstein, Kenneth and Talwalkar, Ameet and Hong, Jason I. and Perer, Adam},\n  title = {Zeno: An Interactive Framework for Behavioral Evaluation of Machine Learning},\n  year = {2023},\n  isbn = {978-1-4503-9421-5/23/04},\n  publisher = {Association for Computing Machinery},\n  address = {New York, NY, USA},\n  url = {https://doi.org/10.1145/3544548.3581268},\n  doi = {10.1145/3544548.3581268},\n  booktitle = {CHI Conference on Human Factors in Computing Systems},\n  location = {Hamburg, Germany},\n  series = {CHI \'23}\n}\n```\n\n## Community\n\nChat with us on our [Gitter channel](https://gitter.im/zeno-ml-eval/community) or leave an issue on this repository if you run into any issues or have a request!\n',
    'author': 'Ángel Alexander Cabrera',
    'author_email': 'alex.cabrera@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zenoml.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<=3.11',
}


setup(**setup_kwargs)
