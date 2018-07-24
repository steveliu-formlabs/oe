
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://defconfig"

KERNEL_DEFCONFIG_intel-corei7-64 = "${S}/defconfig"
