#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from django import template

register = template.Library()


@register.filter(name="filter_gestiondata")
def filter_gestiondata(value, formatter):
    print(formatter)
    print(value)
    print(value.index)
    for key in formatter:
        print(key)
        if key == "date":
            # value = datetime(value, '%Y')
            value = value
            return value
        elif key == "string":
            value = value.lowercase
            print('string')
            return value
        else:
            return value
