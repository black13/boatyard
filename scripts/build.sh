#!/bin/sh
# One-command build for the myboat skeleton.
# Run from the poky checkout:  scripts/build.sh

set -e

MACHINE=imx8mp-lpddr4-evk
DISTRO=mydistro

if [ ! -f build/conf/local.conf ]; then
    mkdir -p build/conf
    cp yocto-skeleton/local.conf.sample build/conf/local.conf
    cat >> build/conf/bblayers.conf <<EOF
BBLAYERS += " \\"
  \${TOPDIR}/../meta-openembedded/meta-oe \\"
  \${TOPDIR}/../meta-openembedded/meta-python \\"
  \${TOPDIR}/../meta-openembedded/meta-networking \\"
  \${TOPDIR}/../meta-imx/meta-bsp \\"
  \${TOPDIR}/../meta-mydistro \\"
  \${TOPDIR}/../meta-mybsp \\"
  \${TOPDIR}/../meta-myproduct \\"
  "
EOF
fi

source poky/oe-init-build-env build
bitbake myimage

# The wic image: tmp/deploy/images/$MACHINE/myimage-$MACHINE.wic
# Flash:  sudo dd if=myimage-*.wic of=/dev/sdX bs=4M conv=fsync
# On the EVK:  cat /etc/build      <- the manifest, like the reference platform
