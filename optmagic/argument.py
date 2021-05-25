#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio
"""

# Built-in modules #
import inspect, functools, re

###############################################################################
class Argument:

    def __init__(self, optmagic, name, default, desc):
        # A reference to the parent object #
        self.optmagic = optmagic
        # The python variable name #
        self.name = name
        # The default value #
        self.default = default
        # The description of this argument in the docstring #
        self.desc = desc
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
        # Some names can be abbreviated #
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
        # We should add it to the default group in most cases #
        if self.has_default: group = parser
        # If we don't have a default value we add it to the required group #
        else: group = required
        # Call method with all arguments #
        return group.add_argument('--' + self.name,
                                  '-' + self.short_letter,
                                  **self.kwargs)