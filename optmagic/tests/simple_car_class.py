#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to test the functionality of the `optmagic` module.

Contains a simple example class that we want to later expose as a
command line tool.

Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio
"""

# Built-in modules #
import os

# Constants #
project_url = 'https://github.com/xapple/optmagic'

###############################################################################
class Car:
    """
    A simple car that has a name, a color, is automatic or manual and can be
    a convertible. In addition, it has a maximum speed, and can take the path
    to a file to represent the registration document. Optionally, the car
    can have a left-sided configuration for countries that drive on the other
    side of the road.
    """

    def __init__(self,
                 name,
                 color        = 'red',
                 automatic    = True,
                 convertible  = None,
                 max_speed    = 60,
                 registration = None,
                 sided        = 'right',
                 ):
        """
        Args:

            name: Lorem.

            color: Lorem.

            automatic: Determines if the car is automatic or not. This option
                       can be either 'True' or 'False'.

            convertible: Lorem.

            max_speed: Lorem.

            registration: Lorem.

            sided: The side of the road on which the car is supposed to drive.
                   Either 'left' or 'right'. No other options are supported.
                   By default 'right'.
        """
        # Save attributes #
        self.name         = name
        self.color        = color
        self.automatic    = automatic
        self.convertible  = convertible
        self.max_speed    = max_speed
        self.registration = registration
        self.sided        = sided
        # Assign default values and change others #
        self.transform()
        # Validate attributes #
        self.validate()

    def transform(self):
        """
        This method will replace empty attributes with defaults when this is
        needed and will convert others to proper types.
        """
        # The name should be lower-case #
        self.name = self.name.lower()
        # If we don't know it's convertible we assume it's not #
        if self.convertible is None:
            self.convertible = False
        # The speed should be an integer #
        self.max_speed = int(self.max_speed)

    def validate(self):
        """
        This method will raise an Exception if any of the arguments passed by
        the user are illegal.
        """
        # Check color #
        from matplotlib.colors import CSS4_COLORS as valid_colors
        if self.color not in valid_colors:
            msg = "The color '%s' is not a valid color name."
            raise Exception(msg % self.color)
        # Check the automatic #
        if self.automatic is not True and self.automatic is not False:
            msg = "The automatic property has to be True or False not '%s'."
            raise ValueError(msg % self.automatic)
        # Check the convertible #
        if self.convertible is not True and self.convertible is not False:
            msg = "The convertible property has to be True or False not '%s'."
            raise ValueError(msg % self.convertible)
        # Check the maximum speed #
        if not isinstance(self.max_speed, int):
            msg = "The maximum speed property has to be an integer not '%s'."
            raise ValueError(msg % self.max_speed)
        if self.max_speed < 0:
            raise ValueError("The maximum speed of the car cannot be negative.")
        # Check the registration #
        if self.registration is not None:
            if not os.path.exists(self.registration):
                msg = "The file located at '%s' does not exist."
                raise ValueError(msg % self.registration)
        # Check the side #
        if self.sided not in ['left', 'right']:
            msg = "The sideness of the car is not 'right' or 'left'."
            raise Exception(msg)

    def __repr__(self):
        return "<%s object '%s'>" % (self.__class__.__name__, self.name)

    def __str__(self):
        # Transmission #
        transmission = 'automatic' if self.automatic else 'manual'
        # First line #
        msg = f"This {transmission} {self.color} car is named {self.name}.\n"
        # Second line #
        msg +=  f"It can go up to {self.max_speed} km/h"
        if self.convertible: msg += " and is a convertible.\n"
        else:                msg += ".\n"
        # Third line #
        if self.registration:
            msg += f"The registration is available at '{self.registration}'.\n"
        # Fourth line #
        if self.sided == 'left':
            msg += "It drives on the left side of the road.\n"
        # Return #
        return msg

    def __call__(self, verbose=False):
        if verbose: print("The verbose mode is activated.")
        print(self)

###############################################################################
if __name__ == '__main__':
    car = Car('corvette')
    car(verbose=True)