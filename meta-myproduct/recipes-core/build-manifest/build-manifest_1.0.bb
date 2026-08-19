SUMMARY = "Write the build manifest to /etc/build"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# Boring stuff §1: every shipped unit answers "what am I running?"
# Output format mirrors the platform.s /etc/build:
#
#   DISTRO = mydistro
#   DISTRO_VERSION = 4.0.29
#   IMAGE_BASENAME = myimage
#   MACHINE = imx8mp-lpddr4-evk
#   ----------------
#   meta-poky = HEAD:<commit>
#   meta-imx  = HEAD:<commit>
#   ...

inherit image-buildinfo

BUILDINFO_VARS:append = " DISTRO DISTRO_VERSION IMAGE_BASENAME MACHINE BUILDTYPE"
BUILDINFO_FILE = "build"

python do_buildinfo:append() {
    import subprocess
    lines = []
    for layer in (d.getVar("BBLAYERS") or "").split():
        try:
            rev = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=layer,
                stderr=subprocess.DEVNULL).decode().strip()
        except Exception:
            rev = "unknown"
        lines.append("%s = HEAD:%s" % (os.path.basename(layer.rstrip("/")), rev))
    path = os.path.join(d.getVar("IMAGE_ROOTFS"), "etc", "build")
    with open(path, "a") as f:
        f.write("\n".join(lines) + "\n")
}

FILES:${PN} = "/etc/build"
