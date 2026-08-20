# Step 1 — Connect to the shared box

Your H200 workstation is already running. Open a terminal and SSH in:

```sh
ssh root@ssh4.vast.ai -p 35532
```

If it asks about a host key, accept (`yes`). You're in as root.

Then run step 2:

```sh
curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/02-instance-setup.sh | bash
```

> Note: this box is shared with your training work. The build script is
> written to be a good citizen: it limits itself to ~24 cores and runs
> niced, so your other jobs keep most of the machine.
