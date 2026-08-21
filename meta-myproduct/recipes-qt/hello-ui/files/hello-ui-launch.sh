#!/bin/sh
# Launch hello-ui against the Wayland compositor.
# Pin the platform so Qt never falls back to xcb (which fails: no X server).
export QT_QPA_PLATFORM=wayland
exec /usr/bin/hello-ui
