#!/bin/bash
# boatyard build — runs bitbake, detached, log at ~/build.log.
# Optional argument = MACHINE (default qemuarm64).
#   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/build.sh | bash
#   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/build.sh | bash -s beaglebone-yocto
#   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/build.sh | bash -s genericx86-64
set -e

MACHINE_TARGET="${1:-qemuarm64}"

cd ~/yocto/poky
source oe-init-build-env build
touch conf/sanity.conf

sed -i "s/^MACHINE = .*/MACHINE = \"$MACHINE_TARGET\"/" conf/local.conf

echo "starting bitbake core-image-minimal for $MACHINE_TARGET (detached, log ~/build.log)..."
nohup nice -n 10 bitbake core-image-minimal > ~/build.log 2>&1 &

echo
echo "build is running. Live view:  tail -f ~/build.log"
echo "(ctrl-c stops the VIEW, not the build)"
echo
echo "When you see 'Tasks Summary' near the end of the log, it's done."
echo "Image lands in: ~/yocto/poky/build/tmp/deploy/images/$MACHINE_TARGET/"
