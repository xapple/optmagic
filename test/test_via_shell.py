#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to test the functionality of the `optmagic` module.

You can execute these tests with pytest.

Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio

Call it like this:

    $ pytest ./test_via_shell.py
"""

# Built-in modules #
import os, inspect

# Third party modules #
import pbs3

# Constants #
file_name = inspect.getframeinfo(inspect.currentframe()).filename
this_dir  = os.path.dirname(os.path.abspath(file_name)) + '/'

# Create the command #
cmd = pbs3.Command(this_dir + 'expose_class.py')

###############################################################################
def test_simple_case():
    # Call the command #
    output = cmd()
    # Check the result #
    assert output == 'xxxxxxx'

###############################################################################
if __name__ == '__main__':
    test_simple_case()