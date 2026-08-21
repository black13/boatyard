# boatyard — boot the qemuarm64 image locally on Windows.
# Run from D:\boatyard\qemu-run (PowerShell):
#   .\run-qemu.ps1
# Quit QEMU with: Ctrl-A then X

$QEMU = "C:\Program Files\qemu\qemu-system-aarch64.exe"

& $QEMU `
  -M virt -cpu cortex-a57 -smp 4 -m 1024 `
  -kernel "images\Image" `
  -drive "file=images\core-image-minimal-qemuarm64.ext4,format=raw,if=none,id=hd" `
  -device virtio-blk-device,drive=hd `
  -append "root=/dev/vda rw console=ttyAMA0,115200" `
  -nographic -monitor none
