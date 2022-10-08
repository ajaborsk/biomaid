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
import os.path
import subprocess

from django.apps import apps
from django.core.management.base import BaseCommand

from common import config


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Add/update symlinks for applications documentation
        for app in apps.get_app_configs():
            # For every registred (django) application
            if app.path.startswith(config.settings.BASE_DIR):
                # If it's in BIOM_AID directory (which is probably not the best criteria...)
                app_path = app.path[len(config.settings.BASE_DIR) + 1 :]  # NOQA
                if app_path not in ('local',):  # This one has a special treatment...
                    for doc_name in (
                        'sysadmin',
                        'admin',
                        'internals',
                        'dev',
                        'user',
                    ):  # Should'nt get these from settings ?
                        subprocess.run(
                            ['rm', '-Rf', os.path.join(doc_name, 'doc_' + app_path)],
                            cwd='docs',
                        )
                        if os.path.exists(os.path.join(app_path, 'docs', doc_name)):
                            self.stdout.write(f"Linking {os.path.join(app_path, doc_name)}...")
                            subprocess.run(
                                [
                                    'ln',
                                    '-sf',
                                    os.path.join('../..', app_path, 'docs', doc_name),
                                    os.path.join(doc_name, 'doc_' + app_path),
                                ],
                                cwd='docs',
                            )
                            # Append link to main doc index...
                            ...

        # Build the documentation
        subprocess.run(['make', 'html'], cwd='docs')
        subprocess.run(['make', 'latexpdf'], cwd='docs')

        # Install html & pdf manual in /static
        ...
