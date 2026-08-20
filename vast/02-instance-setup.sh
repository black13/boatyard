#!/bin/bash
# Step 2 — prepare the build environment on the shared box.
# Safe to run: apt packages + clones only, nothing destructive.
set -e

export DEBIAN_FRONTEND=noninteractive

apt-get update -y -q
apt-get install -y -q gawk wget git diffstat unzip gcc build-essential \
    chrpath cpio python3 python3-pip python3-pexpect xz-utils debianutils \
    python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev xterm python3-subunit \
    mesa-common-dev zstd liblz4-tool file locales
locale-gen en_US.UTF-8

mkdir -p ~/yocto && cd ~/yocto

[ -d poky ] || git clone -q -b kirkstone git://git.yoctoproject.org/poky.git
[ -d meta-openembedded ] || git clone -q -b kirkstone git://git.openembedded.org/meta-openembedded
[ -d meta-qt5 ] || git clone -q -b kirkstone https://github.com/meta-qt5/meta-qt5.git
[ -d boatyard ] || git clone -q https://github.com/black13/boatyard.git

echo "setup complete — now run step 3:"
echo "  curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/03-build.sh | bash"
