# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['essencia_model', 'essencia_model.base']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'deta[async]==1.1.0a2',
 'pydantic[dotenv,email]>=1.10.4,<2.0.0',
 'starlette>=0.24.0,<0.25.0']

setup_kwargs = {
    'name': 'essencia-model',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
