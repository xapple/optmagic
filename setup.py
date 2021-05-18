from setuptools import setup, find_namespace_packages

setup(
    name             = 'optmagic',
    version          = '1.0.1',
    description      = 'Automatically make a command line interface from a '
                       'class or function.',
    license          = 'MIT',
    url              = 'http://github.com/xapple/optmagic/',
    author           = 'Lucas Sinclair',
    author_email     = 'lucas.sinclair@me.com',
    packages         = find_namespace_packages(),
    install_requires = ['docstring_parser'],
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    include_package_data = True,
)
