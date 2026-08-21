"""Wait for a vast instance to reach 'running', printing progress."""
import json
import subprocess
import sys
import time

VAST = r"C:\Users\jjosb\.local\bin\vastai.exe"
contract = int(sys.argv[1])
timeout_min = float(sys.argv[2]) if len(sys.argv) > 2 else 15

for n in range(int(timeout_min)):
    time.sleep(60)
    r = subprocess.run([VAST, "show", "instances", "--raw"],
                       capture_output=True, text=True)
    rows = json.loads(r.stdout)
    inst = next((x for x in rows if x["id"] == contract), None)
    if not inst:
        print(f"[{n + 1}min] instance gone")
        sys.exit(1)
    st = inst["actual_status"]
    msg = (inst.get("status_msg") or "")[:60]
    print(f"[{n + 1}min] {st} {msg}", flush=True)
    if st == "running":
        print("RUNNING:", inst["ssh_host"], inst["ssh_port"])
        sys.exit(0)
print("still loading at timeout", flush=True)
sys.exit(1)
