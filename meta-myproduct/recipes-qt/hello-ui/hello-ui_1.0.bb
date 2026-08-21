SUMMARY = "hello-ui — the Qt5 QML app in miniature (mirrors the platform.s ui_app)"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

DEPENDS = "qtbase qtdeclarative qtquickcontrols"

SRC_URI = "file://main.cpp file://Main.qml file://qml.qrc file://hello-ui.pro file://hello-ui-launch.sh"

S = "${WORKDIR}"

inherit qmake5

do_install() {
    install -d ${D}${bindir}
    install -m 0755 hello-ui ${D}${bindir}/hello-ui
    install -m 0755 hello-ui-launch.sh ${D}${bindir}/hello-ui-launch
}

FILES:${PN} = "${bindir}/hello-ui"
RDEPENDS:${PN} += "qtdeclarative-qmlplugins qtdeclarative-plugins"
