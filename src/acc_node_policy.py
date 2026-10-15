#!/usr/bin/env python3
"""
Ansible Control Center — Node Authorization Policy

Authors: Jeff Swenson and ChatGPT / OpenAI GPT-6
Version: 0.1.0

Purpose:
    Enforce explicit node-role authorization for ACC operations.

    Unknown hosts and control-plane nodes must not be
    treated as workers.

    This module performs no remote operations.
"""

import ipaddress

from acc_config import ACCConfigError, masters, workers


def validate_node_policy(config, inventory_hosts):
    """Validate configured roles against inventory membership."""

    if not isinstance(inventory_hosts, dict):
        raise ACCConfigError("Inventory hosts must be a dictionary")

    master_names = set(masters(config))
    worker_names = set(workers(config))

    if len(master_names) != 3:
        raise ACCConfigError(
            "Exactly three HA masters must be configured"
        )

    if not worker_names:
        raise ACCConfigError(
            "At least one worker must be explicitly configured"
        )

    if master_names & worker_names:
        raise ACCConfigError(
            "Master and worker roles overlap"
        )

    expected = master_names | worker_names
    missing = expected - set(inventory_hosts)

    if missing:
        raise ACCConfigError(
            "Configured hosts missing from inventory: "
            + ", ".join(sorted(missing))
        )

    addresses = {}

    for hostname in expected:
        details = inventory_hosts[hostname]

        if not isinstance(details, dict):
            raise ACCConfigError(
                f"Invalid inventory entry: {hostname}"
            )

        address = details.get("ansible_host")

        if not isinstance(address, str) or not address:
            raise ACCConfigError(
                f"Missing explicit host address: {hostname}"
            )

        try:
            parsed = ipaddress.IPv4Address(address)
        except ipaddress.AddressValueError as exc:
            raise ACCConfigError(
                f"Invalid IPv4 address for host: {hostname}"
            ) from exc

        if (
            parsed.is_unspecified
            or parsed.is_loopback
            or parsed.is_multicast
        ):
            raise ACCConfigError(
                f"Unusable IPv4 address for host: {hostname}"
            )

        normalized = str(parsed)

        if normalized in addresses:
            raise ACCConfigError(
                "Duplicate managed-node addresses are forbidden"
            )

        addresses[normalized] = hostname

    return True


def authorize_worker(config, inventory_hosts, hostname):
    """Authorize worker operations; deny unknown/master hosts."""

    validate_node_policy(config, inventory_hosts)

    if hostname not in workers(config):
        raise ACCConfigError(
            f"Worker operation denied for host: {hostname}"
        )

    return True


def authorize_master_readonly(config, inventory_hosts, hostname):
    """Authorize read-only queries against configured HA masters."""

    validate_node_policy(config, inventory_hosts)

    if hostname not in masters(config):
        raise ACCConfigError(
            f"Master query denied for host: {hostname}"
        )

    return True
