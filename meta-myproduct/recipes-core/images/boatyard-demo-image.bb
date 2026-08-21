SUMMARY = "boatyard demo image — Weston + Qt5 QML (the Garmin pattern in miniature)"
DESCRIPTION = "Weston compositor auto-launching the hello-ui QML app: the same \
Qt/Wayland architecture as ui_app, built clean-room on top of poky."
LICENSE = "MIT"

inherit core-image

IMAGE_FEATURES += "ssh-server-openssh weston"

IMAGE_INSTALL += " \
    qtbase qtdeclarative qtwayland qtwayland-plugins \
    hello hello-ui \
"
