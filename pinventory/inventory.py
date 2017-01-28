#!/usr/bin/env python3
"""Pinventory.

An Ansible dynamic inventory provider that finds Raspberry Pi devices.

Usage:
    pinventory --list [--pretty]
    pinventory --host <hostname> [--pretty]
    pinventory --help
    pinventory --version

Options:
    -h --help  Show this screen.
    --version  Show version.
    --list     Show a JSON object of all groups.
    --host     Show a JSON object of variables for the specified host.
    --pretty   Pretty-print JSON output.

"""
import json
import socket
import sys
from functools import reduce

import pkg_resources
from docopt import docopt

from pinventory import __version__
from pinventory.network import arp_ip_mac, establish_routes

RASPBERRY_PI_MAC_ADDRESS_PREFIX = 'b8:27:eb:'
DEFAULT_JSON_INDENTATION = 4

def locate_pi_devices():
    """Find all Raspberry Pi devices on the local network.

    Raspberry Pi computers are identified by the first three
    bytes of their MAC address.
    """
    establish_routes()
    pi_ip_hostname_macs = ip_hostname_macs_matching_mac_prefix(RASPBERRY_PI_MAC_ADDRESS_PREFIX)
    return pi_ip_hostname_macs


def ip_hostname_macs_matching_mac_prefix(mac_prefix):
    pi_ip_mac_addresses = [(ip, mac) for ip, mac in arp_ip_mac() if mac.startswith(mac_prefix)]
    ip_hostname_macs = []
    for pi_ip_address, pi_mac_address in pi_ip_mac_addresses:
        hostaddr, _, _, = socket.gethostbyaddr(pi_ip_address)
        hostname, _, _ = hostaddr.partition('.')
        ip_hostname_macs.append((pi_ip_address, hostname, pi_mac_address))
    return ip_hostname_macs


def make_inventory():
    ip_hostname_macs = locate_pi_devices()
    all_raspberry_group = set(ip for ip, hostname, mac in ip_hostname_macs)
    hostsvars = make_hostsvars(ip_hostname_macs)
    inventory = {
        'raspberries': {
            'hosts': sorted(all_raspberry_group),
        },
        '_meta': {
            'hostvars': hostsvars
        }
    }

    group = 'pinventory.transform.inventory'
    transformers = (entry_point.load() for entry_point in pkg_resources.iter_entry_points(group=group))
    return reduce(lambda a, f: f(a), transformers, inventory)


def make_hostsvars(ip_hostname_macs):
    hostsvars = {ip: {'ip': ip,
                      'hostname': hostname,
                      'mac': mac} for ip, hostname, mac in ip_hostname_macs}

    group = 'pinventory.transform.hostsvars'
    transformers = (entry_point.load() for entry_point in pkg_resources.iter_entry_points(group=group))
    return reduce(lambda a, f: f(a), transformers, hostsvars)


def collect_host_variables(hostname):
    ip_hostname_macs = locate_pi_devices()
    hostsvars = make_hostsvars(ip_hostname_macs)
    try:
        hostvars = hostsvars[hostname]
    except KeyError:
        hostvars = {}
    return hostvars


def print_inventory(indent=None):
    inventory = make_inventory()
    json_inventory = json.dumps(inventory, indent=indent, sort_keys=True)
    print(json_inventory)


def print_host_variables(hostname, indent=None):
    host_variables = collect_host_variables(hostname)
    json_host_variables = json.dumps(host_variables, indent=indent, sort_keys=True)
    print(json_host_variables)


def main(argv=None):
    arguments = docopt(__doc__, argv, version=__version__)
    indent = DEFAULT_JSON_INDENTATION if arguments['--pretty'] else None
    if arguments['--list']:
        print_inventory(indent=indent)
    elif arguments['--host']:
        print_host_variables(arguments['<hostname>'], indent=indent)

if __name__ == '__main__':
    sys.exit(main())


