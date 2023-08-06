# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['repoupdate']
entry_points = \
{'console_scripts': ['repoupdate = repoupdate:main']}

setup_kwargs = {
    'name': 'repoupdate',
    'version': '0.1.0',
    'description': 'Sync your local with remote',
    'long_description': 'None',
    'author': 'Jiri Podivin',
    'author_email': 'jpodivin@redhat.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
