# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_registry_python']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

entry_points = \
{'console_scripts': ['schema_registry_python_cli = '
                     'schema_registry_python.cli:cli']}

setup_kwargs = {
    'name': 'schema-registry-python',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'h-silva',
    'author_email': 'h-silva@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
