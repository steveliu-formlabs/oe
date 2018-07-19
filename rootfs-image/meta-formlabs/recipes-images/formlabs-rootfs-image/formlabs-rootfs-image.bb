SUMMARY = "Formlabs Factory Calibration Image"

IMAGE_FEATURES += "splash package-management x11"

LICENSE = "MIT"

DISTRO_FEATURES += "wifi"

inherit core-image distro_features_check extrausers

SYSTEMD_DEFAULT_TARGET = "graphical.target"

REQUIRED_DISTRO_FEATURES = "x11"

EXTRA_USERS_PARAMS = "\
  useradd -P formlabs formlabs; \
  usermod -P root root; \
  usermod -s /bin/bash formlabs; \
  usermod -aG sudo formlabs; \
  usermod -aG cdrom formlabs; \
  usermod -aG audio formlabs; \
  usermod -aG video formlabs; \
  usermod -aG input formlabs; \
  usermod -aG netdev formlabs; \
  usermod -aG users formlabs; \
  usermod -aG docker formlabs; \
  "
