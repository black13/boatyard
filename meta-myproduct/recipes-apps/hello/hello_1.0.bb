SUMMARY = "hello — the daemon pattern (boring stuff §3)"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://hello.c file://hello.service"

S = "${WORKDIR}"

inherit systemd

SYSTEMD_SERVICE:${PN} = "hello.service"

# eng vs rel, one codebase two personalities (boring stuff §8):
CFLAGS:append = "${@bb.utils.contains('DISTRO_FEATURES','engmode',' -DENG','',d)}"

do_compile() {
    ${CC} ${CFLAGS} ${LDFLAGS} hello.c -o hello
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 hello ${D}${bindir}/hello
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 hello.service ${D}${systemd_system_unitdir}/hello.service
}
