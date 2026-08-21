@echo off
rem boatyard — boot the qemuarm64 image in a window.
rem Run from D:\boatyard\qemu-run. The boot log + login appear in the window.
rem Keyboard grab: Ctrl+Alt to release mouse. Quit: close the window.
rem Serial console also mirrors to boot.log for diagnostics.
"C:\Program Files\qemu\qemu-system-aarch64.exe" -M virt -cpu cortex-a57 -smp 4 -m 1024 -device ramfb -display sdl -kernel "images\Image" -drive "file=images\core-image-minimal-qemuarm64.ext4,format=raw,if=none,id=hd" -device virtio-blk-device,drive=hd -append "root=/dev/vda rw console=tty0 console=ttyAMA0,115200" -serial file:boot.log -monitor none
