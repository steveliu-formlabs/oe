FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://50-org.freedesktop.NetworkManager.rules"

do_install_append(){
    install -m 0755 ${S}/../50-org.freedesktop.NetworkManager.rules ${D}${sysconfdir}/polkit-1/rules.d
}
