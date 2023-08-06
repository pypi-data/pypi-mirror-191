# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ttm']
entry_points = \
{'console_scripts': ['ttm = ttm:main']}

setup_kwargs = {
    'name': 'ttm',
    'version': '0.13.0',
    'description': 'Tiny task manager for Linux, MacOS and Unix-like systems',
    'long_description': 'None',
    'author': 'Yuri Escalianti',
    'author_email': 'yuriescl@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yuriescl/ttm',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
