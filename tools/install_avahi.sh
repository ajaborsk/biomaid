#!/bin/sh

# Ce script est destiné à installer, configuer et lancer avahi pour une machine virtuelle miroir de
#  la machine de production.
# Il est prévu pour une machine virtuelle sous Linux Ubuntu (ou Debian)
# Il est à exécuter en mode su : sudo install_avahi.sh


apt-get install avahi-daemon
#sed -i.bak -e "s/^#domain-name=.*/domain-name=local/" /etc/avahi/avahi-daemon.conf
systemctl enable avahi-daemon
systemctl start avahi-daemon
