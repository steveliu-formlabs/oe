DESCRIPTION = "Configuration files for formlabs user"

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
    install -d ${D}/home/formlabs
    install -m 0666 ${S}/.xinitrc ${D}/home/formlabs/.xinitrc
    install -m 0666 ${S}/.bashrc ${D}/home/formlabs/.bashrc
    install -m 0666 ${S}/.dmrc ${D}/home/formlabs/.dmrc
}

FILES_${PN} = " \
    /home/formlabs/.xinitrc \
    /home/formlabs/.bashrc \
    /home/formlabs/.dmrc \
    "