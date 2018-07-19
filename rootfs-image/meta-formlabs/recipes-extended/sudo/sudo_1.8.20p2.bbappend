
python populate_packages_append(){
    postinst = """#!/bin/sh
echo "formlabs ALL=(ALL) ALL" >> $D/etc/sudoers
"""
    d.setVar(d.expand('pkg_postinst_${PN}'), postinst)
}
