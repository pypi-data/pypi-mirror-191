# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikeometric',
 'spikeometric.datasets',
 'spikeometric.models',
 'spikeometric.stimulus']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0',
 'networkx>=3.0,<4.0',
 'numpy>=1.21.4,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'spikeometric',
    'version': '0.1.0',
    'description': 'Spikeometric is a Pytorch Geometric based framework for simulating spiking neural networks (SNNs) using Generalized Linear Models and Linear-Nonlinear-Poisson models.',
    'long_description': "# Spikeometric - GLM-based Spiking Neural Networks with PyTorch Geometric\n\nThis package provides a simple and scaleable way to simulate networks of neurons using either\nLinear-Nonlinear-Poisson models (LNP) or its cousin the Generalized Linear Model (GLM).\n\nThe framework is built on top of torch modules and let's you tune parameters in your model to match a certain firing rate, provided the model is differentiable. \n\nOne key application is the problem of infering connectivity from spike data, where these models are often used both as generative and inference models.\n\n# Install\nBefore installing `spikeometric` you will need to download versions of PyTorch and PyTorch Geometric that work with your hardware. When you have done that (for example in a conda environment), you are ready to download spikeometric with:\n\n    pip install spikeometric\n\n# Documentation\n\nFor more information about the package and a full API reference check out our [documentation](https://spikeometric.readthedocs.io/en/latest/).\n",
    'author': 'Jakob Sønstebø',
    'author_email': 'jakobls16@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bioAI-Oslo/Spikeometric',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
