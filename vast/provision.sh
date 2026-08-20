#!/bin/bash
# boatyard provision — gets the machine READY to build (one-time per box).
# Run on the vast box:   curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/provision.sh | bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "=== [1/3] apt packages ==="
apt-get update -y -q
apt-get install -y -q gawk wget git diffstat unzip gcc build-essential \
    chrpath cpio python3 python3-pip python3-pexpect xz-utils debianutils \
    python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev xterm python3-subunit \
    mesa-common-dev zstd liblz4-tool file locales
locale-gen en_US.UTF-8
git config --global --add safe.directory '*'

echo "=== [2/3] clone layers (GitHub mirrors — git.yoctoproject.org is blocked here) ==="
mkdir -p ~/yocto && cd ~/yocto
# remove any half-cloned dirs from a failed run
[ -d poky/.git ]              || rm -rf poky
[ -d meta-openembedded/.git ] || rm -rf meta-openembedded
[ -d poky ]                   || git clone -q -b kirkstone https://github.com/yoctoproject/poky.git
[ -d meta-openembedded ]      || git clone -q -b kirkstone https://github.com/openembedded/meta-openembedded.git
[ -d meta-qt5 ]               || git clone -q -b kirkstone https://github.com/meta-qt5/meta-qt5.git
if [ -d boatyard ]; then (cd boatyard && git pull -q); else git clone -q https://github.com/black13/boatyard.git; fi

echo "=== [3/3] configure ==="
cd poky
source oe-init-build-env build

cat > conf/bblayers.conf <<'EOF'
POKY_BBLAYERS_CONF_VERSION = "2"
BBPATH = "${TOPDIR}"
BBFILES ?= ""
BBLAYERS ?= " \
  ${TOPDIR}/../meta \
  ${TOPDIR}/../meta-poky \
  ${TOPDIR}/../meta-yocto-bsp \
  ${TOPDIR}/../../meta-openembedded/meta-oe \
  ${TOPDIR}/../../meta-qt5 \
  ${TOPDIR}/../../boatyard/meta-myproduct \
  "
EOF

if ! grep -q '^MACHINE = "qemuarm64"' conf/local.conf; then
cat >> conf/local.conf <<'EOF'
MACHINE = "qemuarm64"
IMAGE_INSTALL:append = " qtbase qtdeclarative hello-ui hello"
DISTRO_FEATURES:append = " opengl wayland"

# shared box — leave cores for the other work
BB_NUMBER_THREADS = "24"
PARALLEL_MAKE = "-j 24"
EOF
fi

# we build as root inside the vast container — skip the host sanity checks
touch conf/sanity.conf

echo
echo "machine is ready. now run the build script."
