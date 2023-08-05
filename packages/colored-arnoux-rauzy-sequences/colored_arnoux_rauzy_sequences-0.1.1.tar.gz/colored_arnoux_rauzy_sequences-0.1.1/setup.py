## -*- encoding: utf-8 -*-
import os
import sys
from setuptools import setup
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests


# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib colored_arnoux_rauzy_sequences")
        if errno != 0:
            sys.exit(1)

setup(
    name = "colored_arnoux_rauzy_sequences",
    version = readfile("VERSION").strip(), # the VERSION file is shared with the documentation
    description='Colored Arnoux-Rauzy sequences and their asymptotic critical exponent',
    long_description = readfile("README.rst"), # get the long description from the README
    long_description_content_type='text/x-rst',
    url='https://gitub.u-bordeaux.fr/jlepsova/colored_arnoux_rauzy_sequences',
    author='Jana Lepsova',
    author_email='lepsova.jana@gmail.com', # choose a main contact email
    license='GPLv2+', # This should be consistent with the LICENCE file
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'Topic :: Software Development :: Build Tools',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
      'Programming Language :: Python :: 3.8',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = "SageMath Arnoux-Rauzy Words Critical exponent",
    packages = ['colored_arnoux_rauzy_sequences'],
    install_requires = ['sage-package', 'sphinx'],
    setup_requires = ['sage-package'],
    cmdclass = {'test': SageTest} # adding a special setup command for tests
)
