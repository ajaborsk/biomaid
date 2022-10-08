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
import logging
import os
from collections.abc import Mapping
from glob import glob
from os.path import exists

from django.conf import settings
from tomlkit.exceptions import ParseError
from tomlkit.toml_file import TOMLFile

logger = logging.getLogger(__name__)


def merge_dicts(d1, d2):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, Mapping):
            merge_dicts(d1[k], v)
        else:
            d1[k] = v


class Configuration(dict):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self._initialized = False
        self.settings = settings
        self.pyproject = TOMLFile(os.path.join(settings.BASE_DIR, 'pyproject.toml')).read()

        self._config = {}
        # Get all configurations
        configs = []
        for fn in ['local/config.toml'] + glob('local/config.d/*.toml'):
            try:
                configs.append(dict(TOMLFile(os.path.join(settings.BASE_DIR, fn)).read()))
            except ParseError as exc:
                logger.warning("Unable to parse TOML file '{}': {}".format(fn, exc))

        # Merge all configuration into one
        for config in configs:
            merge_dicts(self._config, config)

        # This very instance (not shared) configuration, at last
        fn = os.path.join(settings.BASE_DIR, 'instance_config.toml')
        if exists(fn):
            try:
                merge_dicts(self._config, dict(TOMLFile(fn).read()))
            except ParseError as exc:
                logger.warning("Unable to parse TOML file '{}': {}".format(fn, exc))

    def _initialize(self):
        self.initialized = True

    def get(self, item, default=None):
        if item == 'settings':
            return self.settings
        elif item == 'pyproject':
            return self.pyproject
        else:
            return self._config.get(item, default)

    def __getitem__(self, item):
        if item == 'settings':
            return self.settings
        elif item == 'pyproject':
            return self.pyproject
        else:
            return self._config.get(item, None)

    def __getattr__(self, item):
        return self._config.get(item, None)
