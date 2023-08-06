# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['monarch_py',
 'monarch_py.datamodels',
 'monarch_py.implementations',
 'monarch_py.implementations.solr',
 'monarch_py.implementations.sql',
 'monarch_py.interfaces',
 'monarch_py.service',
 'monarch_py.utilities']

package_data = \
{'': ['*']}

install_requires = \
['docker>=6.0.1,<7.0.0',
 'linkml>=1.3.14,<2.0.0',
 'mkdocs-material>=8.5.10,<9.0.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mkdocstrings[python]>=0.19.0,<0.20.0',
 'pydantic>=1.9.1,<2.0.0',
 'pystow>=0.4.9,<0.5.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['monarch = monarch_py.cli:app']}

setup_kwargs = {
    'name': 'monarch-py',
    'version': '0.3.3',
    'description': 'Monarch Initiative data access library',
    'long_description': 'None',
    'author': 'Kevin Schaper',
    'author_email': 'kevin@tislab.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
