
do_install_append(){
     sed -i "s/ExecStart.*/ExecStart=-\/sbin\/agetty -a root %I \$TERM/g" ${D}/lib/systemd/system/getty@.service
}