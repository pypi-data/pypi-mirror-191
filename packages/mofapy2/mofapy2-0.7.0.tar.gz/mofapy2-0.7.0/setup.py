# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mofapy2',
 'mofapy2.build_model',
 'mofapy2.core',
 'mofapy2.core.distributions',
 'mofapy2.core.nodes',
 'mofapy2.notebooks',
 'mofapy2.run',
 'mofapy2.simulate']

package_data = \
{'': ['*'], 'mofapy2.run': ['test_data/*', 'test_data/with_nas/*']}

install_requires = \
['h5py>=3,<4',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'scikit-learn>=1,<2',
 'scipy>=1,<2']

setup_kwargs = {
    'name': 'mofapy2',
    'version': '0.7.0',
    'description': 'Multi-omics factor analysis',
    'long_description': '# Multi-Omics Factor Analysis\n\n![PyPi version](https://img.shields.io/pypi/v/mofapy2)\n\nMOFA is a factor analysis model that provides a general framework for the integration of multi-omic data sets in an unsupervised fashion.  \nThis repository contains `mofapy2` Python library source code.\n\n- For the downstream analysis in Python please check the mofax package: https://github.com/bioFAM/mofax\n- For the downstream analysis in R please check the MOFA2 package: https://github.com/bioFAM/MOFA2\n\nPlease [visit our website](https://biofam.github.io/MOFA2/) for details, tutorials, and much more.\n\n## Installation\n\nInstall the stable version from the Python Package Index:\n```\npip install mofapy2\n```\n\nOr install the latest development version from the repository:\n```\npip install git+https://github.com/bioFAM/mofapy2@dev --force-reinstall --no-deps\n```\n\n\n',
    'author': 'Ricard Argelaguet',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https:/biofam.github.io/MOFA2/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
