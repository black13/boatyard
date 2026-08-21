"""Kill qemu, then extract the kernel's embedded config (IKCONFIG) and
check the graphics/console options relevant to the windowed boot."""
import subprocess
import struct
import time
import zlib
from pathlib import Path

subprocess.run(["taskkill", "/F", "/IM", "qemu-system-aarch64.exe"],
               capture_output=True)
time.sleep(2)
print("qemu stopped.")

img = (Path(r"D:\boatyard\qemu-run\images\Image")).read_bytes()
marker = b"IKCFG_ST"
i = img.find(marker)
print("IKCONFIG embedded:", i != -1)

if i != -1:
    start = i + len(marker)
    gz = img.find(b"\x1f\x8b", start, start + 512)
    cfg = None
    if gz != -1:
        try:
            cfg = zlib.decompress(img[gz:], 16 + zlib.MAX_WBITS).decode("utf-8", "replace")
        except Exception as e:
            print("decompress failed:", e)
    if cfg is None:
        raise SystemExit("no config extracted")
    wanted = [
        "CONFIG_VT", "CONFIG_DRM_VIRTIO_GPU", "CONFIG_FRAMEBUFFER_CONSOLE",
        "CONFIG_DRM_FBDEV_EMULATION", "CONFIG_DRM_SIMPLEDRM",
        "CONFIG_FB_SIMPLE", "CONFIG_DRM", "CONFIG_TTY",
    ]
    for line in cfg.splitlines():
        key = line.split("=")[0]
        if key in wanted:
            print(line)
