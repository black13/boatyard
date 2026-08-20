# The Study Plan — what we should be knowing

This is the living map of the learning project. It is deliberately generic
(no vendor material) — the goal is understanding the *platform engineering*,
not any one product. Each item has a **concept** (what to know), an
**observation** (what the reference system did — from the private study
notes), and a **practice** (what to build/run in this repo).

Order matters. Each stage unlocks the next.

---

## Stage 1 — Embedded Linux, the substrate

**Why first:** everything else sits on this. You can't understand Yocto or Qt
without knowing what a rootfs is, what a bootloader does, what the kernel
cmdline controls.

| Concept | Observation | Practice |
|---|---|---|
| Boot sequence: ROM → u-boot → kernel → init | u-boot script selecting A/B slots, kernel args `root=PARTUUID=...` | read `meta-mybsp` notes; run qemu and watch the boot log |
| Rootfs anatomy: /etc, /usr, mounts, fstab | read-only `/` with tmpfs `/var/volatile` and `/media` | `fstab.note` in this repo — understand every line |
| systemd: units, services, targets | daemons with `StateDirectory`, restart policies, `StartLimitAction=reboot` | `hello.service` — read it, then extend it |
| The kernel cmdline | `isolcpus=3 threadirqs` for real-time | add a custom cmdline arg, read it back from `/proc/cmdline` in qemu |
| Processes & IPC: DBus, named pipes, sockets | UI↔server split across DBus; FIFO IPC for media mounting | make `hello` (daemon) and `hello-ui` (UI) talk over DBus — Stage 3 exercise |

## Stage 2 — Yocto, the build system

**Why second:** the whole platform is *assembled* here. This is the most
career-relevant skill in the study.

| Concept | Observation | Practice |
|---|---|---|
| Layers, recipes, machines, distros | distro frozen at a branch; BSP machine per board; app layers track master | build the skeleton in qemu; then add your own recipe |
| The task graph: fetch → unpack → configure → compile → package | the same flow for every package | `bitbake -e hello` — read the environment |
| IMAGE_FEATURES & image recipes | `read-only-rootfs`, `ssh-server-openssh` | toggle a feature, see the rootfs change |
| The SDK: `populate_sdk`, environment-setup, cross-qmake | the cross-compile loop | build the SDK, cross-build `hello-ui` on the host, run on qemu |
| Reproducibility: manifests, pinned commits, sstate cache | `/etc/build` carries every layer's commit | the `build-manifest` recipe — run it, read `/etc/build` in qemu |
| Updates: SWUpdate, A/B slots, signed descriptions | dual root slots, per-image sha256, postinstall commit | `sw-description.template` + `myimage-ab.wks.in` — understand each field |

## Stage 3 — Qt on embedded

**Why third:** the UI half of the stack, and the thing you explicitly wanted.

| Concept | Observation | Practice |
|---|---|---|
| Qt modules: QtCore vs QtGui vs QML/QtQuick | UI in QML (`ui_app`-style), services in QtCore (`server_app`-style) | `hello-ui` + `hello` — the same split |
| Platform plugins: `wayland` vs `eglfs` vs `offscreen` | same QML app, three backends — the plugin *is* the "embedded" part | run `hello-ui` with each `-platform` and watch the status bar |
| The compositor: Weston, kiosk shell, multi-output | Weston with per-output app assignment (touch screen + HDMI) | add a second virtual output in qemu; set `weston.ini` app-ids |
| QML rendering: scene graph, Canvas, textures | the echo-trace Canvas in `hello-ui` — where a sonar trace would draw | make the Canvas stream from the daemon's shared variables (see Stage 4) |
| Signals/slots & DBus bindings | UI subscribes to service state over DBus | `hello` publishes a counter; `hello-ui` renders it live |

## Stage 4 — The application architecture

**Why fourth:** how the pieces become a product — the ten-daemon pattern.

| Concept | Observation | Practice |
|---|---|---|
| Process-per-failure-domain | supervisor + server + UI + per-bus daemons | split `hello` into two daemons with a supervisor script |
| Shared state: a variables broker | the shared-variables service feeding the UI | make a tiny `gsvd`-style broker: daemons publish, UI subscribes |
| The runtime abstraction (the RTOS-shaped API) | `os::init/task/mutex` over pthreads | write your own `os::` mini-library: task/mutex/sleep wrappers over pthreads |
| Supervision & crash policy | spawn supervisor with restart counts, reboot on crash-loop | implement the `StartLimitAction=reboot` pattern by hand once |
| The media pipeline | streaming SDK plugins inside GStreamer | Stage 5 topic — needs gstreamer in the image |

## Stage 5 — The deep end

**Why last:** these need everything before them.

| Concept | Observation | Practice |
|---|---|---|
| Real-time mechanics | `isolcpus`, `threadirqs`, governor, autogroup | measure jitter on your qemu core with/without `isolcpus` |
| DSP offload: the co-processor | audio/DSP work on a DSP core, not the app CPUs | read the HiFi4/DSP architecture in the private notes; understand the split |
| Update containers & signing | header + description + signature + trailer | build a real `.swu` for the qemu image and apply it |
| The full loop | device reports what it runs | qemu unit that answers `cat /etc/build` + `hello-ui` version |

---

## How to run the study

1. **Track**: the vast.ai instance (`vast/`) runs the Stage 2/3 builds —
   you execute, I watch output, we read results together.
2. **Notes**: every concept gets a page in `notes/` once understood —
   written in your own words (that's the real test of knowing).
3. **Pace**: one row per session is plenty. This is months, not days.

*Current position: Stage 1 row 1 (boot sequence) — the qemu build is the
first practical step of Stage 2, and the two can interleave.*
