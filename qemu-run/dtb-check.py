"""Figure out why the guest never initializes a display.
1) Dump the DTB QEMU generates for -machine virt and look for
   framebuffer nodes (simple-framebuffer / ramfb).
2) Scan boot.log for kernel framebuffer/drm probe messages."""
import subprocess
import re
from pathlib import Path

QEMU = r"C:\Program Files\qemu\qemu-system-aarch64.exe"
RUN = Path(r"D:\boatyard\qemu-run")
DTB = RUN / "dump.dtb"
LOG = RUN / "boot.log"

subprocess.run([QEMU, "-machine", "virt,dumpdtb=" + str(DTB)],
               capture_output=True, cwd=str(RUN))
data = DTB.read_bytes() if DTB.exists() else b""
print("dtb size:", len(data))
for needle in [b"simple-framebuffer", b"ramfb", b"framebuffer",
               b"virtio,gpu", b"virtio-gpu-pci"]:
    print(f"  contains {needle.decode():20s}:", needle in data)

print("\n--- boot.log framebuffer/drm lines ---")
if LOG.exists():
    for line in LOG.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.search(r"fb|drm|framebuffer|virtio_gpu|simple", line, re.I):
            print(line[:140])
