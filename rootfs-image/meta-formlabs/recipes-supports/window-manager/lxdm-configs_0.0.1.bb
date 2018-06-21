DESCRIPTION = "LXDM configuration file"

LICENSE = "MIT"

PR = "r0"

SRC_URI = " \
    file://default-display-manager \
    "

LIC_FILES_CHKSUM = " \
    file://default-display-manager;md5=4bae94cb522099bd57e4d0633f82cf53 \
    "

S = "${WORKDIR}"

do_install() {
    install -d ${D}/etc/X11/
    install -m 0644 ${S}/default-display-manager ${D}/etc/X11/default-display-manager
}

FILES_${PN} = " \
    /etc/X11/default-display-manager \
    "

DEPENDS += " lxdm"
