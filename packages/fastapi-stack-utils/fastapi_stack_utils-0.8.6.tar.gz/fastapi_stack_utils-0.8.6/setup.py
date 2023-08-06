# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_stack_utils',
 'fastapi_stack_utils.cli',
 'fastapi_stack_utils.schemas']

package_data = \
{'': ['*']}

install_requires = \
['asgi-correlation-id==3.2.2',
 'fastapi==0.92.0',
 'pydantic-vault==0.7.2',
 'python-json-logger==2.0.5',
 'pytz==2022.7.1',
 'sentry-sdk==1.15.0',
 'typer[all]==0.7.0',
 'uvicorn[standard]==0.20.0']

entry_points = \
{'console_scripts': ['fsu = fastapi_stack_utils.cli.cli:cli']}

setup_kwargs = {
    'name': 'fastapi-stack-utils',
    'version': '0.8.6',
    'description': 'Utils to extend the FastAPI with logging and exception handlers',
    'long_description': 'None',
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas-ks@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
