"""Run one remote command on the working vast box and print output."""
import subprocess
import sys
from pathlib import Path

SSH = r"C:\Windows\System32\OpenSSH\ssh.exe"
KEY = r"C:\Users\jjosb\.ssh\id_ed25519_vast"

box = Path(r"D:\boatyard\vast\vast-working-box.txt").read_text().split()
contract, host, port = box[0], box[1], box[2]

cmd = " ".join(sys.argv[1:])
r = subprocess.run(
    [SSH, "-i", KEY, "-o", "StrictHostKeyChecking=no",
     "-p", port, f"root@{host}", cmd],
    capture_output=True, text=True, timeout=60)
print(r.stdout)
if r.stderr.strip():
    print("STDERR:", r.stderr[:400])
