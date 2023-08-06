#!/usr/bin/env python

from __future__ import print_function

import sys

from setuptools import setup

if sys.version_info < (2, 7):
    print("Python versions prior to 2.7 are not supported for pip installed mlsql-plugin.",
          file=sys.stderr)
    sys.exit(-1)

try:
    exec(open('version.py').read())
except IOError:
    print("Failed to load mlsql-plugin version file for packaging.",
          file=sys.stderr)
    sys.exit(-1)

VERSION = __version__

setup(
    name='mlsql_plugin_tool',
    version=VERSION,
    description='Tool to build MLSQL Plugin',
    long_description="Tool to build MLSQL Plugin from https://github.com/allwefantasy/mlsql-plugins",
    author='WilliamZhu',
    author_email='allwefantasy@gmail.com',
    url='https://github.com/allwefantasy/mlsql-plugin-tool',
    packages=['tech',
              'tech.mlsql',
              'tech.mlsql.plugin',
              'tech.mlsql.plugin.tool',
              'tech.mlsql.plugin.tool.commands'
              ],
    include_package_data=True,
    license='http://www.apache.org/licenses/LICENSE-2.0',
    install_requires=[
        'click>=6.7',
        'jinja2>=3.0.0',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        mlsql_plugin_tool=tech.mlsql.plugin.tool.Plugin:main
    ''',
    setup_requires=['pypandoc'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy']
)
