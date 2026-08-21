"""Download the demo image + kernel from the working vast box."""
import subprocess
import time
from pathlib import Path

SCP = r"C:\Windows\System32\OpenSSH\scp.exe"
KEY = r"C:\Users\jjosb\.ssh\id_ed25519_vast"
DEST = Path(r"D:\boatyard\qemu-run\images")

box = Path(r"D:\boatyard\vast\vast-working-box.txt").read_text().split()
host, port = box[1], box[2]
base = f"root@{host}:~/yocto/poky/build/tmp/deploy/images/qemux86-64"

files = [
    ("boatyard-demo-image-qemux86-64.ext4", "boatyard-demo-qemux86-64.ext4"),
    ("bzImage", "bzImage-demo"),
]

for remote, local in files:
    t0 = time.time()
    print(f"downloading {remote} ...", flush=True)
    r = subprocess.run(
        [SCP, "-i", KEY, "-o", "StrictHostKeyChecking=no",
         "-P", port, f"{base}/{remote}", str(DEST / local)],
        capture_output=True, text=True, timeout=1800)
    print(f"  rc={r.returncode} in {time.time() - t0:.0f}s", flush=True)
    if r.returncode != 0:
        print(r.stderr[:300])

print("\nlocal files:")
for f in sorted(DEST.iterdir()):
    print(f"  {f.name}  {round(f.stat().st_size / 1048576, 1)} MB")
