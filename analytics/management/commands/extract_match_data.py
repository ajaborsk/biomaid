#  Copyright (c)

#
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
"""
Django command to extract a dataset from the database in order to provide data to
learning/building record matching algorithm
"""
from django.core.management.base import BaseCommand
from django.db.models import Q

from analytics.match import RecordFetcher


def reference_read(filename):
    xy = []
    with open(filename) as f:
        for line in f.readlines():
            parts = list(map(lambda s: s.strip(), line.strip().split('#', 1)))
            if len(parts) == 2:
                content, comment = parts  # noqa
            else:
                content, comment = parts[0], ''  # noqa
            parts = list(map(lambda s: s.strip(), content.strip().split(',', 1)))
            if len(parts) == 2:
                src, dst = parts
            else:
                src, dst = parts[0], None

            # print(src, '->', dst, '#', comment)
            if dst is not None and dst[0] != '?':
                xy.append((src, dst))
    return xy


def splitter(commande_ligne_key):
    cmd, li = commande_ligne_key.split('-')
    return Q(commande=cmd, no_ligne_lc=li)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        # Add/update symlinks for applications documentation
        all = reference_read(options['filepath'])
        print(all[0][0].split('.'), end='')
        print(all[0][1].split('.'))
        # pprint(all[1:])
        # left_qs = apps.get_model('extable', "ExtCommande").records.all()
        # right_qs = apps.get_model('assetplusconnect', 'BFt1996').records.using('gmao').all()

        left_record_fetcher = RecordFetcher(models='extable.ExtCommande', key_builder=splitter)
        right_record_fetcher = RecordFetcher(
            models=['assetplusconnect.EnCours', 'assetplusconnect.BFt1996'],
            using='gmao',
            key_builder='nu_int',
        )

        # print(left_qs)

        for row in all[1:]:
            print(row[0], row[1])
            # cmd, li = row[0].split('-')
            print(left_record_fetcher.get(key=row[0]))
            print(right_record_fetcher.get(key=row[1]))
