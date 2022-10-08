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


@register.filter(name='has_group')
def has_group(user, group_name):
    # group = Group.objects.get(name=group_name)
    # group2 = str(group)
    # test = 'test'
    # print(group2)
    # print("name : ", group.name)
    # print("permissions : ", group.permissions)
    # print(user.groups.filter(name=group_name))
    return user.groups.filter(name=group_name).exists()
    # in user.groups.all()
