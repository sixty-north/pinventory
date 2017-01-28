def transform(inventory):
    """Transform an Ansible inventory object prior to JSON serialization.

    Args:
        inventory: A dictionary containing an Ansible inventory.
            The inventory contains per-host variables for 'ip_address',
            'hostname' and 'mac_address'.

    Returns:
        A dictionary containing an Ansible inventory.
    """
    return inventory


