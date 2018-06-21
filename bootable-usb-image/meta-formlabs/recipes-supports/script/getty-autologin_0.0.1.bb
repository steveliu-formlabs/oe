DESCRIPTION = "System V Init Getty Auto Login"

LICENSE = "MIT"

PR = "r0"

SRC_URI = " \
    file://autologin \
    "

LIC_FILES_CHKSUM = " \
    file://autologin;md5=2c18d14db42191a2110361570c34a777 \
    "

S = "${WORKDIR}"

do_install() {
    install -d ${D}/usr/bin
    install -m 0755 ${S}/autologin ${D}/usr/bin/autologin
}

FILES_${PN} = " \
    /usr/bin/autologin \
    "
