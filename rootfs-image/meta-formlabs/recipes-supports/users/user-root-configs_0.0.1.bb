DESCRIPTION = "Configuration files for root user"

LICENSE = "MIT"

PR = "r0"

SRC_URI = " \
    file://.xinitrc \
    file://.bashrc \
    file://.dmrc \
    "

LIC_FILES_CHKSUM = " \
    file://.xinitrc;md5=e9b8f9e70efa254defdf18a9cdb13287 \
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