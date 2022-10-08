#  Copyright (c) 2020 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#  This file is part of the BiomAid distribution.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This script build a ISO image with BiomAid auto-install on Ubuntu

  To use it :
  - Login as root
  - Setup a new virtual environment
  - Copy (or link) this file and mk-iso.yaml into a local directory
  - Install dependencies (see below)
  - Run it : python mk_iso.py

  Dependecies :
  - python-apt (install from AUR for ArchLinux, no PIP package available)
  - pyyaml (install from PIP)
"""

import os
from subprocess import run

image_file = 'ubuntu-20.04.4-live-server-amd64.iso'


def get_iso():
    if image_file not in os.listdir('.'):
        run(['wget', 'https://releases.ubuntu.com/20.04/ubuntu-20.04.4-live-server-amd64.iso'])


def mk_iso():
    run(['livefs-edit', image_file, 'biom-aid-on-' + image_file, '--action-yaml', 'mk-iso.yaml'])


if __name__ == '__main__':
    get_iso()
    mk_iso()
