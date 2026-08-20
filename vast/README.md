# boatyard build run — vast.ai

## Division of labor (standing rule)

- **You run the scripts and watch the output.** The build is always visible
  in YOUR terminal; nothing is hidden.
- **Scripts tee to `~/build.log`** on the box.
- **The agent tails that same log** over SSH and reports at milestones —
  it never runs the build itself, only watches.

## The two scripts

| Script | Purpose | When |
|---|---|---|
| `provision.sh` | apt deps + git config + clone layers + configure | once per box |
| `build.sh` | bitbake, detached, log at `~/build.log` | every build |

## How to run (on the vast box, as root over SSH)

```sh
# once per box:
curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/provision.sh | bash

# every build:
curl -sL https://raw.githubusercontent.com/black13/boatyard/main/vast/build.sh | bash
```

Watch it live in your terminal:

```sh
tail -f ~/build.log     # ctrl-c stops the VIEW, not the build
```

Done = you see `Tasks Summary` near the end of the log.

## Box picking

- Cheapest fixed offers: search 16+ CPU cores, 100 GB+ disk, verified,
  non-interruptible, ~$0.15-0.20/hr — a first build costs ~$0.30 total.
- Interruptible bids (~$0.11/hr) are an option for repeat runs once the
  sstate cache is backed up.

## Safety

- All commands are standard: apt, git clone, bitbake
- Nothing touches your laptop — everything runs on the vast box
- SSH from Windows: `ssh` is built in (OpenSSH client)
