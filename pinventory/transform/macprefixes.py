def transform(mac_prefixes):
    """Transform an collections of MAC addresses prefixes which will be checked..

    This transform is the identity function, and is provided as an example.

    Args:
        mac_prefixes: A set of MAC addresses prefixes.

    Returns:
        A set of MAC addresses prefixes.
    """
    
    # # Example: Remove the official Rasperry Pi Foundation MAC address prefix
    #
    # from pinventory.inventory import RASPBERRY_PI_MAC_ADDRESS_PREFIX
    # mac_prefixes.discard(RASPBERRY_PI_MAC_ADDRESS_PREFIX)

    return mac_prefixes
