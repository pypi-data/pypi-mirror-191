# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['essencia_engine', 'essencia_engine.base']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Unidecode>=1.3.6,<2.0.0',
 'anyio>=3.6.2,<4.0.0',
 'asgi-csrf>=0.9,<0.10',
 'bcrypt>=4.0.1,<5.0.0',
 'deta[async]==1.1.0a2',
 'httpx>=0.23.3,<0.24.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'pydantic[email,dotenv]>=1.10.4,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'starlette>=0.24.0,<0.25.0',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'essencia-engine',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
