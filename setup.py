#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""4chan Python Library.

BASC-py4chan is a Python library that gives access to the 4chan API
and an object-oriented way to browse and get board and thread
information quickly and easily.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
the LICENSE file for more details.
"""

from setuptools import setup

setup(
    name='BASC-py4chan',
    version='0.6.5',
    description=("Python 4chan API Wrapper. Improved version of Edgeworth's "
                 "original py-4chan wrapper."),
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author='Antonizoon Overtwater',
    author_email='antonizoon@bibanon.org',
    url='http://github.com/bibanon/BASC-py4chan',
    packages=['basc_py4chan'],
    package_dir={
        'basc_py4chan': 'basc_py4chan',
    },
    package_data={'': ['README.rst', 'LICENSE']},
    install_requires=['requests >= 1.0.0'],
    extras_require={
        'test': [
            'pytest==3.5.1',
        ],
        'server': [
            'appdirs>=1.4.3',
            'beautifulsoup4>=4.6.0',
            'click>=6.7',
            'Flask-Admin>=1.5.0',
            'flask-paginate>=0.5.1',
            'flask-sqlalchemy>=2.3.2',
            'Flask-WTF>=0.14.2',
            'Flask>=0.12.2',
            'furl>=1.0.1',
            'SQLAlchemy-Utils>=0.32.18',
            'sqlalchemy>=1.2.4',
            'structlog>=18.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'basc-py4chan-server = basc_py4chan_server.__main__:cli'
        ]
    },
    keywords='4chan api',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
