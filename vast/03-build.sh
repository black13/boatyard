#!/bin/bash
# Step 3 — the build, tuned for the shared box.
# Runs detached, tees to ~/build.log so both of us can tail it.
set -e

cd ~/yocto/poky
source oe-init-build-env build

cat > conf/bblayers.conf <<'EOF'
POKY_BBLAYERS_CONF_VERSION = "2"
BBPATH = "${TOPDIR}"
BBFILES ?= ""
BBLAYERS ?= " \
  ${TOPDIR}/../meta \
  ${TOPDIR}/../meta-poky \
  ${TOPDIR}/../meta-yocto-bsp \
  ${TOPDIR}/../meta-openembedded/meta-oe \
  ${TOPDIR}/../meta-qt5 \
  ${TOPDIR}/../boatyard/meta-myproduct \
  "
EOF

cat >> conf/local.conf <<'EOF'
MACHINE = "qemuarm64"
IMAGE_INSTALL:append = " qtbase qtdeclarative hello-ui hello"
DISTRO_FEATURES:append = " opengl wayland"

# shared box — leave cores for the other work
BB_NUMBER_THREADS = "24"
PARALLEL_MAKE = "-j 24"
EOF

echo "starting bitbake (detached, log: ~/build.log)..."
nohup nice -n 10 bitbake core-image-minimal > ~/build.log 2>&1 &

echo "watch it here:  tail -f ~/build.log"
