# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cggnn',
 'cggnn.explain',
 'cggnn.util',
 'cggnn.util.interpretability',
 'cggnn.util.ml',
 'cggnn.util.ml.layers']

package_data = \
{'': ['*']}

install_requires = \
['bokeh',
 'h5py',
 'matplotlib',
 'networkx',
 'numpy',
 'pandas',
 'psycopg2-binary',
 'pyshp',
 'scikit-learn',
 'scipy',
 'tables',
 'tqdm']

setup_kwargs = {
    'name': 'cg-gnn',
    'version': '0.1.3',
    'description': 'Create cell graphs from pathology slide data and train a graph neural network to predict patient outcomes for SPT.',
    'long_description': '# `cg-gnn`\n\n`cg-gnn` (short for "Cell Graph - Graph Neural Networks\'\') is a library to create cell graphs from pathology slide data and train a graph neural network model using them to predict patient outcomes. This library is designed to be used with and as part of the [SPT framework](https://github.com/nadeemlab/SPT), although independent functionality is also possible provided you can provide formatted, cell level slide data.\n\nThis library is a heavily modified version of [histocartography](https://github.com/BiomedSciAI/histocartography) and two of its applications, [hact-net](https://github.com/histocartography/hact-net) and [patho-quant-explainer](https://github.com/histocartography/patho-quant-explainer).\n\n## Installation\n\n### Using pip\n\nIn addition to installing via pip,\n```\npip install cg-gnn\n```\nyou must also install using the instructions on their websites,\n* [pytorch](https://pytorch.org/get-started/locally/)\n* [DGL](https://www.dgl.ai/pages/start.html)\n* [CUDA](https://anaconda.org/nvidia/cudatoolkit) (optional but highly recommended if your machine supports it)\n\n### From source\n\n1. Clone this repository\n2. Create a conda environment using\n```\nconda env create -f environment.yml\n```\n3. Run this module from the command line using `main.py`. Alternatively, scripts in the main directory running from `a` to `d4` allow you to step through each individual section of the `cg-gnn` pipeline, saving files along the way.\n\n\n## Credits\n\nAs mentioned above, this repository is a heavily modified version of [the histocartography project](https://github.com/BiomedSciAI/histocartography) and two of its applications: [hact-net](https://github.com/histocartography/hact-net) and [patho-quant-explainer](https://github.com/histocartography/patho-quant-explainer). Specifically,\n\n* Cell graph formatting, saving, and loading using DGL is patterned on how they were implemented in hact-net\n* The neural network training and inference module is modified from the hact-net implementation for cell graphs\n* Importance score and separability calculations are sourced from patho-quant-explainer\n* The dependence on histocartography is indirect, through the functionality used by the above features\n\nDue to dependency issues that arose when using the version of histocartography published on PyPI, we\'ve chosen to copy and make slight updates to only the modules of histocartography used by the features supported in this library.\n',
    'author': 'Carlin Liao',
    'author_email': 'liaoc2@mskcc.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CarlinLiao/cg-gnn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
