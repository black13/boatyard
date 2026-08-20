# Stage 1 — The Boot Script, line by line

**What:** how an embedded Linux device goes from power-on to a running
kernel, as an annotated u-boot script.
**Source of the pattern:** the reference platform's production boot script
(the private study notes hold the original; this is the generic restatement).

---

## The script

```sh
# 1. Naming things
setenv devtype mmc
setenv devnum ${mmcdev}
setenv fdt_file imx8mp-queenstown.dtb
setenv kernel_addr_r ${loadaddr}

# 2. The A/B decision
if test -z "${boot_slot}"; then
    echo "ERROR: Boot slot undefined!"
    exit
fi

# 3. OS-supplied overrides
if load ${devtype} ${mmcdev}#root_${boot_slot} ${loadaddr} /boot/uEnv.txt; then
    env import -t ${loadaddr} ${filesize}
fi

# 4. Name -> number -> UUID
part number mmc ${mmcdev} root_${boot_slot} root_part_num
part uuid mmc ${mmcdev}:${root_part_num} root_partuuid

# 5. Stable identity
machine set-id ${mmcdev} machine-id
setenv bootargs ${bootargs} systemd.machine_id=${machine-id}

# 6. Load kernel + device tree from the slot
ext4load mmc ${mmcdev}:${root_part_num} ${kernel_addr_r} /boot/Image
ext4load mmc ${mmcdev}:${root_part_num} ${fdt_addr_r} /boot/${fdt_file}

# 7. The kernel command line
setenv bootargs ${bootargs} console=${console} earlycon \
    isolcpus=3 threadirqs \
    root=PARTUUID=${root_partuuid} \
    boot_slot=${boot_slot} ${extrabootargs}

# 8. Handoff
booti ${kernel_addr_r} - ${fdt_addr_r}
```

---

## What each part teaches

**1. Naming things.** The script never hardcodes a device path. `devtype`,
`fdt_file`, load addresses are named variables set once — change the board,
change the variables, not the logic.

**2. The A/B decision happens *before* this script.** `boot_slot` was set by
the updater (or a previous boot verdict). The script's only job: *refuse to
guess*. A device that fails loudly is a device that doesn't brick itself.

**3. The OS can override the bootloader.** `/boot/uEnv.txt` inside the
rootfs is imported into the u-boot environment. The OS is allowed to say
"next time, boot differently" — without reflashing the bootloader. Boot
behavior becomes *data*.

**4. Name → number → UUID.** The bootloader thinks in partition names
(`root_a`). The kernel wants `PARTUUID=…`. The script is the translator.
The updater therefore never touches device numbers — it touches names, which
survive layout changes.

**5. Identity is explicit.** The machine-id is read from hardware and handed
to systemd. Stable identity across boots and across slots.

**6. A slot is a complete system.** Kernel, device tree, and rootfs all live
inside the same partition. The bootloader reads them *from the slot it was
told to boot*. Consequences:
- each slot carries its own matched kernel+dtb+rootfs
- there is no shared boot partition to corrupt
- rolling back a bad update = flipping `boot_slot` back

**7. The cmdline is where policy lives.**
- `root=PARTUUID=…` — which slot, by stable identity
- `isolcpus=3` — reserve a CPU core for time-critical work
- `threadirqs` — run interrupts as threads so priorities can be managed
- the slot name is passed *into* the kernel — the OS knows which slot it is

**8. `booti` is the aarch64 handoff** — kernel image + device tree, no
initrd (the rootfs is a real filesystem, not a ramdisk).

---

## The three ideas that matter most

1. **Names over numbers** — everything is addressed by name or UUID, never
   by device position. Layouts can change; names hold.
2. **A slot is a system** — kernel+dtb+rootfs travel together, so updates
   are atomic at the partition level and rollback is trivial.
3. **The bootloader is dumb on purpose** — it does the minimum (pick slot,
   load, translate names) and gets out of the way. Policy lives in the
   cmdline and the OS.

## Practice (qemu)

Run the qemu image and observe each idea:

```sh
cat /proc/cmdline        # the assembled command line
cat /etc/machine-id      # the identity from step 5
lsblk -o NAME,PARTLABEL,PARTUUID   # names vs numbers
cat /proc/interrupts     # threadirqs: see the threaded handlers
```

*Next in Stage 1: the root filesystem (fstab, mounts, what "read-only" means).*
