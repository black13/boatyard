"""Launch the qemuarm64 image in a WINDOW using ramfb (lightweight
framebuffer) instead of virtio-gpu. Serial also mirrored to boot.log
so we can compare progress. Leaves the window open if healthy."""
import subprocess
import time
from pathlib import Path

QEMU = r"C:\Program Files\qemu\qemu-system-aarch64.exe"
RUN = Path(r"D:\boatyard\qemu-run")
LOG = RUN / "boot.log"

subprocess.run(["taskkill", "/F", "/IM", "qemu-system-aarch64.exe"],
               capture_output=True)
time.sleep(2)

args = [
    QEMU,
    "-M", "virt", "-cpu", "cortex-a57", "-smp", "4", "-m", "1024",
    "-device", "ramfb",
    "-display", "sdl",
    "-kernel", str(RUN / "images" / "Image"),
    "-drive", f"file={RUN / 'images' / 'core-image-minimal-qemuarm64.ext4'},format=raw,if=none,id=hd",
    "-device", "virtio-blk-device,drive=hd",
    "-append", "root=/dev/vda rw console=tty0 console=ttyAMA0,115200",
    "-serial", f"file:{LOG}",
    "-monitor", "none",
]

proc = subprocess.Popen(args, cwd=str(RUN),
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"launched pid {proc.pid} — window should appear")
time.sleep(75)
print(f"alive: {proc.poll() is None}")
if LOG.exists():
    tail = LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-6:]
    print("--- serial progress ---")
    print("\n".join(tail))
