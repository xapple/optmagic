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
import argparse, types, inspect

# Third party modules #
import docstring_parser

################################################################################
class OptMagic:
    """
    This class enables you to create simple command line interfaces starting
    with a class or a function that you want to expose directly to the shell.
    See documentation at https://github.com/xapple/optmagic/
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
    def type(self):
        # Determine the type of the attribute #
        if isinstance(self.obj, type):                 return 'class'
        elif isinstance(self.obj, types.FunctionType): return 'function'
        # Otherwise raise an exception #
        else:
            msg = "OptMagic should be called with a function or a class but" \
                  " not with `%s`." % self.obj
            raise ValueError(msg)

    @property
    def func(self):
        # If it's a class we want to target the constructor #
        if self.type == 'class':    return self.obj.__init__
        if self.type == 'function': return self.obj

    @property
    def docstring(self):
        """
        If you use `inspect.getdoc(self.func)` it returns something slightly
        different.
        """
        return self.func.__doc__

    @property
    def sig(self):
        return inspect.signature(self.obj)

    @property
    def spec(self):
        return inspect.getfullargspec(self.obj)

    @property
    def defaults(self):
        return dict(zip(reversed(self.spec.args),
                        reversed(self.spec.defaults)))

    @property
    def mandatory(self):
        return {param.name
                for param in self.sig.parameters.values()
                if param.default is inspect._empty]

    @property
    def optional(self):
        return {param.name: param.default
                for param in self.sig.parameters.values()
                if param.default is not inspect._empty}

    @property
    def docs(self):
        return {param.arg_name: param.description
                for param in docstring_parser.parse(self.docstring).params}

    @property
    def arguments(self):
        """
        Create Argument objects.
        """
        return [Argument(param.name, param.default, self.docs['param.name'])
                for param in self.sig.parameters.values()]

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
        if self.type == 'function':
            return self.func(*self.args, **self.kwargs)
        # Call if it's a class #
        if self.type == 'class':
            instance = self.obj(*self.args, **self.kwargs)
            return instance(*extra_args, **extra_kwargs)

################################################################################
class Argument:

    def __init__(self, name):
        """
        Lorem.
        """
        self.obj = name
