#!/usr/bin/env bash

set -e

# variables
BUILD_SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
BOOT_USB_DIR=${BUILD_SCRIPT_DIR}/bootable-usb-image
ROOTFS_DIR=${BUILD_SCRIPT_DIR}/rootfs-image

# Install yocto runtime dependencies
function install-packages {

    echo ""
    echo "+---------------------------------------------------------------------+"
    echo "|                                                                     |"
    echo "|                Install Yocto Dependencies                           |"
    echo "|                                                                     |"
    echo "+---------------------------------------------------------------------+"
    echo ""

    sudo apt-get update && sudo apt-get install -y gawk wget git-core diffstat unzip texinfo \
        gcc-multilib build-essential chrpath socat cpio python python3 python3-pip \
        python3-pexpect xz-utils debianutils iputils-ping tmux libncurses5-dev
}

function build-rootfs-image {

    echo ""
    echo "+---------------------------------------------------------------------+"
    echo "|                                                                     |"
    echo "|                  Build Root File System                             |"
    echo "|                                                                     |"
    echo "+---------------------------------------------------------------------+"
    echo ""

    # openembedded-core dir
    OE_CORE_DIR=${ROOTFS_DIR}/openembedded-core
    if [ ! -d ${OE_CORE_DIR} ]; then
        cd ${ROOTFS_DIR} && git clone git://git.openembedded.org/openembedded-core
    fi
    cd ${OE_CORE_DIR} && git checkout rocko

    # bitbake dir
    BITBAKE_DIR=${OE_CORE_DIR}/bitbake
    if [ ! -d ${BITBAKE_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.openembedded.org/bitbake
    fi
    cd ${BITBAKE_DIR} && git checkout 1.36

    # meta-openembedded dir
    OE_DIR=${OE_CORE_DIR}/meta-openembedded
    if [ ! -d ${OE_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.openembedded.org/meta-openembedded
    fi
    cd ${OE_DIR} && git checkout rocko

    # meta-intel dir
    INTEL_DIR=${OE_CORE_DIR}/meta-intel
    if [ ! -d ${INTEL_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-intel
    fi
    cd ${INTEL_DIR} && git checkout rocko

    # meta-intel-qat dir
    INTEL_QAT_DIR=${OE_CORE_DIR}/meta-intel-qat
    if [ ! -d ${INTEL_QAT_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-intel-qat
    fi
    cd ${INTEL_QAT_DIR} && git checkout rocko

    # meta-dpdk
    DPDK_DIR=${OE_CORE_DIR}/meta-dpdk
    if [ ! -d ${DPDK_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-dpdk
    fi
    cd ${DPDK_DIR} && git checkout sumo

    # meta-lxde
    LXDE_DIR=${OE_CORE_DIR}/meta-lxde
    if [ ! -d ${LXDE_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.toradex.com/meta-lxde.git
    fi
    cd ${LXDE_DIR} && git checkout rocko

    # meta-virtualization
    VIR_DIR=${OE_CORE_DIR}/meta-virtualization
    if [ ! -d ${VIR_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-virtualization
    fi
    cd ${VIR_DIR} && git checkout rocko

    # meta-browser
    BROW_DIR=${OE_CORE_DIR}/meta-browser
    if [ ! -d ${BROW_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://github.com/OSSystems/meta-browser.git
    fi
    cd ${BROW_DIR} && git checkout master

    # meta-formlbas
    FORMLABS_DIR=${OE_CORE_DIR}/meta-formlabs
    if [ -d ${FORMLABS_DIR} ]; then
        rm -rf ${FORMLABS_DIR}
    fi
    cp -r ${ROOTFS_DIR}/meta-formlabs ${OE_CORE_DIR}/

    # source
    cd ${OE_CORE_DIR} && source ./oe-init-build-env
    BUILD_DIR=${OE_CORE_DIR}/build

    # copy local.conf
    cp ${ROOTFS_DIR}/local.conf ${BUILD_DIR}/conf
    cp ${ROOTFS_DIR}/bblayers.conf ${BUILD_DIR}/conf

    # TODO: where is kernel config??

    # build image
    cd ${BUILD_DIR} && bitbake formlabs-rootfs-image
}


# 3) Build the bootable image
function build-bootable-usb-image {

    echo ""
    echo "+---------------------------------------------------------------------+"
    echo "|                                                                     |"
    echo "|                     Build Bootable USB                              |"
    echo "|                                                                     |"
    echo "+---------------------------------------------------------------------+"
    echo ""

    # openembedded-core dir
    OE_CORE_DIR=${BOOT_USB_DIR}/openembedded-core
    if [ ! -d ${OE_CORE_DIR} ]; then
        cd ${BOOT_USB_DIR} && git clone git://git.openembedded.org/openembedded-core
    fi
    cd ${OE_CORE_DIR} && git checkout rocko

    # bitbake dir
    BITBAKE_DIR=${OE_CORE_DIR}/bitbake
    if [ ! -d ${BITBAKE_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.openembedded.org/bitbake
    fi
    cd ${BITBAKE_DIR} && git checkout 1.36

    # meta-openembedded dir
    OE_DIR=${OE_CORE_DIR}/meta-openembedded
    if [ ! -d ${OE_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.openembedded.org/meta-openembedded
    fi
    cd ${OE_DIR} && git checkout rocko

    # meta-intel dir
    INTEL_DIR=${OE_CORE_DIR}/meta-intel
    if [ ! -d ${INTEL_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-intel
    fi
    cd ${INTEL_DIR} && git checkout rocko

    # meta-intel-qat dir
    INTEL_QAT_DIR=${OE_CORE_DIR}/meta-intel-qat
    if [ ! -d ${INTEL_QAT_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-intel-qat
    fi
    cd ${INTEL_QAT_DIR} && git checkout rocko

    # meta-dpdk
    DPDK_DIR=${OE_CORE_DIR}/meta-dpdk
    if [ ! -d ${DPDK_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-dpdk
    fi
    cd ${DPDK_DIR} && git checkout sumo

    # meta-lxde
    LXDE_DIR=${OE_CORE_DIR}/meta-lxde
    if [ ! -d ${LXDE_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.toradex.com/meta-lxde.git
    fi
    cd ${LXDE_DIR} && git checkout rocko

    # meta-virtualization
    VIR_DIR=${OE_CORE_DIR}/meta-virtualization
    if [ ! -d ${VIR_DIR} ]; then
        cd ${OE_CORE_DIR} && git clone git://git.yoctoproject.org/meta-virtualization
    fi
    cd ${VIR_DIR} && git checkout rocko

    # meta-formlbas
    FORMLABS_DIR=${OE_CORE_DIR}/meta-formlabs
    if [ -d ${FORMLABS_DIR} ]; then
        rm -rf ${FORMLABS_DIR}
    fi
    cp -r ${BOOT_USB_DIR}/meta-formlabs ${OE_CORE_DIR}/

    # copy rootfs
    RECIPE_DIR=${BOOT_USB_DIR}/openembedded-core/meta-formlabs/recipes-supports/rootfs
    ROOTFS_EXT4=${ROOTFS_DIR}/openembedded-core/build/tmp-glibc/deploy/images/intel-corei7-64/formlabs-rootfs-image-intel-corei7-64.ext4
    cp ${ROOTFS_EXT4} ${RECIPE_DIR}/rootfs

    # insert md5 checksum
    MD5=`md5sum ${ROOTFS_EXT4} | awk '{print $1}'`
    sed -i "s/THIS_IS_THE_DM5_FOR_ROOT_FILE_SYSTEM/${MD5}/g" ${RECIPE_DIR}/rootfs_0.0.1.bb

    # source
    cd ${OE_CORE_DIR} && source ./oe-init-build-env
    BUILD_DIR=${OE_CORE_DIR}/build

    # copy local.conf
    cp ${BOOT_USB_DIR}/local.conf ${BUILD_DIR}/conf
    cp ${BOOT_USB_DIR}/bblayers.conf ${BUILD_DIR}/conf

    # build image
    cd ${BUILD_DIR} && bitbake formlabs-bootable-usb-image

    # copy .iso to current directory
    BOOT_ISO=${BOOT_USB_DIR}/openembedded-core/build/tmp-glibc/deploy/images/intel-corei7-64/formlabs-bootable-usb-image-intel-corei7-64.iso
    cp ${BOOT_ISO} ${BUILD_SCRIPT_DIR}
}

function main {
    install-packages
    build-rootfs-image
    build-bootable-usb-image
}

# Run main function
main