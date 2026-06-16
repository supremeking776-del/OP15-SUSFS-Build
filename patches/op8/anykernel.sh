### AnyKernel3 Ramdisk Mod Script
## OnePlus 8 (instantnoodle / IN2013 / EX01) - ReSukiSU 4.19.157-perf+
properties() { '
kernel.string=ReSukiSU 4.19.157-perf+ for OnePlus 8 by GitHub Actions
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=instantnoodle
device.name2=OnePlus8
device.name3=IN2013
device.name4=instantnoodlep
device.name5=OnePlus8Pro
supported.versions=11 - 14
supported.patchlevels=
'; }
block=/dev/block/bootdevice/by-name/boot;
is_slot_device=0;
ramdisk_compression=auto;
patch_vbmeta_flag=auto;
. tools/ak3-core.sh;
write_boot;
