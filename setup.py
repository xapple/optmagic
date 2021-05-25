#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio
"""

# Imports #
from setuptools import setup, find_namespace_packages
from os import path

# Load the contents of the README file #
this_dir = path.abspath(path.dirname(__file__))
readme_path = path.join(this_dir, 'README.md')
with open(readme_path, encoding='utf-8') as handle: readme = handle.read()

# Call setup #
setup(
    name             = 'optmagic',
    version          = '1.0.9',
    description      = 'Automatically make a command line interface from a '
                       'python class or function.',
    license          = 'MIT',
    url              = 'http://github.com/xapple/optmagic/',
    author           = 'Lucas Sinclair',
    author_email     = 'lucas.sinclair@me.com',
    packages         = find_namespace_packages(),
    install_requires = ['docstring_parser'],
    python_requires  = ">=3.6",
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
)
