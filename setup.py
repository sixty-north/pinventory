"""A setuptools based setup module for Pinventory.
"""
import os
import sys

MINIMUM_VERSION = (3, 4, 0)

if sys.version_info < MINIMUM_VERSION:
    sys.stderr.write("At least Python {} is required for this package. You are running with Python {}\n"
          .format(
            '.'.join(map(str, MINIMUM_VERSION)),
            '.'.join(map(str, sys.version_info))))
    sys.exit(os.EX_CONFIG)

import io
import re

from codecs import open

from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

here = os.path.abspath(os.path.dirname(__file__))


# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pinventory',

    version=find_version("pinventory/__init__.py"),

    description='An Ansible dynamic inventory for locating and categorising Raspberry Pis on the LAN.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/sixty-north/pinventory',

    # Author details
    author='Sixty North AS',
    author_email='rob@sixty-north.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'License :: Other/Proprietary License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.,
        'Programming Language :: Python :: 3.6',
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'test*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'docopt'
    ],

    # The order of these is important!
    tests_require=[
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pinventory=pinventory.inventory:main',
        ],
        'pinventory.transform.inventory': [
            'transform=pinventory.transform.inventory:transform'
        ],
        'pinventory.transform.hostsvars': [
            'transform=pinventory.transform.hostsvars:transform'
        ]
    },
)