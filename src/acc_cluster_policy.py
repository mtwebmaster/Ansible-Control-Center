#!/usr/bin/env python3
"""
Ansible Control Center — Cluster Role Resolution

Resolve explicitly configured HA masters from Ansible inventory.
No remote commands or cluster mutations are performed.
"""

from acc_config import load_config, masters, ACCConfigError
from acc_node_policy import validate_node_policy
import ipaddress


def cluster_master_addresses(config, inventory):
    """Return the validated IPv4 addresses of configured HA masters."""

    validate_node_policy(config, inventory)

    result = set()

    for hostname in masters(config):
        address = inventory[hostname]["ansible_host"]
        result.add(str(ipaddress.IPv4Address(address)))

    if len(result) != 3:
        raise ACCConfigError(
            "Exactly three distinct HA master addresses required"
        )

    return result


def foundation_master(config, inventory):
    """Return the first explicitly configured HA master."""

    validate_node_policy(config, inventory)

    names = list(masters(config))

    if len(names) != 3:
        raise ACCConfigError("Exactly three HA masters required")

    return names[0]
