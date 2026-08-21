"""Create a cheap build instance on vast.ai.

Usage:
  python vast-create.py [--label NAME] [--max-price 0.22]
Prints the new contract id and ssh endpoint.
"""
import argparse
import json
import subprocess
import sys
import time

VAST = r"C:\Users\jjosb\.local\bin\vastai.exe"


def run(args):
    r = subprocess.run([VAST, *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        sys.exit(1)
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="boatyard-build")
    ap.add_argument("--max-price", type=float, default=0.22)
    ap.add_argument("--min-cores", type=int, default=16)
    ap.add_argument("--min-disk", type=int, default=150)
    ap.add_argument("--disk", type=int, default=100)
    args = ap.parse_args()

    query = (
        f"cpu_cores_effective>={args.min_cores} rentable=true verified=true "
        f"disk_space>={args.min_disk} dph_total<{args.max_price}"
    )
    out = run(["search", "offers", query, "--order", "dph_total-",
               "--limit", "10", "--raw"])
    offers = json.loads(out)
    if not offers:
        print("no offers matched", file=sys.stderr)
        sys.exit(1)

    for o in offers:
        print(f"  {o['id']}  ${o['dph_total']}  cpu={o['cpu_cores_effective']} "
              f"ram={o['cpu_ram'] // 1024}G disk={o['disk_space']}G {o['gpu_name']}")

    best = offers[0]
    print(f"\ncreating instance on offer {best['id']}...")
    out = run(["create", "instance", str(best["id"]),
               "--image", "pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime",
               "--label", args.label,
               "--disk", str(args.disk),
               "--raw"])
    print(out)

    created = json.loads(out)
    if not created.get("success"):
        sys.exit(1)
    contract = created["new_contract"]

    print("waiting for the instance to boot...")
    for _ in range(40):
        time.sleep(15)
        rows = json.loads(run(["show", "instances", "--raw"]))
        inst = next((x for x in rows if x["id"] == contract), None)
        if inst and inst.get("actual_status") == "running":
            print(f"\ncontract {contract} is RUNNING")
            print(f"ssh: root@{inst['ssh_host']} -p {inst['ssh_port']}")
            print(f"price: ${inst['dph_total']}/hr")
            return
    print("timed out waiting for running state", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
