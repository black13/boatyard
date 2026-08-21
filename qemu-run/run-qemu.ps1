# boatyard — boot the qemuarm64 image locally on Windows, in a WINDOW.
# Run from D:\boatyard\qemu-run (PowerShell):
#   .\run-qemu.ps1
# The boot log + login prompt appear inside the QEMU window (tty0).
# Serial console also mirrors to boot.log for diagnostics.
# Keyboard grab: Ctrl+Alt to release mouse. Quit: close the QEMU window.

$QEMU = "C:\Program Files\qemu\qemu-system-aarch64.exe"

& $QEMU `
  -M virt -cpu cortex-a57 -smp 4 -m 1024 `
  -device ramfb -display sdl `
  -kernel "images\Image" `
  -drive "file=images\core-image-minimal-qemuarm64.ext4,format=raw,if=none,id=hd" `
  -device virtio-blk-device,drive=hd `
  -append "root=/dev/vda rw console=tty0 console=ttyAMA0,115200" `
  -serial "file:boot.log" `
  -monitor none
