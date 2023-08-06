# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['TtoS']
setup_kwargs = {
    'name': 'ttos-py',
    'version': '0.1.0',
    'description': '',
    'long_description': '## Soon...',
    'author': 'fixees',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
