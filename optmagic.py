#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio
"""

# Constants #
__version__ = '1.0.1'

# Built-in modules #
import argparse, types

################################################################################
class OptMagic:
    """
    This class enables you to create simple command line interfaces starting
    with a class or a function that you want to expose directly to the shell.
    See documentation at https://example.com/

    This project is similar in some ways to https://www.pyinvoke.org/
    """

    def __init__(self, function_or_class):
        """
        Args:

            function_or_class: You can pass either a class object or a function
                               object as the only parameter to OptMagic.
        """
        self.obj = function_or_class

    @property
    def args(self):
        """
        Lorem.
        """
        return []

    @property
    def kwargs(self):
        """
        Lorem.
        """
        return {}

    def __call__(self, *extra_args, **extra_kwargs):
        """
        Lorem.
        """
        # Call if it's a function #
        if isinstance(self.obj, types.FunctionType):
            self.obj(*self.args, **self.kwargs)
        # Call if it's a class #
        if isinstance(self.obj, type):
            instance = self.obj(*self.args, **self.kwargs)
            instance(*extra_args, **extra_kwargs)

################################################################################
class Argument:

    def __init__(self, name):
        """
        Lorem.
        """
        self.obj = name
