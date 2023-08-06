# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Ano_express']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'pandas', 'plotly', 'scipy', 'seaborn', 'statsmodels', 'tqdm']

setup_kwargs = {
    'name': 'ano-express',
    'version': '0.0.2',
    'description': 'A package to access insecticide resistance gene expression meta analyse in Anopheles mosquitoes',
    'long_description': None,
    'author': 'Sanjay Nagi',
    'author_email': 'sanjay.nagi@lstmed.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
