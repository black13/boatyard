#!/bin/bash
# boatyard boot-test — boots the image we just built, in QEMU on this box.
# You watch the boot log; the agent tails the same log.
# Run on the vast box:   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/boot-test.sh | bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "=== [1/2] install qemu (host) ==="
apt-get update -y -q
apt-get install -y -q qemu-system-arm

echo "=== [2/2] boot core-image-minimal-qemuarm64 (detached, log ~/boot.log) ==="
cd ~/yocto/poky
source oe-init-build-env build

nohup runqemu qemuarm64 nographic slirp > ~/boot.log 2>&1 &

echo
echo "booting. Live view:  tail -f ~/boot.log"
echo "(ctrl-c stops the VIEW, not the VM)"
echo
echo "Watch for: kernel messages -> systemd/busybox init -> login prompt."
echo "TCG emulation on this box takes 2-5 minutes to reach login."
