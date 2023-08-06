# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['traceid']
setup_kwargs = {
    'name': 'traceid',
    'version': '0.11.1',
    'description': '',
    'long_description': '# TraceId\n\na \n\n## title\naskldjl\n',
    'author': 'Yibu Ma',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
