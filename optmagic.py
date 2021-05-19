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
import sys, argparse, types, inspect, functools, os.path, re

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
    def sub_docs(self):
        """
        The `docstring_parser` module is able to parse numpydoc style
        docstrings amongst others formats.
        """
        return {param.arg_name: param.description
                for param in docstring_parser.parse(self.docstring).params}

    @functools.cached_property
    def arguments(self):
        # Create all Argument objects #
        result = [Argument(param.name,
                         param.default,
                         self.sub_docs[param.name],
                         self)
                  for param in self.sig.parameters.values()]
        # Return #
        return result

    #----------------------------- Parameters --------------------------------#
    @functools.cached_property
    def child_module(self):
        """The sub-module from which the object is coming from."""
        return inspect.getmodule(self.obj)

    @functools.cached_property
    def base_module(self):
        """The parent package from which the object is coming from."""
        name = self.child_module.__name__.split('.')[0]
        return __import__(name)

    @functools.cached_property
    def prog_string(self):
        """
        This is the name of program that appears at the top of the help string.
        By default it should be name of the module from which the object comes
        from.
        """
        return self.base_module.__name__

    @functools.cached_property
    def usage_string(self):
        """
        This is the short description of the program that appears at the very
        top of the help string and summarizes all options.
        """
        return None

    @functools.cached_property
    def epilog_string(self):
        """
        This is an extra string that appears at the very end of the help
        message. We want to display the URL to the project page.
        """
        # Initialize #
        url = None
        # Search the child module #
        if hasattr(self.child_module, 'project_url'):
            url = self.child_module.project_url
        # Search the parent module #
        if hasattr(self.base_module, 'project_url'):
            url = self.base_module.project_url
        # Make the message #
        if url is not None:
            msg = "More information at " + url
            msg = '-'*75 + '\n| ' + msg + '\n' + '-'*75
            # Remove a new line from the last required argument #
            last_req = [arg for arg in self.arguments if not arg.has_default]
            if last_req: last_req[-1].help = last_req[-1].help[:-1]
            # Return #
            return msg

    @functools.cached_property
    def title_string(self):
        """
        A string that appears at the top of the help message.
        Just after the usage summary.
        """
        return self.base_module.__doc__

    @functools.cached_property
    def version_string(self):
        """The string returned when invoked with the '-v' option"""
        # Initialize #
        version = self.prog_string
        # Search for a version number #
        if hasattr(self.base_module, '__version__'):
            version += " version " + self.base_module.__version__
        elif hasattr(self.child_module, '__version__'):
            version += " version " + self.base_module.__version__
        # Return #
        return version

    #------------------------------- Objects ---------------------------------#
    @functools.cached_property
    def options(self):
        """
        A better formatter class could be constructed based on:
        https://stackoverflow.com/a/65891304
        """
        # Formatter #
        from argparse import RawTextHelpFormatter
        # Options for the parser #
        return dict(prog            = self.prog_string,
                    usage           = self.usage_string,
                    description     = self.title_string,
                    epilog          = self.epilog_string,
                    allow_abbrev    = True,
                    add_help        = False,
                    formatter_class = RawTextHelpFormatter)


    @functools.cached_property
    def parser(self):
        # Create the parser #
        parser = argparse.ArgumentParser(**self.options)
        # Capitalize groups #
        parser._positionals.title = 'Positional arguments'
        parser._optionals.title = 'Optional arguments'
        # Add a special group for required arguments #
        # See https://stackoverflow.com/questions/24180527
        if [arg.has_default for arg in self.arguments]:
            required = parser.add_argument_group('Required arguments')
        else:
            required = None
        # Iterate over arguments #
        for arg in self.arguments: arg.add_arg(parser, required)
        # Add the version argument #
        parser.add_argument('--version', '-v', action='version',
                            version=self.version_string,
                            help="Show program's version number and exit.")
        # Add the help argument #
        parser.add_argument('--help', '-h', action='help',
                            default=argparse.SUPPRESS,
                            help='Show this help message and exit.')
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

    #------------------------------- Extras ----------------------------------#
    @functools.cached_property
    def markdown(self):
        """
        Return a markdown version of the help string.
        This actually creates a file somewhere on the filesystem!
        """
        import argmark
        return argmark.md_help(self.parser)

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
    def flat_desc(self):
        """
        The same string as self.desc but with newlines and whitespaces removed
        as well as all lowercase.
        """
        return ' '.join(self.desc.split()).lower()

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
            parts = self.name.split('_')
            if parts[0] == 'output': yield 'o'
            if len(parts) > 1: yield parts[1][0]
            yield self.name[0]
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
        return self.desc + '\n\n'

    @functools.cached_property
    def default(self):
        if self.has_default: return self.default
        else:                return None

    @functools.cached_property
    def choices(self):
        """
        Example:
        parser.add_argument('throw', choices=['rock', 'paper', 'scissors']).
        """
        # Initialize #
        choices = None
        # Detect cases where there are only two choices #
        regex = re.compile("either ['\"`](.+?)['\"`] or ['\"`](.+?)['\"`]")
        match = regex.findall(self.flat_desc)
        if match: choices = match[0]
        # Return #
        return choices

    @functools.cached_property
    def type(self):
        """
        Example:
        parser.add_argument('throw',  type=int).
        """
        return None

    @functools.cached_property
    def metavar(self):
        """
        Example:
        parser.add_argument('throw',  metavar="EXAMPLE").
        """
        # Initialize #
        metavar = None
        # Split the docstring into words #
        words = self.desc.split()
        # Let's take the second word of the docstring if the first word
        # is "the".
        if words[0].lower() == "the":
            metavar = words[1].upper()
        # Some names can be abbriviated #
        if metavar == "NUMBER":    metavar = "NUM"
        if metavar == "DIRECTORY": metavar = "DIR"
        # Return #
        return metavar

    @functools.cached_property
    def kwargs(self):
        # Initialize #
        kwargs = {}
        # Add options #
        if self.help is not None:    kwargs['help']    = self.help
        if self.default is not None: kwargs['default'] = self.default
        if self.choices is not None: kwargs['choices'] = self.choices
        if self.type is not None:    kwargs['type']    = self.type
        if self.metavar is not None: kwargs['metavar'] = self.metavar
        # Is it required #
        kwargs['required'] = not self.has_default
        # Return #
        return kwargs

    #------------------------------- Methods ---------------------------------#
    def add_arg(self, parser, required):
        """Add this argument to the argparse parser."""
        if self.has_default: group = parser
        else:                group = required
        return group.add_argument('--' + self.name,
                                  '-' + self.short_letter,
                                  **self.kwargs)

###############################################################################
# The code below is used for debugging purposes
# It uses the test case found in the 'test/' directory

# You can call it like this:
#   $ python3 -m optmagic --name=hello
# Or via ipython for interativeness:
#   $ ipython3 -i -- optmagic.py --name hello
# Or via the executable:
#   $ test/expose_the_class.py -n hello --max_speed 130
# Or inside ipython with these commands:
#    from optmagic import OptMagic; from simple_car_class import Car;
#    self = OptMagic(Car); self.optmagic_argv = "--name=hello"; self()

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
