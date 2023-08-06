# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tech']

package_data = \
{'': ['*'], 'tech': ['data/*']}

install_requires = \
['cvxopt>=1.2,<2.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.3.4,<2.0.0',
 'scipy>=1.6,<2.0']

setup_kwargs = {
    'name': 'fortitudo-tech',
    'version': '0.8.2',
    'description': 'Investment and risk technologies maintained by Fortitudo Technologies.',
    'long_description': '.. image:: https://github.com/fortitudo-tech/fortitudo.tech/actions/workflows/tests.yml/badge.svg\n   :target: https://github.com/fortitudo-tech/fortitudo.tech/actions/workflows/tests.yml\n\n.. image:: https://codecov.io/gh/fortitudo-tech/fortitudo.tech/branch/main/graph/badge.svg?token=Z16XK92Gkl \n   :target: https://codecov.io/gh/fortitudo-tech/fortitudo.tech\n\n.. image:: https://static.pepy.tech/personalized-badge/fortitudo-tech?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads\n   :target: https://pepy.tech/project/fortitudo-tech\n\nFortitudo Technologies Open Source\n==================================\n\nThis package allows you to freely explore open-source implementations of some\nof our fundamental technologies, e.g., Entropy Pooling and CVaR optimization \nin Python.\n\nThe package is intended for advanced users who are comfortable specifying\nportfolio constraints and Entropy Pooling views using matrices and vectors.\nThis gives full flexibility in relation to working with these technologies\nand allows you to build your own high-level interfaces if you wish. Hence,\ninput checking is intentionally kept to a minimum.\n\nFortitudo Technologies is a fintech company that offers novel investment\ntechnologies as well as quantitative and digitalization consultancy to the\ninvestment management industry. For more information, please visit our\n`website <https://fortitudo.tech>`_.\n\nInstallation Instructions\n-------------------------\n\nInstallation can be done via pip::\n\n   pip install fortitudo.tech\n\nFor best performance, we recommend that you install the package in a `conda environment\n<https://conda.io/projects/conda/en/latest/user-guide/concepts/environments.html>`_\nand let conda handle the installation of dependencies before installing the\npackage using pip. You can do this by following these steps::\n\n   conda create -n fortitudo.tech python scipy pandas -y\n   conda activate fortitudo.tech\n   conda install -c conda-forge cvxopt=1.3 -y\n   pip install fortitudo.tech\n\nThe examples might require you to install additional packages, e.g., seaborn and\nipykernel / notebook / jupyterlab if you want to run the notebooks. Using pip to\ninstall these packages should not cause any dependency issues.\n\nDisclaimer\n----------\n\nThis package is completely separate from our proprietary solutions and therefore\nnot representative of neither the quality nor the functionality offered by the Simulation\nEngine and Investment Analysis modules. If you are an institutional investor and want\nto experience how some of these methods can be used in practice for sophisticated\ninvestment analysis, please request a demo by sending an email to demo@fortitudo.tech.\n',
    'author': 'Fortitudo Technologies',
    'author_email': 'software@fortitudo.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://fortitudo.tech',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
