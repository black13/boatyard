"""Self-healing vast build box launcher.

Loop: pick a cheap offer -> create instance -> wait for running ->
ssh-check -> if SSH works, STOP and print the user's commands.
If not, destroy and try the next offer (up to --tries).

The working box is LEFT RUNNING; its contract id is written to
vast-working-box.txt.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

VAST = r"C:\Users\jjosb\.local\bin\vastai.exe"
SSH = r"C:\Windows\System32\OpenSSH\ssh.exe"
KEY = r"C:\Users\jjosb\.ssh\id_ed25519_vast"
IMAGE = "ubuntu:22.04"


def vast(*args, **kw):
    return subprocess.run([VAST, *args], capture_output=True, text=True, **kw)


def ssh_ok(host, port):
    r = subprocess.run(
        [SSH, "-i", KEY, "-o", "StrictHostKeyChecking=no",
         "-o", "ConnectTimeout=8", "-p", str(port), f"root@{host}",
         "echo up"],
        capture_output=True, text=True, timeout=30)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tries", type=int, default=5)
    ap.add_argument("--max-price", type=float, default=0.25)
    ap.add_argument("--min-cores", type=int, default=16)
    ap.add_argument("--min-disk", type=int, default=200)
    ap.add_argument("--label", default="boatyard-build")
    ap.add_argument("--disk", type=int, default=100)
    args = ap.parse_args()

    query = (f"cpu_cores_effective>={args.min_cores} rentable=true "
             f"verified=true disk_space>={args.min_disk} "
             f"dph_total<{args.max_price}")
    r = vast("search", "offers", query, "--order", "dph_total-",
             "--limit", "12", "--raw")
    offers = json.loads(r.stdout)
    if not offers:
        print("no offers", file=sys.stderr)
        sys.exit(1)
    print(f"{len(offers)} candidate offers\n")

    tried = set()
    for attempt in range(args.tries):
        offer = next(o for o in offers if o["id"] not in tried)
        tried.add(offer["id"])
        print(f"--- attempt {attempt + 1}/{args.tries}: offer {offer['id']} "
              f"${offer['dph_total']} cpu={offer['cpu_cores_effective']} "
              f"ram={offer['cpu_ram'] // 1024}G "
              f"disk={offer['disk_space']}G ---")

        r = vast("create", "instance", str(offer["id"]),
                 "--image", IMAGE, "--label", args.label,
                 "--disk", str(args.disk), "--raw")
        try:
            created = json.loads(r.stdout)
        except json.JSONDecodeError:
            print("  create failed:", r.stdout[:120])
            continue
        contract = created.get("new_contract")
        if not contract:
            print("  no contract returned")
            continue

        running = None
        for _ in range(16):
            time.sleep(15)
            rows = json.loads(vast("show", "instances", "--raw").stdout)
            inst = next((x for x in rows if x["id"] == contract), None)
            if not inst:
                break
            if inst["actual_status"] == "running":
                running = (inst["ssh_host"], inst["ssh_port"], contract)
                break

        if not running:
            print("  never reached running — destroying")
            vast("destroy", "instance", str(contract), input="y\n")
            continue

        host, port, contract = running
        print(f"  running at {host}:{port} — ssh-checking...")
        ok = False
        for _ in range(8):
            if ssh_ok(host, port):
                ok = True
                break
            time.sleep(20)
        if not ok:
            print("  ssh refused — destroying, next offer")
            vast("destroy", "instance", str(contract), input="y\n")
            continue

        print(f"\nBOX READY: contract {contract}  {host}:{port}\n")
        print("Run these in YOUR terminal:\n")
        print(f"ssh -i C:\\Users\\jjosb\\.ssh\\id_ed25519_vast "
              f"root@{host} -p {port}\n")
        print("curl -sL https://raw.githubusercontent.com/black13/"
              "boatyard/main/vast/provision.sh | bash\n")
        print("curl -sL https://raw.githubusercontent.com/black13/"
              "boatyard/main/vast/build.sh | bash -s qemux86-64 "
              "boatyard-demo-image\n")
        Path(r"D:\boatyard\vast\vast-working-box.txt").write_text(
            f"{contract} {host} {port}\n")
        sys.exit(0)

    print("\nall attempts failed — vast is having a bad day", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
