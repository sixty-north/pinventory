#!/usr/bin/env python3
"""Pinventory.

A dynamic inventory provider for Ansible that finds fresh Raspberry Pi devices.

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
import socket
import sys

from docopt import docopt

from pinventory import __version__
from pinventory.network import arp_ip_mac, establish_routes

RASPBERRY_PI_MAC_ADDRESS_PREFIX = 'b8:27:eb:'


def locate_pi_devices():
    """Find all Raspberry Pi devices on the local network.

    Raspberry Pi computers are identified by the first three
    bytes of their MAC address.
    """
    establish_routes()
    pi_ip_hostnames = ip_hostnames_matching_mac_prefix(RASPBERRY_PI_MAC_ADDRESS_PREFIX)
    return pi_ip_hostnames


def ip_hostnames_matching_mac_prefix(mac_prefix):
    pi_ip_addresses = [ip for ip, mac in arp_ip_mac() if mac.startswith(mac_prefix)]
    ip_hostnames = []
    for pi_ip_address in pi_ip_addresses:
        hostaddr, _, _, = socket.gethostbyaddr(pi_ip_address)
        hostname, _, _ = hostaddr.partition('.')
        ip_hostnames.append((pi_ip_address, hostname))
    return ip_hostnames


def make_inventory():
    pi_ip_hostnames = locate_pi_devices()
    return dict(pi_ip_hostnames)


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