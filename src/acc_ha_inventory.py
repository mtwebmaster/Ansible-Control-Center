#!/usr/bin/env python3
"""
Ansible Control Center — Portable HA inventory resolver

Authors: Jeff Swenson and ChatGPT / OpenAI GPT-6
Version: 0.1.0

Resolves HA voters from explicitly configured master names.
No Kubernetes or cluster state changes are performed.
"""

import ipaddress
import json
import subprocess

from acc_config import ACCConfigError, expand_path, masters


def resolve_voters(config, inventory_data=None):
    """
    Return {master_name: 'IPv4:port'}.

    Reject missing, duplicate, or invalid master addresses.
    """

    names = masters(config)

    if len(names) != 3 or len(set(names)) != 3:
        raise ACCConfigError(
            "Exactly three distinct HA masters are required"
        )

    if inventory_data is None:
        inventory = expand_path(config["inventory"])

        result = subprocess.run(
            ["ansible-inventory", "-i", str(inventory), "--list"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        if result.returncode != 0:
            raise ACCConfigError(
                "Unable to resolve Ansible inventory"
            )

        try:
            inventory_data = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise ACCConfigError(
                "Invalid Ansible inventory output"
            ) from exc

    if not isinstance(inventory_data, dict):
        raise ACCConfigError("Invalid inventory data")

    hostvars = inventory_data.get("_meta", {}).get("hostvars", {})

    if not isinstance(hostvars, dict):
        raise ACCConfigError("Missing inventory host variables")

    port = config["microk8s"]["dqlite_port"]
    result = {}
    seen_addresses = set()

    for name in names:
        if name not in hostvars:
            raise ACCConfigError(
                f"Required master absent from inventory: {name}"
            )

        variables = hostvars[name]

        if not isinstance(variables, dict):
            raise ACCConfigError(
                f"Invalid inventory entry: {name}"
            )

        address = variables.get("ansible_host")

        if not isinstance(address, str):
            raise ACCConfigError(
                f"Missing explicit address for master: {name}"
            )

        try:
            parsed = ipaddress.IPv4Address(address)
        except ipaddress.AddressValueError as exc:
            raise ACCConfigError(
                f"Invalid IPv4 address for master: {name}"
            ) from exc

        if parsed.is_unspecified or parsed.is_multicast or parsed.is_loopback:
            raise ACCConfigError(
                f"Unusable master address: {name}"
            )

        if str(parsed) in seen_addresses:
            raise ACCConfigError(
                "Duplicate HA master addresses are not permitted"
            )

        seen_addresses.add(str(parsed))
        result[name] = f"{parsed}:{port}"

    return result
