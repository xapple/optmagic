[![PyPI version](https://badge.fury.io/py/optmagic.svg)](https://badge.fury.io/py/optmagic)

# `optmagic` version 1.0.9

This project enables you to create simple command line interfaces starting
with a python class, or a python function that you want to expose directly to the shell.

It contains functionality which has not yet all been fully documented. Stay tuned.

## Similar projects

* [argparse](https://docs.python.org/3/library/argparse.html)
* [invoke](https://www.pyinvoke.org/)
* [click](https://click.palletsprojects.com/)
* [docopt](https://docopt.org/)

### Why not use one of those?

Ideally, the programmer should not have to specify anything extra than what the class or function already contains to expose its functionality. None of these other packages strive to accomplish that goal like `optmagic` does, as you can see in the following comparative examples.

    TODO

## Demo 

    TODO

## Installing

To install the `optmagic` package, simply type the following command on your terminal:

    $ pip3 install optmagic

## Dependencies

The project depends on the following module for parsing the docstrings automatically:

* `docstring_parser`

If you want to run the test suite for `optmagic` you will also need the following extra libraries:

* `pytest`
* `matplotlib`
* `pbs3`

## Extra documentation

More documentation is available at:

<http://xapple.github.io/optmagic/optmagic>

This documentation is simply generated with:

    $ pdoc3 --html --output-dir docs --force optmagic