@echo off
rem boatyard — boot the WESTON + Qt5 demo image in a window.
rem What you should see: kernel text, then the Weston desktop fills the
rem window, then the hello-ui QML app (sonar trace) auto-launches on top.
rem Mouse/keyboard are captured by the window (Ctrl+Alt releases).
rem Serial console mirrors to boot-demo.log for diagnostics.
cd /d D:\boatyard\qemu-run
"C:\Program Files\qemu\qemu-system-x86_64w.exe" -machine q35 -cpu IvyBridge -smp 4 -m 1024 -vga virtio -usb -device usb-tablet -kernel "images\bzImage-demo" -hda "images\boatyard-demo-image-qemux86-64.ext4" -append "root=/dev/sda rw console=ttyS0,115200 oprofile.timer=1 tsc=reliable no_timer_check rcupdate.rcu_expedited=1" -display sdl -serial file:boot-demo.log
