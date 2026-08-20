#!/bin/bash
# boatyard build — runs bitbake, detached, log at ~/build.log.
# Run on the vast box:   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/build.sh | bash
set -e

cd ~/yocto/poky
source oe-init-build-env build
touch conf/sanity.conf

echo "starting bitbake (detached, log ~/build.log)..."
nohup nice -n 10 bitbake core-image-minimal > ~/build.log 2>&1 &

echo
echo "build is running. Live view:  tail -f ~/build.log"
echo "(ctrl-c stops the VIEW, not the build)"
echo
echo "When you see 'Tasks Summary' near the end of the log, it's done."
