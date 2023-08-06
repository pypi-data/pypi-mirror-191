# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hyena']
setup_kwargs = {
    'name': 'hyena-py',
    'version': '0.0.1.dev1',
    'description': 'data purifier with schema',
    'long_description': '[![version badge](https://badge.fury.io/py/hyena.svg)](https://badge.fury.io/py/hyena)\n\n**hyena** is data purifier with schema\n\n## Warning\n\nThis repository is on developing. Some bugs may exist, possible to change suddenly. And no document yet.\n\n\n## Installation\n\n    pip install hyena\n',
    'author': 'jrog612',
    'author_email': 'jrog612@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jrog612/hyena',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
