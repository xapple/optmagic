#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to test the functionality of the `optmagic` module.

This script should be executable (chmod +x) so that it can be called from the
shell directly.

Written by Lucas Sinclair.
MIT Licensed.
Contact at www.sinclair.bio

Call it like this:

    $ ./expose_class.py corvette --max_speed=130
"""

# Module #
from optmagic.optmagic import OptMagic

# Test class (or could be a function) #
from simple_class import Car

# Apply magic #
if __name__ == '__main__':
    OptMagic(Car)()
