import sys
import socket
import ipaddress
import subprocess


_local_networks = ("127.", "0:0:0:0:0:0:0:1")

# ignore these prefixes -- localhost, unspecified, and link-local
_ignored_networks = _local_networks + ("0.", "0:0:0:0:0:0:0:0", "169.254.", "fe80:")


def detect_family(addr):
    if "." in addr:
        assert ":" not in addr
        return socket.AF_INET
    elif ":" in addr:
        return socket.AF_INET6
    else:
        raise ValueError("invalid ipv4/6 address: %r" % addr)


def expand_addr(addr):
    """convert address into canonical expanded form --
    no leading zeroes in groups, and for ipv6: lowercase hex, no collapsed groups.
    """
    family = detect_family(addr)
    addr = socket.inet_ntop(family, socket.inet_pton(family, addr))
    if "::" in addr:
        count = 8-addr.count(":")
        addr = addr.replace("::", (":0" * count) + ":")
        if addr.startswith(":"):
            addr = "0" + addr
    return addr


def _get_local_addr(family, remote):
    try:
        s = socket.socket(family, socket.SOCK_DGRAM)
        try:
            s.connect((remote, 9))
            return s.getsockname()[0]
        finally:
            s.close()
    except socket.error:
        return None


def get_local_addr(remote=None, ipv6=True):
    """Get primary LAN address of host

    Args:
        remote: If supplied, return LAN address that host would use
            to access that specific remote address. By default,
            returns address it would use to access the public
            internet.

        ipv6: Attempt to find an ipv6 address first if True,
            otherwise only check ipv4.

    Returns:
        Primary LAN address for host, or None if could not be
        determined.
    """
    if remote:
        family = detect_family(remote)
        local = _get_local_addr(family, remote)
        if not local:
            return None
        if family == socket.AF_INET6:
            # expand zero groups so the startswith() test works.
            local = expand_addr(local)
        if local.startswith(_local_networks):
            # border case where remote addr belongs to host
            return local
    else:
        # NOTE: the two addresses used here are TESTNET addresses,
        #       which should never exist in the real world.
        if ipv6:
            local = _get_local_addr(socket.AF_INET6, "2001:db8::1234")
            # expand zero groups so the startswith() test works.
            if local:
                local = expand_addr(local)
        else:
            local = None
        if not local:
            local = _get_local_addr(socket.AF_INET, "192.0.2.123")
            if not local:
                return None
    if local.startswith(_ignored_networks):
        return None
    return local


def local_ip_address(remote=None, ipv6=True):
    addr = get_local_addr(remote, ipv6)
    if addr is None:
        return None
    return ipaddress.ip_address(addr)


def local_netmask(local_ip_address):
    a = subprocess.check_output("ifconfig", shell=True).decode(sys.getdefaultencoding())
    matches = filter(lambda line: line.startswith("inet " + str(local_ip_address)),
                   map(str.strip, a.splitlines()))
    try:
        match = next(matches)
    except StopIteration:
        raise RuntimeError("Could not locate network corresponding to {}".format(local_ip_address))

    _, _, suffix = match.partition('netmask')
    netmask_hex = suffix.split()[0]
    netmask_int = int(netmask_hex, base=0)
    netmask_address = ipaddress.ip_address(netmask_int)
    return str(netmask_address)


def make_network(ip_address, netmask):
    ip_address = ipaddress.ip_address(ip_address)
    netmask = ipaddress.ip_address(netmask)
    network_address = ipaddress.ip_address(int(ip_address) & int(netmask))
    return ipaddress.ip_network('/'.join((str(network_address), str(netmask))))


def local_network(remote=None, ipv6=True):
    ip_address = local_ip_address(remote, ipv6)
    netmask = local_netmask(ip_address)
    return make_network(ip_address, netmask)


def arp_ip_mac():
    a = subprocess.check_output("arp -an", shell=True).decode(sys.getdefaultencoding())
    for line in a.splitlines():
        words = line.split()
        maybe_ip_address = [word[1:-1] for word in words if word.count('.') == 3]
        maybe_mac_address = [word for word in words if word.count(':') == 5]
        if maybe_ip_address and maybe_mac_address:
            yield maybe_ip_address[0], maybe_mac_address[0]


def establish_routes():
    """Establish routes to all devices on the local network using nmap.

    This is useful so that subsequent calls to arp_ip_mac() discover all devices.
    """
    network = local_network()
    nmap_command = 'nmap -sP {!s}'.format(network)
    subprocess.check_call(nmap_command, shell=True, stdout=subprocess.DEVNULL)