"""Run the demo qemu command exactly like run-demo.cmd, but capture
stderr and report whether the process stays alive."""
import subprocess
import time
from pathlib import Path

RUN = Path(r"D:\boatyard\qemu-run")
QEMU = r"C:\Program Files\qemu\qemu-system-x86_64w.exe"

args = [
    QEMU, "-machine", "q35", "-cpu", "IvyBridge", "-smp", "4", "-m", "1024",
    "-vga", "virtio", "-usb", "-device", "usb-tablet",
    "-kernel", str(RUN / "images" / "bzImage-demo"),
    "-hda", str(RUN / "images" / "boatyard-demo-image-qemux86-64.ext4"),
    "-append", "root=/dev/sda rw console=ttyS0,115200 oprofile.timer=1 "
               "tsc=reliable no_timer_check rcupdate.rcu_expedited=1",
    "-display", "sdl",
    "-serial", f"file:{RUN / 'boot-demo.log'}",
]

err = RUN / "demo-err.log"
with open(err, "w") as ef:
    proc = subprocess.Popen(args, cwd=str(RUN), stderr=ef,
                            stdout=subprocess.DEVNULL)
time.sleep(15)
print("alive after 15s:", proc.poll() is None)
if proc.poll() is not None:
    print("exit code:", proc.returncode)
print("--- stderr ---")
print(err.read_text(errors="replace")[:800])
