DESCRIPTION = "Root File System installer"

LICENSE = "MIT"

PR = "r0"

SRC_URI = " \
    file://formlabs-ascii-logo.txt \
    file://rootfs-installer.py \
    "

LIC_FILES_CHKSUM = " \
    file://formlabs-ascii-logo.txt;md5=089db123d61d97becff31b42126f0473 \
    "

S = "${WORKDIR}"

do_install() {
    install -d ${D}/usr/share
    install -m 0644 ${S}/formlabs-ascii-logo.txt ${D}/usr/share/formlabs-ascii-logo.txt
    install -d ${D}/usr/bin
    install -m 0755 ${S}/rootfs-installer.py ${D}/usr/bin/rootfs-installer
}

FILES_${PN} = " \
    /usr/share/formlabs-ascii-logo.txt \
    /usr/bin/rootfs-installer \
    "

DEPENDS += " python"
RDEPENDS_${PN} += "python"