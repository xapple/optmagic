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

# Constants #
file_name = inspect.getframeinfo(inspect.currentframe()).filename
this_dir  = os.path.dirname(os.path.abspath(file_name)) + '/'

###############################################################################
def test_simple_case():
    # Create the command #
    import pbs3
    cmd = pbs3.Command(this_dir + 'expose_the_class.py')
    # Call the command #
    output = cmd('--name=corvette')
    # What we expect #
    expected = "This automatic red car is named corvette.\n" \
               "It can go up to 60 km/h.\n\n"
    # Check the result #
    assert str(output) == expected

###############################################################################
if __name__ == '__main__':
    test_simple_case()