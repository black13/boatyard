# Stage 1 — The Device Tree

**What:** the data structure that describes the hardware so the kernel
doesn't have to hardcode it.
**Canonical doc:** Grant Likely, *"Linux and the Devicetree"* —
https://docs.kernel.org/devicetree/usage-model.html

---

## The one-line idea

A device tree (DT) is a **tree of named nodes with named properties** that
describes a specific board's hardware. The kernel reads it at boot and
builds the device model from it. Same kernel binary, many boards — the
differences are *data*, not code.

The on-disk form is the **FDT** (Flattened Device Tree, the `.dtb` file) —
a binary blob the bootloader hands to the kernel. The human form is
**`.dts`** source, compiled with `dtc`.

## What the kernel uses it for (the three jobs)

**1. Platform identification.** The root node's `compatible` property is a
list of strings, most-specific first:

```
compatible = "boardname", "soc", "family";
```

Early boot matches this against a table of known machines and picks the
setup code. Most boards need no custom code at all — the SoC/family entry
matches the generic support.

**2. Runtime configuration.** The `/chosen` node carries boot parameters —
`bootargs`, initrd location, and platform extras. The kernel reads it before
anything else.

**3. Device population.** Every node with a `compatible` string becomes a
device. Root-level nodes become `platform_device`s; bus children (i2c, spi,
usb...) are created by their parent bus driver at probe time. This is the
"trick": the tree's hierarchy mirrors the bus hierarchy.

## The vocabulary

| Term | Meaning |
|---|---|
| node | a device or logical group: `i2c@30a30000` |
| property | key-value data on a node: `reg`, `compatible`, `interrupts` |
| `compatible` | "which driver claims this" — `vendor,model` strings |
| `reg` | address(es) on the parent bus — the unit address matches the node name |
| `#address-cells` / `#size-cells` | how many 32-bit words an address/size takes |
| `interrupts` / `interrupt-parent` | how the device's IRQ line is wired |
| phandle (`&name`) | a link to another node — how a sound node refers to its codec |
| `aliases` | stable names (`serial0`) for userspace |
| binding | the documented convention for how a device type is described |

## The pattern to recognize

```dts
/ {
    compatible = "vendor,board", "vendor,soc";
    memory { device_type = "memory"; reg = <0x0 0x40000000>; };
    chosen { bootargs = "..."; };

    soc {
        compatible = "simple-bus";
        i2c@1000 {
            compatible = "vendor,i2c";
            reg = <0x1000 0x100>;
            codec@1a {          /* an i2c child: address, not memory */
                compatible = "wlf,wm8903";
                reg = <0x1a>;
            };
        };
    };
    sound {
        compatible = "vendor,sound";
        i2s-codec = <&codec>;   /* phandle link */
    };
};
```

Notice: the SoC's internal devices sit on a `simple-bus` (they're
memory-mapped with absolute addresses), while `codec@1a` is an i2c child
whose `reg` is a *bus address* (0x1a), not memory. The tree structure
*is* the bus topology.

## Why this matters for the platform study

1. **One kernel, many boards** — the reference platform ships one kernel
   image for several boards; each board is a different `.dtb`. The boot
   script (Stage 1, previous note) picks the dtb by name.
2. **Hardware changes are data changes** — adding a peripheral = adding a
   node + a driver, not forking the kernel.
3. **The dtb is the board's fingerprint** — reading it tells you the SoC,
   RAM, codecs, buses, and wiring without touching hardware.

## Practice (qemu)

```sh
# the live tree the kernel actually built:
ls /proc/device-tree/
cat /proc/device-tree/compatible        # identification strings
cat /proc/device-tree/memory/reg        # hex — RAM size

# decompile the dtb if dtc is installed:
dtc -I fs -O dts /proc/device-tree
```

*Next in Stage 1: the root filesystem (fstab, mounts, read-only).*
