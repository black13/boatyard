# $0 Qt5 learning path — run it in qemu today

The skeleton now ships a miniature copy of the platform.s UI architecture:

- `hello-ui`  = the `ui_app` equivalent  (QtQuick/QML scene, Wayland client)
- `hello`     = the `server_app` equivalent (QtCore-ish headless daemon, systemd)

## Build for emulation (free, no board)

```sh
# in the poky checkout
source poky/oe-init-build-env build-qemu
MACHINE=qemuarm64 bitbake myimage
```

Add Qt to the image first — in `local.conf`:

```sh
IMAGE_INSTALL:append = " hello-ui hello weston weston-init"
DISTRO_FEATURES:append = " wayland x11"
```

and add `meta-qt5` to `bblayers.conf` (clone it from
https://github.com/meta-qt5/meta-qt5, branch matching your poky — 'kirkstone'
or the older branch if you want Qt 5.6-era APIs).

## Run it

```sh
runqemu qemuarm64 nographic slirp     # boot
# on the target:
export XDG_RUNTIME_DIR=/run/user/root
weston --tty=1 &
hello-ui -platform wayland             # the Garmin path: Qt on Weston
# or skip the compositor entirely:
hello-ui -platform eglfs               # Qt owns the screen (kiosk without Weston)
```

The status bar in the app prints which plugin it's using — that's the lesson:
**the same QML app runs on wayland, eglfs, or xcb**; the platform plugin is
the whole "embedded" difference. That's exactly how the platform.s `ui_app` works.

## Then learn the SDK loop (still $0)

```sh
bitbake -c populate_sdk myimage
# install the .sh SDK, then on the host:
source /opt/mydistro/*/environment-setup-aarch64-*
qmake && make          # cross-compile hello-ui from your laptop
scp hello-ui root@<qemu-ip>:/
```

## When cash allows

The same image runs on a Raspberry Pi 4 with `MACHINE=raspberrypi4`
(+ `meta-raspberrypi`) — the only difference is real DRM/GPU instead of
emulated GL. Nothing in the code changes.
