#!/usr/bin/env python3
"""
ACC v6.2 — MicroK8s HA Membership Checker

Authors: Jeff Swenson and ChatGPT Pro / OpenAI GPT-6
Version: 0.1.0
Purpose: Read-only comparison of reported MicroK8s HA voter membership.
Requirements: Python 3, Ansible, existing inventory and SSH key.
Usage: python3 ha-membership-check.py

Changelog:
  0.1.0 - Initial three-master membership verification.
Logging: Console only. No passwords or tokens are saved.
"""

import re
import subprocess
import sys
from pathlib import Path

from acc_config import load_config, expand_path, ACCConfigError
from acc_ha_inventory import resolve_voters

CONFIG = load_config()
INV = expand_path(CONFIG["inventory"])
KEY = expand_path(CONFIG["ssh_key"])
EXPECTED = resolve_voters(CONFIG)

def parse_status(output):
    """Extract running state, HA state and voter membership."""
    running = False
    enabled = False
    voters = set()
    section = None
    address = None

    for line in output.splitlines():
        stripped = line.strip()

        if line == "microk8s:":
            section = "microk8s"
            continue

        if line == "high-availability:":
            section = "ha"
            continue

        if line and not line.startswith(" "):
            section = None

        if section == "microk8s":
            if stripped == "running: True":
                running = True

        elif section == "ha":
            if stripped == "enabled: True":
                enabled = True
            elif stripped.startswith("- address:"):
                address = stripped.split(":", 1)[1].strip()
            elif stripped == "role: voter" and address:
                voters.add(address)
                address = None

    return running, enabled, voters


def query_all_masters():
    """Query three MicroK8s masters with one interactive Ansible execution."""
    command = [
        "ansible",
        ",".join(EXPECTED),
        "-i", str(INV),
        "--private-key", str(KEY),
        "-b",
        "-K",
        "-m", "ansible.builtin.command",
        "-a", "microk8s status --format yaml",
    ]

    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
        stdin=sys.stdin,
    )

    # Parse explicit per-host Ansible result headers.
    # Never treat an absent host as successfully queried.
    host_pattern = "|".join(map(re.escape, EXPECTED))
    headers = list(re.finditer(
        rf"^({host_pattern}) \| "
        r"(SUCCESS|CHANGED|FAILED|UNREACHABLE)"
        r"(?: \| rc=(-?\d+))? >>.*$",
        result.stdout,
        re.MULTILINE,
    ))

    reports = {}

    for index, match in enumerate(headers):
        host = match.group(1)
        state = match.group(2)
        rc = match.group(3)

        end = (
            headers[index + 1].start()
            if index + 1 < len(headers)
            else len(result.stdout)
        )

        body = result.stdout[match.end():end]

        if state not in ("SUCCESS", "CHANGED") or rc != "0":
            reports[host] = None
            continue

        reports[host] = parse_status(body)

    if result.returncode != 0:
        print(
            "WARNING: Ansible batch failed (exit "
            + str(result.returncode) + "). Verification unavailable.",
            file=sys.stderr,
        )
        return {}

    return reports




def main():
    expected_voters = set(EXPECTED.values())

    print("ACC v6.2 — MICROK8S HA MEMBERSHIP CHECK")
    print("Expected voters:", len(expected_voters))
    print("Querying all three masters through one Ansible invocation.")
    print()

    try:
        reports = query_all_masters()
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("UNAVAILABLE: Ansible HA query failed:", exc)
        return 1

    successful = 0

    for host in EXPECTED:
        report = reports.get(host)

        if report is None:
            print(f"{host}: UNAVAILABLE or query failed")
            continue

        running, enabled, voters = report

        print(f"{host}:")
        print("  MicroK8s running:", running)
        print("  HA enabled:", enabled)
        print("  Voters:", sorted(voters))

        if running and enabled and voters == expected_voters:
            print("  RESULT: PASS")
            successful += 1
        else:
            print("  RESULT: FAIL — Membership or status mismatch")

    print()
    print(f"MEMBERSHIP AGREEMENT: {successful}/3 masters")

    if successful == 3:
        print("PASS: All masters report identical expected membership")
        print("LIVE DQLITE CONSENSUS: NOT INDEPENDENTLY VERIFIED")
        return 0

    print("WARNING: HA membership could not be fully verified")
    print("LIVE DQLITE CONSENSUS: UNKNOWN")
    return 1




if __name__ == "__main__":
    sys.exit(main())
