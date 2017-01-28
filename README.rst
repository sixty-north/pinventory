==========
Pinventory
==========

*Pinventory* is an Ansible Dynamic Inventory for locating and
categorising Raspberry Pi computers on the local network.

Installation
============

In the Python environment which you are using::

  $ python setup.py install

A wrapper script called simply ``pinventory`` will be installed
which can be used to invoke the Python package.

Direct usage
============

To obtain an Ansible inventory of Raspberry Pi computers on the
LAN::

  $ pinventory --list --pretty
  {
      "_meta": {
          "hostvars": {
              "10.0.0.149": {
                  "hostname": "lime",
                  "ip": "10.0.0.149",
                  "mac": "b8:27:eb:a5:93:c5"
              },
              "10.0.0.186": {
                  "hostname": "raspberrypi",
                  "ip": "10.0.0.186",
                  "mac": "b8:27:eb:73:9d:67"
              }
          }
      },
      "raspberries": {
          "hosts": [
              "10.0.0.149",
              "10.0.0.186"
          ]
      }
  }

To obtain the host variables for a particular host::

    $ pinventory --host 10.0.0.149 --pretty
    {
        "hostname": "lime",
        "ip": "10.0.0.149",
        "mac": "b8:27:eb:a5:93:c5"
    }


Invocation from Ansible
=======================

Pass the ``pinventory`` executable using the ``-i`` inventory option, and
Ansible will execute it as a *dynamic inventory*.  For example, assuming
``pinventory`` is available on the PATH, to run an ad hoc Ansible command
on all Raspberry Pi devices on the LAN, use::

  $ ansible raspberries -i `which pinventory` <command>

Customisation
=============

By default the returned inventory includes *all* Raspberry Pi
computers on the local network. The contents of the inventory
and variables associated with each host can be customised by
providing pluggable functions at two ``pkg_resources`` entry
points capable of transforming the default inventory and
host variables respectively. Example functions can be found
in the ``pinventory.transforms.hostsvars`` and
``pinventory.transforms.inventory`` sub-modules.

