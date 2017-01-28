def transform(inventory):
    """Transform an Ansible inventory object prior to JSON serialization.

    This transform is the identity function, and is provided as an example.

    Args:
        inventory: A dictionary containing an Ansible inventory.
            The inventory contains per-host variables for 'ip_address',
            'hostname' and 'mac_address'.

    Returns:
        A dictionary containing an Ansible inventory.
    """
    # # Example: Create two new groups called raw-raspberries and taken-raspberries.
    # #          The first group contains all hosts which which are called
    # #          'raspberrypi', the second group contains the remaining Raspberry Pi
    # #          computers.
    #
    # all_raspberry_hosts = set(inventory['raspberries']['hosts'])
    # raw_raspberry_hosts = set(host for host, hostvars in inventory['_meta']['hostvars'].items()
    #                           if hostvars['hostname'].startswith('raspberrypi'))
    # taken_raspberry_hosts = all_raspberry_hosts - raw_raspberry_hosts
    # inventory['raw-raspberries'] = {'hosts': sorted(raw_raspberry_hosts)}
    # inventory['taken-raspberries'] = {'hosts': sorted(taken_raspberry_hosts)}
    return inventory
