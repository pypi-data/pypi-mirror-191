# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causal_discovery', 'causal_discovery.algos', 'causal_discovery.scripts']

package_data = \
{'': ['*']}

install_requires = \
['dm-haiku>=0.0.9,<0.0.10',
 'jax>=0.4.1,<0.5.0',
 'jaxlib>=0.4.1,<0.5.0',
 'matplotlib>=3.6.2,<4.0.0',
 'networkx>=2.8.8,<3.0.0',
 'optax>=0.1.4,<0.2.0',
 'pyvis>=0.3.1,<0.4.0',
 'seaborn>=0.12.1,<0.13.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'causal-discovery',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Causal discovery\n\nCausal discovery is the process of inferring causal relationships between variables from observational data. This repository aims to provide a collection of causal discovery algorithms implemented in Python.\n\n## Development setup\n\nThis repository uses [Poetry](https://python-poetry.org/) as a dependency manager. To install the dependencies, run:\n\n```zsh\n$ poetry install\n```\n\n## Usage\n\nPull this repository and run the following command:\n\n```zsh\n$ poetry build\n```\n\nThen, install the package:\n\n```zsh\n$ pip install dist/causal-discovery-0.1.0.tar.gz\n```\n\nexample usage:\n\n```python\nfrom causal_discovery.algos.notears import NoTears\n\n# load dataset\ndataset = ...  \n\n# initialize model\nmodel = NoTears(\n    rho=1, \n    alpha=0.1, \n    l1_reg=0, \n    lr=1e-2\n)\n\n# learn the graph\n_ = model.learn(dataset.X)\n\n# adjacency matrix\nprint(model.W)\n```\n\n## Algorithms\n\n| Algorithm | Reference |\n|-----------|-----------|\n| **NOTEARS** | [DAGs with NO TEARS: Continuous Optimization for Structure Learning, 2019](https://arxiv.org/abs/1803.01422) |\n\n## Results\n\nThis is the example of the results of the algorithm.\n\n![Results](./images/notears_res.png)\n',
    'author': 'nutorbit',
    'author_email': 'nutorbitx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
