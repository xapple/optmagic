#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio
"""

# Built-in modules #
import os, argparse

###############################################################################
class PytestAction(argparse.Action):
    """
    The module base directory should be passed in with `default`
    """

    def __init__(self, option_strings, dest, **kwargs):
        # Call the parent class constructor #
        super().__init__(option_strings, dest, **kwargs)
        # No metavar #
        self.metavar = '\b'
        # No destination #
        self.dest = argparse.SUPPRESS
        # No arguments #
        self.nargs = 0

    def __call__(self, parser, namespace, values, option_string=None):
        # Import #
        import pytest
        # The module directory can't end with a slash #
        self.default = self.default.rstrip('/')
        # Where are the tests #
        if os.path.basename(self.default) == 'tests':
            test_dir = self.default
        else:
            test_dir = self.default + '/tests'
        # Run #
        exit_code = pytest.main([test_dir])
        # Exit cleanly #
        parser.exit(status=exit_code)