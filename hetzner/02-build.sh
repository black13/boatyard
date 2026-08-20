#!/bin/bash
# 02-build.sh — run ON the Hetzner box. Full Yocto build, detached.
set -e

sudo apt-get update -y
sudo apt-get install -y gawk wget git diffstat unzip gcc build-essential \
    chrpath cpio python3 python3-pip python3-pexpect xz-utils debianutils \
    python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev xterm python3-subunit \
    mesa-common-dev zstd liblz4-tool file locales
sudo locale-gen en_US.UTF-8

cd ~
git clone -b kirkstone git://git.yoctoproject.org/poky.git
git clone -b kirkstone git://git.openembedded.org/meta-openembedded
git clone -b kirkstone https://github.com/meta-qt5/meta-qt5.git
git clone https://github.com/black13/boatyard.git

cd ~/poky
source oe-init-build-env build

# layers
sed -i 's#^BBLAYERS.*#BBLAYERS ?= " \\\n  ${TOPDIR}/../meta \\\n  ${TOPDIR}/../meta-poky \\\n  ${TOPDIR}/../meta-yocto-bsp \\\n  ${TOPDIR}/../meta-openembedded/meta-oe \\\n  ${TOPDIR}/../meta-qt5 \\\n  ${TOPDIR}/../boatyard/meta-myproduct \\\n  "#' conf/bblayers.conf

# config
cat >> conf/local.conf <<'EOF'
MACHINE = "qemuarm64"
IMAGE_INSTALL:append = " qtbase qtdeclarative hello-ui hello"
DISTRO_FEATURES:append = " opengl wayland"
EOF

# start the build detached
nohup bitbake core-image-minimal > ~/build.log 2>&1 &
echo "build started — watch with:  tail -f ~/build.log"
