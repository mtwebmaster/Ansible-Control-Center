"""
ACC v6.0.1 — Secure Kubernetes API Authentication Test
Authors: Jeff Swenson; ChatGPT Pro / OpenAI GPT-6
Requirements: Python 3, OpenSSH, existing Kubernetes CA
Logging: Console results only; credentials are never logged
Version: 6.0.1
"""
import json
import pathlib
import subprocess
import ssl
import urllib.request
import urllib.error
import sys


from acc_config import load_config, expand_path
from acc_cluster_policy import cluster_master_addresses
import subprocess as _subprocess

CONFIG = load_config()

_inventory_result = _subprocess.run(
    [
        "ansible-inventory",
        "-i",
        expand_path(CONFIG["inventory"]),
        "--list",
    ],
    capture_output=True,
    text=True,
    check=True,
    timeout=30,
)

_inventory = json.loads(_inventory_result.stdout)["_meta"]["hostvars"]

_masters = CONFIG["microk8s"]["masters"]
_selected_master = _masters[0]

cluster_master_addresses(CONFIG, _inventory)

MASTER_IP = _inventory[_selected_master]["ansible_host"]
SSH_USER = CONFIG["management_user"]


HOME = pathlib.Path.home()
CA = HOME / ".config/ansible-control-center/certs/kubernetes-ca.crt"
KEY = pathlib.Path(expand_path(CONFIG["ssh_key"]))
API = f"https://{MASTER_IP}:{CONFIG['microk8s']['api_port']}"

try:
    print("=== REQUESTING SHORT-LIVED TOKEN ===")

    result = subprocess.run([
        "ssh", "-T",
        "-i", str(KEY),
        "-o", "IdentitiesOnly=yes",
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=yes",
        f"{SSH_USER}@{MASTER_IP}",
        "microk8s kubectl -n acc-monitoring create token acc-k8s-monitor --duration=10m"
    ], capture_output=True, text=True, timeout=30, check=True)

    token = result.stdout.strip()
    if not token or len(token) < 50:
        raise RuntimeError("Token request returned invalid data")

    print("Token request: PASS")

    context = ssl.create_default_context(cafile=str(CA))

    def api_request(path):
        req = urllib.request.Request(
            API + path,
            headers={"Authorization": "Bearer " + token}
        )
        try:
            with urllib.request.urlopen(req, context=context, timeout=10) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            return e.code, None

    print("\n=== KUBERNETES NODE ACCESS ===")
    status, data = api_request("/api/v1/nodes")
    print("HTTP status:", status)
    if status != 200:
        raise RuntimeError("Node API access failed")
    print("Nodes:", len(data.get("items", [])))

    print("\n=== KUBERNETES POD ACCESS ===")
    status, data = api_request("/api/v1/pods")
    print("HTTP status:", status)
    if status != 200:
        raise RuntimeError("Pod API access failed")
    print("Pods:", len(data.get("items", [])))

    print("\n=== SECRETS ACCESS RESTRICTION ===")
    status, _ = api_request("/api/v1/secrets")
    print("HTTP status:", status)
    if status != 403:
        raise RuntimeError("Secrets access restriction failed")

    print("\nACC KUBERNETES API TEST: PASS")

except Exception as exc:
    print("ACC KUBERNETES API TEST: FAILED")
    print("Error type:", type(exc).__name__)
    sys.exit(1)
