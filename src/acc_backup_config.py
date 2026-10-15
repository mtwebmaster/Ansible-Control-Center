#!/usr/bin/env python3
"""
ACC Backup Configuration Reader

Reads and validates backup settings without starting
a backup or connecting to remote systems.
"""

import ipaddress
import os
import sys
from pathlib import Path

from acc_config import load_config, expand_path, ACCConfigError
from acc_ha_inventory import resolve_voters
from acc_cluster_policy import foundation_master


def settings():
    config = load_config()
    backup = config["backups"]

    required = (
        "directory",
        "ssh_key",
        "ssh_user",
        "remote_host",
        "mount_point",
    )

    for field in required:
        if not isinstance(backup.get(field), str) or not backup[field]:
            raise ACCConfigError(
                f"Missing required backup setting: {field}"
            )

    if backup["ssh_user"] != "microbackup":
        raise ACCConfigError(
            "Remote backup account must be microbackup"
        )

    from acc_ha_inventory import resolve_voters
    from acc_cluster_policy import cluster_master_addresses
    import json
    import subprocess

    masters = config["microk8s"]["masters"]
    selected = backup["remote_host"]

    if selected not in masters:
        raise ACCConfigError(
            "Backup host must be a configured HA master"
        )

    inventory_path = expand_path(config["inventory"])

    result = subprocess.run(
        ["ansible-inventory", "-i", inventory_path, "--list"],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )

    inventory = json.loads(result.stdout).get(
        "_meta", {}
    ).get("hostvars", {})

    # Validate the complete HA master address set.
    validated = cluster_master_addresses(config, inventory)

    address = inventory[selected]["ansible_host"]
    address = str(ipaddress.IPv4Address(address))

    if address not in validated:
        raise ACCConfigError(
            "Selected backup master failed cluster validation"
        )

    mount = Path(expand_path(backup["mount_point"])).resolve()
    directory = Path(expand_path(backup["directory"])).resolve()
    key = Path(expand_path(backup["ssh_key"])).resolve()

    if not mount.is_absolute() or str(mount) == "/":
        raise ACCConfigError("Unsafe backup mount point")

    if directory == mount or mount not in directory.parents:
        raise ACCConfigError(
            "Backup directory must be beneath its mount point"
        )

    return {
        "directory": str(directory),
        "ssh_key": str(key),
        "ssh_user": backup["ssh_user"],
        "host": str(ipaddress.IPv4Address(address)),
        "mount_point": str(mount),
    }


def main():
    values = settings()

    if len(sys.argv) != 2 or sys.argv[1] not in values:
        raise SystemExit("Usage: acc_backup_config.py FIELD")

    print(values[sys.argv[1]])


if __name__ == "__main__":
    try:
        main()
    except (ACCConfigError, ValueError, OSError) as exc:
        raise SystemExit(f"Backup configuration rejected: {exc}")
