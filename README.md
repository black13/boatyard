# boatyard — a reference Yocto skeleton for the i.MX8MP EVK

A minimal, buildable copy of the platform patterns documented in
the platform-pattern notes (kept in the private study repo), targeting the **NXP i.MX 8M Plus
EVK** (`imx8mp-lpddr4-evk`).

## Layout

```
yocto-skeleton/
├── local.conf.sample           build config (read-only rootfs, A/B, manifest)
├── scripts/build.sh            one-command build
├── meta-mydistro/              the distro layer  ("mydistro" equivalent)
├── meta-mybsp/                 the BSP layer      (EVK machine + tweaks)
└── meta-myproduct/             the product layer  (apps track master)
    ├── recipes-core/build-manifest/   → /etc/build on every image
    ├── recipes-core/base-files/       → the read-only fstab
    ├── wic/                            → A/B partition layout
    ├── recipes-support/swupdate/       → signed update description
    └── recipes-apps/hello/             → the daemon pattern
```

## Prerequisites

```
sudo apt install gawk wget git diffstat unzip gcc-multilib build-essential \
     chrpath socat cpio python3 zstd liblz4-tool xz-utils
mkdir -p ~/yocto && cd ~/yocto
git clone -b kirkstone git://git.yoctoproject.org/poky.git
git clone -b kirkstone git://git.openembedded.org/meta-openembedded
git clone -b lf-5.15.71-2.2.0 https://github.com/nxp-imx/meta-imx.git
git clone <your repo with yocto-skeleton> meta-mydistro meta-mybsp meta-myproduct
```

## Build

```
cd ~/yocto
cp yocto-skeleton/local.conf.sample build/conf/local.conf   (edit MACHINE if needed)
source poky/oe-init-build-env build
bitbake myimage
```

The image lands in `build/tmp/deploy/images/imx8mp-lpddr4-evk/` as
`myimage-imx8mp-lpddr4-evk.wic` — flash it to an SD card, boot the EVK,
then check `cat /etc/build` on the unit: it will print the full manifest,
exactly like the platform.s devices do.

## Patterns implemented (cross-ref to the playbook)

| Pattern | Where |
|---|---|
| §1 reproducible manifest | `build-manifest_1.0.bb` |
| §2 read-only rootfs | `local.conf.sample`, `base-files_%.bbappend` |
| §3 daemon architecture | `hello_1.0.bb` + `hello.service` |
| §4 A/B updates | `myimage-ab.wks.in` + boot slot logic in `build.sh` notes |
| §5 one update channel | `sw-description` template |
| §6 real-time | kernel cmdline in `imx8mp-lpddr4-evk.conf` |
| §7 container format | `sw-description` + signing notes in README |
| §8 eng/rel culture | `BUILDTYPE` distro knob in `mydistro.conf` |
