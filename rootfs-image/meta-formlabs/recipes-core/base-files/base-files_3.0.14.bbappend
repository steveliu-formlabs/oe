
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://.bashrc"

do_install_append(){
    install -m 0755 ${S}/.bashrc ${D}${sysconfdir}/skel/.bashrc
}
