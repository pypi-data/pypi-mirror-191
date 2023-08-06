# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lyceeplus']
setup_kwargs = {
    'name': 'lyceeplus',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Pierre Lemaitre',
    'author_email': 'oultetman@sfr.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
