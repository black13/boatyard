"""Check qemu state and reproduce a launch capturing stderr to see
exactly why the window does not appear in the user's session."""
import subprocess
import time
from pathlib import Path

QEMU = r"C:\Program Files\qemu\qemu-system-aarch64.exe"
RUN = Path(r"D:\boatyard\qemu-run")
LOG = RUN / "boot.log"
ERR = RUN / "qemu-err.log"

r = subprocess.run(["tasklist"], capture_output=True, text=True)
running = "qemu-system-aarch64" in r.stdout
print("qemu currently running:", running)

if LOG.exists():
    lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    print("boot.log lines:", len(lines))
    print("\n".join(lines[-4:]))

subprocess.run(["taskkill", "/F", "/IM", "qemu-system-aarch64.exe"],
               capture_output=True)
time.sleep(2)

args = [
    QEMU, "-M", "virt", "-cpu", "cortex-a57", "-smp", "4", "-m", "1024",
    "-device", "ramfb", "-display", "sdl",
    "-kernel", str(RUN / "images" / "Image"),
    "-drive", f"file={RUN / 'images' / 'core-image-minimal-qemuarm64.ext4'},format=raw,if=none,id=hd",
    "-device", "virtio-blk-device,drive=hd",
    "-append", "root=/dev/vda rw console=tty0 console=ttyAMA0,115200",
    "-serial", f"file:{LOG}", "-monitor", "none",
]

with open(ERR, "w") as ef:
    proc = subprocess.Popen(args, cwd=str(RUN), stderr=ef,
                            stdout=subprocess.DEVNULL)
time.sleep(20)
print("alive after 20s:", proc.poll() is None)
err = ERR.read_text(encoding="utf-8", errors="replace") if ERR.exists() else ""
print("--- stderr ---")
print(err.strip()[:1200] if err.strip() else "(empty)")
