#!/usr/bin/env python3
"""Pinventory.

A dynamic inventory provider for Ansible that finds fresh Raspberry Pis.

Usage:
    pinventory --list
    pinventory --host <hostname>

Options:
    -h --help  Show this screen.
    --version  Show version.
    --list     Output a JSON encoded dictionary of all groups.
    --host     Output a JSON encoded dictionary of variables for the specified host.

"""
import json
import sys
from docopt import docopt

from pinventory import __version__


def make_inventory():
    return {}


def collect_host_variables(hostname):
    _ = hostname
    return {}


def print_inventory():
    inventory = make_inventory()
    json_inventory = json.dumps(inventory)
    print(json_inventory)


def print_host_variables(hostname):
    host_variables = collect_host_variables(hostname)
    json_host_variables = json.dumps(host_variables)
    print(json_host_variables)

def main(argv=None):
    arguments = docopt(__doc__, argv, version=__version__)
    if arguments['--list']:
        print_inventory()
    elif arguments['--host']:
        print_host_variables(arguments['<hostname>'])

if __name__ == '__main__':
    sys.exit(main())