"""Diagnose the qemuarm64 boot: kill any stuck qemu, relaunch headless,
capture the serial console to boot.log, print the tail."""
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
    "-kernel", str(RUN / "images" / "Image"),
    "-drive", f"file={RUN / 'images' / 'core-image-minimal-qemuarm64.ext4'},format=raw,if=none,id=hd",
    "-device", "virtio-blk-device,drive=hd",
    "-append", "root=/dev/vda rw console=ttyAMA0,115200",
    "-nographic",
    "-serial", f"file:{LOG}",
    "-monitor", "none",
]

proc = subprocess.Popen(args, cwd=str(RUN),
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"launched pid {proc.pid}, waiting 90s...")
time.sleep(90)

poll = proc.poll()
print(f"process alive after 90s: {poll is None}")

if LOG.exists():
    tail = LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-40:]
    print("--- boot.log tail ---")
    print("\n".join(tail))
