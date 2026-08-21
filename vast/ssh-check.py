"""Retry SSH to a vast box until it accepts, then print its vitals."""
import subprocess
import sys
import time

port = sys.argv[1]
host = sys.argv[2] if len(sys.argv) > 2 else "ssh7.vast.ai"
key = r"C:\Users\jjosb\.ssh\id_ed25519_vast"

for i in range(12):
    r = subprocess.run(
        [r"C:\Windows\System32\OpenSSH\ssh.exe", "-i", key,
         "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=8",
         "-p", port, f"root@{host}",
         "hostname; nproc; free -g | head -2; df -h / | tail -1"],
        capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        print(r.stdout)
        sys.exit(0)
    print(f"try {i + 1}: rc={r.returncode}", flush=True)
    time.sleep(30)
print("ssh never came up", flush=True)
sys.exit(1)
