DESCRIPTION = "Configuration files for root user"

LICENSE = "MIT"

PR = "r0"

SRC_URI = " \
    file://.xinitrc \
    file://.bashrc \
    file://.dmrc \
    "

LIC_FILES_CHKSUM = " \
    file://.xinitrc;md5=fb6f7726d07f37ab664e59ce197cf6ab \
    "

S = "${WORKDIR}"

do_install() {
     install -d ${D}/home/root
     install -m 0644 ${S}/.xinitrc ${D}/home/root/.xinitrc
     install -m 0644 ${S}/.bashrc ${D}/home/root/.bashrc
     install -m 0644 ${S}/.dmrc ${D}/home/root/.dmrc
}

FILES_${PN} = " \
    /home/root/.xinitrc \
    /home/root/.bashrc \
    /home/root/.dmrc \
    "