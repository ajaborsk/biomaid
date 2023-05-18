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
from functools import reduce

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
                # if app_path not in ('local',):  # This one has a special treatment...
                if True:
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

        # Get tags from configuration files to allow conditional documentation parts
        # Use ..only:: directive to use it
        tags = ['django_app_' + appname.replace('.', '_') for appname in config.settings.INSTALLED_APPS] + [
            'option_' + option for option in config.get('options', {}).keys() if option
        ]

        sphinx_opts = reduce(lambda x, y: x + y, [['-t', tag] for tag in tags], [])

        subprocess.run(['make', 'clean'], cwd='docs')

        # We have to use shell=True here since we use shell variable to pass tag names to make & sphinx-build
        subprocess.run('SPHINXOPTS="' + ' '.join(sphinx_opts) + '" make html', cwd='docs', shell=True)
        subprocess.run('SPHINXOPTS="' + ' '.join(sphinx_opts) + '" make latexpdf', cwd='docs', shell=True)

        # Install html & pdf manual in /static
        ...
