#!/bin/bash
# 03-destroy.sh — tear down the farm. Run when the build is done.
set -e

# if run FROM the box itself, this is a no-op reminder; run it on YOUR machine
if [ -f /etc/hetzner ]; then
    echo "Run this on your local machine, not the server."
    exit 1
fi

hcloud server delete boatyard-build
echo "farm destroyed — billing stopped"
