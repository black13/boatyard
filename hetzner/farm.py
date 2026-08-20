#!/usr/bin/env python3
"""farm.py — Python controller for the one-day Hetzner build farm.

Usage (from boatyard/hetzner/):
    .venv/Scripts/python farm.py create    # provision the cx52 box
    .venv/Scripts/python farm.py status    # IP + cost + ssh command
    .venv/Scripts/python farm.py destroy   # tear down, billing stops

Requires a Hetzner API token in the env:
    set HCLOUD_TOKEN=<token>   (Windows)   or   export HCLOUD_TOKEN=<token>
"""

import os
import sys
import time

from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.locations.domain import Location

NAME = "boatyard-build"
SERVER_TYPE = "cx52"        # 16 vCPU / 32 GB / 360 GB — ~0.055 EUR/hr
IMAGE = "ubuntu-24.04"
LOCATION = "nbg1"


def client() -> Client:
    token = os.environ.get("HCLOUD_TOKEN")
    if not token:
        sys.exit("set HCLOUD_TOKEN to your Hetzner API token first")
    return Client(token=token)


def create(c: Client) -> None:
    if c.servers.get_by_name(NAME):
        print(f"server '{NAME}' already exists")
        return
    ssh_keys = [k.name for k in c.ssh_keys.get_all()]
    kwargs = {
        "name": NAME,
        "server_type": ServerType(SERVER_TYPE),
        "image": Image(name=IMAGE),
        "location": Location(LOCATION),
    }
    if ssh_keys:
        kwargs["ssh_keys"] = ssh_keys
    server = c.servers.create(**kwargs)
    action = server.action
    print(f"creating {NAME} ({SERVER_TYPE})...")
    while c.actions.get_by_id(action.id).status == "running":
        time.sleep(2)
    server.reload()
    print(f"ready: ssh root@{server.public_net.primary_ipv4.address}")
    print(f"price: ~0.055 EUR/hr — destroy when done: farm.py destroy")


def status(c: Client) -> None:
    s = c.servers.get_by_name(NAME)
    if not s:
        print("no server running")
        return
    s.reload()
    print(f"name:    {s.name}")
    print(f"status:  {s.status}")
    print(f"type:    {s.server_type.name}")
    print(f"ip:      {s.public_net.primary_ipv4.address}")
    print(f"ssh:     ssh root@{s.public_net.primary_ipv4.address}")
    print("build:   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/hetzner/02-build.sh | bash")
    print("cost:    ~0.055 EUR/hr while it lives")


def destroy(c: Client) -> None:
    s = c.servers.get_by_name(NAME)
    if not s:
        print("nothing to destroy")
        return
    s.delete()
    print(f"destroyed {NAME} — billing stopped")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    c = client()
    {"create": create, "status": status, "destroy": destroy}[cmd](c)
