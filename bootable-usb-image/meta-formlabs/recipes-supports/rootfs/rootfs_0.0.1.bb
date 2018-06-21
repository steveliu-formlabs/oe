DESCRIPTION = "The real root file system copy to disk"

LICENSE = "MIT"

PR = "r0"

SRC_URI = " \
    file://formlabs-rootfs-image-intel-corei7-64.ext4 \
    "

LIC_FILES_CHKSUM = " \
    file://formlabs-rootfs-image-intel-corei7-64.ext4;md5=THIS_IS_THE_DM5_FOR_ROOT_FILE_SYSTEM \
    "

S = "${WORKDIR}"

do_install() {
     install -d ${D}/
     install -m 0644 ${S}/formlabs-rootfs-image-intel-corei7-64.ext4 ${D}/formlabs-rootfs-image-intel-corei7-64.ext4
}

FILES_${PN} = " \
    /formlabs-rootfs-image-intel-corei7-64.ext4 \
    "
