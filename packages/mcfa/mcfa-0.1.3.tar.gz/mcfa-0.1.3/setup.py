# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcfa']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyppca>=0.0.4,<0.0.5',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'tensorflow-probability>=0.16.0,<0.17.0',
 'tensorflow>=2.11.0,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'mcfa',
    'version': '0.1.3',
    'description': 'Mixtures of Common Factor Analyzers with missing data',
    'long_description': '[![arXiv](https://img.shields.io/badge/arXiv-2203.11229-f9f107.svg)](https://arxiv.org/abs/2203.11229) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n<p align="center">\n  <img width="260" src="https://raw.githubusercontent.com/maxmahlke/mcfa/main/gfx/logo_mcfa.png">\n</p>\n\nThis `python` package implements the Mixtures of Common Factor Analyzers model\nintroduced by [Baek+ 2010](https://ieeexplore.ieee.org/document/5184847). It\nuses [tensorflow](https://www.tensorflow.org/) to implement a stochastic\ngradient descent, which allows for model training without prior imputation of\nmissing data. The interface resembles the [sklearn](https://scikit-learn.org/stable/) model API.\n\n# Documentation\n\nRefer to the `docs/documentation.ipynb` for the documentation and\n`docs/4d_gaussian.ipynb` for an example application.\n\n# Install\n\nInstall from PyPi using `pip`:\n\n     $ pip install mcfa\n\nThe minimum required `python` version is 3.8.\n\n# Alternatives\n\n- [EMMIXmfa](https://github.com/suren-rathnayake/EMMIXmfa) in `R`\n- [Casey+ 2019](https://github.com/andycasey/mcfa) in `python`\n\nCompared to this implementation, Casey+ 2019 use an EM-algorithm instead of a\nstochastic gradient descent. This requires the imputation of the missing values\n**before** the model training. On the other hand, there are more initialization\nroutines the lower space loadings and factors available in the Casey+ 2019 implementation.\n',
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maxmahlke/mcfa.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
