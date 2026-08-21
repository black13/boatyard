@echo off
rem boatyard — boot in a WINDOW (only works in a session with working graphics).
rem If no window appears, use run-qemu.cmd (text mode) instead.
cd /d D:\boatyard\qemu-run
"C:\Program Files\qemu\qemu-system-aarch64.exe" -M virt -cpu cortex-a57 -smp 4 -m 1024 -device ramfb -display sdl -kernel "images\Image" -drive "file=images\core-image-minimal-qemuarm64.ext4,format=raw,if=none,id=hd" -device virtio-blk-device,drive=hd -append "root=/dev/vda rw console=tty0 console=ttyAMA0,115200" -serial file:boot.log -monitor none
