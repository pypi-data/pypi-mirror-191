#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os

from setuptools import setup, find_packages
from chef import __version__
setup(
    name = 'Py3Chef',
    version = __version__,
    packages = find_packages(),
    author = 'Noah Kantrowitz',
    author_email = 'noah@coderanger.net',
    maintainer = 'Leigh Johnson',
    maintainer_email = 'leigh@bitsy.ai',
    description = 'Python implementation of a Chef API client.',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license = 'Apache 2.0',
    keywords = '',
    url = 'http://github.com/leigh-johnson/pychef',
    classifiers = [],
    zip_safe = False,
    install_requires = ['six>=1.9.0','requests>=2.7.0'],
    test_suite = 'pytest',
    python_requires='>3.6.9',
    include_package_data=True
)
