#!/bin/bash
# boatyard build — runs bitbake, detached, log at ~/build.log.
#   bash build.sh [MACHINE] [IMAGE]
# defaults: qemuarm64 / core-image-minimal
#
# The graphical demo (weston + Qt5 QML):
#   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/build.sh | bash -s qemux86-64 boatyard-demo-image
#
# Other targets:
#   bash -s beaglebone-yocto            # BeagleBone Black
#   bash -s genericx86-64               # old PCs / laptops
set -e

MACHINE_TARGET="${1:-qemuarm64}"
IMAGE_TARGET="${2:-core-image-minimal}"

cd ~/yocto/poky
source oe-init-build-env build
touch conf/sanity.conf

sed -i "s/^MACHINE = .*/MACHINE = \"$MACHINE_TARGET\"/" conf/local.conf

echo "starting bitbake $IMAGE_TARGET for $MACHINE_TARGET (detached, log ~/build.log)..."
nohup nice -n 10 bitbake "$IMAGE_TARGET" > ~/build.log 2>&1 &

echo
echo "build is running. Live view:  tail -f ~/build.log"
echo "(ctrl-c stops the VIEW, not the build)"
echo
echo "When you see 'Tasks Summary' near the end of the log, it's done."
echo "Image lands in: ~/yocto/poky/build/tmp/deploy/images/$MACHINE_TARGET/"
