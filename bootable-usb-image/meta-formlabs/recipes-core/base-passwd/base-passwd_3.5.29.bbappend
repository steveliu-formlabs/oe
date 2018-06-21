
python populate_packages_append(){
    postinst = """#!/bin/sh
sed -i "s/root.*/root::0:0:root:\/home\/root:\/usr\/bin\/rootfs-installer/g" $D${sysconfdir}/passwd
"""
    d.setVar(d.expand('pkg_postinst_${PN}'), postinst)
}
