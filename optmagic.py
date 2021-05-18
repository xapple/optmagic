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
import sys, argparse, types, inspect, functools, os.path

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

        Other:

            For debugging you can set the special attribute `optmagic_argv`
            to a string of your choosing which will cause sys.argv to be
            ignored.
        """
        self.obj = function_or_class

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object on '%s'>" % (self.__class__.__name__, self.obj)

    #----------------------------- Properties --------------------------------#
    @functools.cached_property
    def type(self):
        # Determine the type of the attribute #
        if isinstance(self.obj, type):                 return 'class'
        elif isinstance(self.obj, types.FunctionType): return 'function'
        # Otherwise raise an exception #
        else:
            msg = "OptMagic should be called with a function or a class but" \
                  " not with `%s`." % self.obj
            raise ValueError(msg)

    @functools.cached_property
    def func(self):
        # If it's a class we want to target the constructor #
        if self.type == 'class':    return self.obj.__init__
        if self.type == 'function': return self.obj

    @functools.cached_property
    def docstring(self):
        """
        If you use `inspect.getdoc(self.func)` it returns something slightly
        different.
        """
        return self.func.__doc__

    @functools.cached_property
    def sig(self):
        return inspect.signature(self.obj)

    @functools.cached_property
    def spec(self):
        """Unused."""
        return inspect.getfullargspec(self.obj)

    @functools.cached_property
    def defaults(self):
        """Unused."""
        return dict(zip(reversed(self.spec.args),
                        reversed(self.spec.defaults)))

    @functools.cached_property
    def sub_docs(self):
        """Is able to parse numpydoc style doc strings amongst others."""
        return {param.arg_name: param.description
                for param in docstring_parser.parse(self.docstring).params}

    @functools.cached_property
    def arguments(self):
        """Create all Argument objects."""
        return [Argument(param.name,
                         param.default,
                         self.sub_docs[param.name],
                         self)
                for param in self.sig.parameters.values()]

    #----------------------------- Parameters --------------------------------#
    @functools.cached_property
    def name_string(self):
        return "Cool"

    @functools.cached_property
    def version_string(self):
        return "version X.Y.Z"

    @functools.cached_property
    def title_string(self):
        """
        A string that appears at the top of the help message.
        This could be for instance:
            > "Classify from module `crest4` version 4.0.1"
        """
        return "Lorem ipsum dolor sit amet"

    #------------------------------- Objects ---------------------------------#
    @functools.cached_property
    def options(self):
        """
        It is also possible to change the program name with:
            prog = self.name_string
        Other:
            * usage='%(prog)s [options] path',
            * epilog='Enjoy the program! :)')
        """
        # Options for the parser #
        return dict(description  = self.title_string,
                    allow_abbrev = True)

    @functools.cached_property
    def parser(self):
        # Create the parser #
        parser = argparse.ArgumentParser(**self.options)
        # Iterate over arguments #
        for arg in self.arguments: arg.add_arg(parser)
        # Add the version argument #
        parser.add_argument('--version', '-v', action='version',
                            version=self.version_string)
        # Return #
        return parser

    @functools.cached_property
    def parsed_args(self):
        # Check for debug mode #
        if hasattr(self, 'optmagic_argv'):
            import shlex
            argument_list = shlex.split(self.optmagic_argv)
            return self.parser.parse_args(argument_list)
        # Call the parser #
        return self.parser.parse_args()

    @functools.cached_property
    def kwargs(self):
        return vars(self.parsed_args)

    #------------------------------- Methods ---------------------------------#
    def __call__(self, *extra_args, **extra_kwargs):
        # Call if it's a function #
        if self.type == 'function':
            return self.func(**self.kwargs)
        # Call if it's a class #
        if self.type == 'class':
            instance = self.obj(**self.kwargs)
            return instance(*extra_args, **extra_kwargs)

################################################################################
class Argument:

    def __init__(self, name, default, desc, optmagic):
        # The python variable name #
        self.name = name
        # The default value #
        self.default = default
        # The description of this argument in the docstring #
        self.desc = desc
        # A reference to the parent object #
        self.optmagic = optmagic
        # An attribute to check if a value is cached #
        self.letter_chosen = False

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object '%s'>" % (self.__class__.__name__, self.name)

    def __str__(self):
        """A longer string representation for printing purposes."""
        msg = f"Argument `{self.name}`"
        if self.has_default: msg += f" with default '{self.default}'."
        else:                msg += f" without a default."
        return msg

    #----------------------------- Properties --------------------------------#
    @functools.cached_property
    def has_default(self):
        """Did the argument have a default value or not?"""
        return self.default is not inspect._empty

    @functools.cached_property
    def short_letter(self):
        """
        Pick a short letter for the option in addition to its full name.
        For this we need to check the short letters of the other arguments
        in order to avoid picking twice the same one.
        """
        # Which letters have been taken already #
        existing = set(arg.short_letter for arg in self.optmagic.arguments
                       if arg.letter_chosen is True) | {'h', 'v'}
        # So that other arguments can check if this attribute is set #
        self.letter_chosen = True
        # Check if all letters are taken #
        if len(existing) == 26: return None
        # Function to pick possible letters iteratively #
        def pick_letter():
            yield self.name[0]
            parts = self.name.split('_')
            if len(parts) > 1: yield parts[1][0]
            if len(parts) > 2: yield parts[2][0]
            if len(parts) > 3: yield parts[3][0]
            else:
                for letter in self.name:
                    if letter != '_': yield letter
        # Pick #
        for letter in pick_letter():
            if letter not in existing: return letter

    #----------------------------- Parameters --------------------------------#
    @functools.cached_property
    def help(self):
        """
        Lorem.
        """
        return "Help string for " + self.name + "."

    @functools.cached_property
    def default(self):
        """
        Lorem.
        """
        if self.has_default: return self.default
        else:                return None

    @functools.cached_property
    def choices(self):
        """
        parser.add_argument('throw', choices=['rock', 'paper', 'scissors']).
        """
        return None

    @functools.cached_property
    def type(self):
        """
        parser.add_argument('throw',  type=int).
        """
        return None

    @functools.cached_property
    def kwargs(self):
        # Initialize #
        kwargs = {}
        # Add options #
        if self.help is not None:    kwargs['help'] = self.help
        if self.default is not None: kwargs['default'] = self.default
        if self.choices is not None: kwargs['choices'] = self.choices
        if self.type is not None:    kwargs['type'] = self.type
        # Is it required #
        kwargs['required'] = not self.has_default
        # Return #
        return kwargs

    #------------------------------- Methods ---------------------------------#
    def add_arg(self, parser):
        """Add this argument to the argparse parser."""
        parser.add_argument('--' + self.name,
                            '-' + self.short_letter,
                            **self.kwargs)

###############################################################################
if __name__ == '__main__':
    # Get the current directory of this python script #
    this_file = (inspect.stack()[0])[1]
    this_dir  = os.path.dirname(this_file)
    # Get the path of our test class #
    class_file = this_dir + '/test/simple_car_class.py'
    # Import it #
    from importlib.machinery import SourceFileLoader
    module = SourceFileLoader("simple_car", class_file).load_module()
    # Create an object #
    self = OptMagic(module.Car)
    # Forward the arguments #
    self.optmagic_argv = ' '.join(sys.argv[1:])
    # Call #
    self()
