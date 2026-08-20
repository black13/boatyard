# Hetzner one-day build farm

Hetzner Cloud, hourly billing — a 16-vCPU/32GB box for ~€1.20/day.
You create it, build, destroy. Nothing to unsubscribe.

## Step 0 — one-time account setup (you do this)

1. Sign up at https://console.hetzner.com (needs a payment method)
2. Create a project (default one is fine)
3. **Security → API Tokens → Generate token** — copy it
4. Paste the token back in chat; I'll store it with hcloud:

```sh
hcloud context create boatyard
# then paste the token when asked
```

## Step 1 — create the farm (I run, or you run with me)

```sh
hcloud server create \
  --name boatyard-build \
  --type cx52 \
  --image ubuntu-24.04 \
  --location nbg1 \
  --ssh-key your-key-name
```

If you have no SSH key yet, generate one first:

```sh
ssh-keygen -t ed25519 -f ~/.ssh/hetzner_boatyard
hcloud ssh-key create --name boatyard --public-key-from-file ~/.ssh/hetzner_boatyard.pub
```

## Step 2 — build (run 02-build.sh on the box)

```sh
hcloud server ssh boatyard-build    # drops you in
curl -sL https://raw.githubusercontent.com/black13/boatyard/main/hetzner/02-build.sh | bash
```

The build runs detached and writes to `~/build.log` — `04-watch.sh` tails it.

## Step 3 — destroy (run 03-destroy.sh)

```sh
hcloud server delete boatyard-build
```

Cost: ~€0.055/hr × hours used. A full qemuarm64 image with Qt5 = 2–4 h
on this box. No minimum term, no monthly bill.
