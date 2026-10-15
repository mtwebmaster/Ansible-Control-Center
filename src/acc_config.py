#!/usr/bin/env python3
"""
Ansible Control Center (ACC)
Portable configuration loader.

Authors: Jeff Swenson and ChatGPT / OpenAI GPT-6
Version: 0.1.0

Loads and validates ACC configuration without modifying
the running system or performing network operations.
"""

import ipaddress
import json
import os
from pathlib import Path


class ACCConfigError(Exception):
    """Raised when ACC configuration is missing or invalid."""


DEFAULT_PATH = (
    Path.home()
    / ".config"
    / "ansible-control-center"
    / "config.json"
)


def load_config(path=None):
    """Load and validate ACC configuration."""

    config_path = Path(
        path
        or os.environ.get("ACC_CONFIG", DEFAULT_PATH)
    ).expanduser()

    if not config_path.is_file():
        raise ACCConfigError(
            f"ACC configuration not found: {config_path}"
        )

    try:
        data = json.loads(config_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ACCConfigError(
            f"Cannot read ACC configuration: {exc}"
        ) from exc

    validate_config(data)
    return data


def validate_config(data):
    """Validate required settings and enforce safe node roles."""

    if not isinstance(data, dict):
        raise ACCConfigError("Configuration must be an object")

    cluster = data.get("microk8s")

    if not isinstance(cluster, dict):
        raise ACCConfigError(
            "Missing microk8s configuration"
        )

    masters = cluster.get("masters")
    workers = cluster.get("workers")

    if not isinstance(masters, list) or len(masters) < 3:
        raise ACCConfigError(
            "At least three explicit master names are required"
        )

    if not isinstance(workers, list):
        raise ACCConfigError(
            "Worker list must be explicitly configured"
        )

    nodes = masters + workers

    if any(
        not isinstance(node, str) or not node.strip()
        for node in nodes
    ):
        raise ACCConfigError(
            "Node names must be nonempty strings"
        )

    if len(nodes) != len(set(nodes)):
        raise ACCConfigError(
            "Duplicate node names are not permitted"
        )

    if set(masters) & set(workers):
        raise ACCConfigError(
            "Masters and workers must be separate"
        )

    for key in ("dqlite_port", "api_port"):
        port = cluster.get(key)

        if (
            not isinstance(port, int)
            or isinstance(port, bool)
            or not 1 <= port <= 65535
        ):
            raise ACCConfigError(
                f"Invalid microk8s port: {key}"
            )

    for key in ("inventory", "ssh_key"):
        value = data.get(key)

        if not isinstance(value, str) or not value.strip():
            raise ACCConfigError(
                f"Missing or invalid setting: {key}"
            )

    return True


def expand_path(value):
    """Expand user-home and environment variables in paths."""
    return Path(
        os.path.expandvars(
            os.path.expanduser(value)
        )
    )


def masters(config):
    return tuple(config["microk8s"]["masters"])


def workers(config):
    return tuple(config["microk8s"]["workers"])


def is_master(config, hostname):
    return hostname in masters(config)


def is_worker(config, hostname):
    return hostname in workers(config)


def require_worker(config, hostname):
    """Reject operations targeting unknown or master nodes."""
    if not is_worker(config, hostname):
        raise ACCConfigError(
            f"Host '{hostname}' is not an authorized worker"
        )


def require_master(config, hostname):
    if not is_master(config, hostname):
        raise ACCConfigError(
            f"Host '{hostname}' is not an authorized master"
        )
