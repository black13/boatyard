@echo off
rem boatyard — boot the qemuarm64 image as TEXT in this console window.
rem No graphics needed at all. Works on any Windows session (RDP included).
rem Watch it boot to "qemuarm64 login:" -> root (no password) -> hello
cd /d D:\boatyard\qemu-run
"C:\Program Files\qemu\qemu-system-aarch64.exe" -M virt -cpu cortex-a57 -smp 4 -m 1024 -kernel "images\Image" -drive "file=images\core-image-minimal-qemuarm64.ext4,format=raw,if=none,id=hd" -device virtio-blk-device,drive=hd -append "root=/dev/vda rw console=ttyAMA0,115200" -nographic -monitor none
pause
