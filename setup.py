"""\
"""
from distribute_setup import use_setuptools
use_setuptools()

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = ['']

setup(
    name='python-bitcoinaddress',
    version='0.2.2',
    description="Python bitcoin address validation",
    long_description=read('README.md'),
    license="GPLv3",
    author="Robert-Reinder Nederhoed",
    author_email="r.r.nederhoed@gmail.com",
    url='https://github.com/nederhoed/python-bitcoinaddress',
    keywords='bitcoin address validation',
    packages=find_packages(),
    test_suite="tests",
    install_requires=requires,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)
