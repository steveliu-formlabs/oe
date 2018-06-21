SUMMARY = "Formlabs Factory Calibration Image"

IMAGE_FEATURES += "splash package-management x11"

LICENSE = "MIT"

inherit core-image distro_features_check extrausers

SYSTEMD_DEFAULT_TARGET = "graphical.target"

REQUIRED_DISTRO_FEATURES = "x11"

#EXTRA_USERS_PARAMS = "\
#  useradd -P formlabs formlabs; \
#  usermod -P root root; \
#  "
