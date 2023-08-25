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
from __future__ import annotations

import copy
import datetime
import os
import types
import unicodedata
from abc import ABC
from glob import glob
from logging import warning
from typing import Type
from django.db import models
from django.db.models import (
    ForeignKey,
    TextField,
    IntegerField,
    FloatField,
    DecimalField,
    Index,
    Manager,
    JSONField,
)
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext as _
from common.command import BiomAidCommand
from pytz import utc

from common import config
from smart_view.smart_expression import SmartExpression
from overoly.base import OverolyModel as Model


class ExtableManager(Manager):
    def __init__(self, fields_list):
        super().__init__()
        self.fields_list = fields_list

    def get_by_natural_key(self, *args):
        return super().get(**dict(zip(self.fields_list, args)))


class ExtableEngine(ABC):
    """A abstract class for engines that handle external table data"""

    TYPES: dict = {
        'string': (TextField, [], {}),
        'json': (JSONField, [], {}),
        'integer': (IntegerField, [], {}),
        'datetime': (DateTimeField, [], {}),
        'float': (FloatField, [], {}),
        'money': (DecimalField, [], {'max_digits': 14, 'decimal_places': 2}),
        'foreign_key': (ForeignKey, lambda prefix, col_def: [col_def['foreign_table']], {'on_delete': models.PROTECT}),
    }

    @staticmethod
    def create_model_class(schema: dict, prefix: str = '', module=None) -> Type[Model]:
        """Create a (Django) model from a descriptive Schema and put it in the extable (Django) application"""

        # Used as a template for model class
        class Meta:
            managed = False

        # Future model class attributes (will be in __dict__)
        attrs = {}

        # Add fields
        for fname, column_sch in schema['columns'].items():
            field_class = ExtableEngine.TYPES[column_sch['type']][0]
            args = ExtableEngine.TYPES[column_sch['type']][1]
            if callable(args):
                args = args(prefix, column_sch)
            kwargs = ExtableEngine.TYPES[column_sch['type']][2]
            if callable(kwargs):
                kwargs = kwargs(prefix, column_sch)
            kwargs = dict(
                {
                    'verbose_name': column_sch.get('src_column'),
                    'null': True,
                    'blank': True,
                },
                **kwargs,
            )
            attrs[fname] = field_class(
                *args,
                **kwargs,
            )

        # Add miscellaneous stuff
        attrs.update(
            {
                '__module__': module.__name__ if module else None,
                'Meta': Meta,
            }
        )

        def natural_key_def(self):
            return tuple(getattr(self, f) for f in list(schema.get('key')))

        # Add key columns as index, contraints and natural key
        if schema.get('key'):
            attrs['Meta'].indexes = [Index(fields=schema.get('key'))]
            attrs['Meta'].unique_together = [list(schema.get('key'))]
            attrs['natural_key'] = natural_key_def
            attrs['objects'] = ExtableManager(list(schema.get('key')))

        # Do create the model class
        model_class: Type[Model] = type(prefix + schema['name'], (Model,), attrs)

        # Add this model class to module
        if isinstance(module, types.ModuleType):
            setattr(module, prefix + schema['name'], model_class)

        return model_class

    @staticmethod
    def fieldname_build(title: str, field_names: list = None) -> str:
        """
        Build a valid unique (lowcase) identifier (less than 64 characters long) from a string (for instance a column title/header)
        It works by removing all special characters and replace them by best lowcase ASCII approximation

        :param title: String used to build the fieldname
        :param field_names: list of previously defined identifiers (default is a empty list)
        :return: a valid, unique identifier, less than 64 characters long
        """
        field_names = field_names or []

        # Create a simple valid identifier
        fname = ''
        for c in (char for char in unicodedata.normalize('NFD', title) if unicodedata.combining(char) == 0):
            if c.isalnum():
                fname += c.lower()
            elif not fname.endswith('_'):
                fname += '_'
        fname = fname[:60].strip('_')

        # Ensure uniqueness
        if fname in field_names:
            idx = 0
            while fname + str(idx) in field_names:
                idx += 1
            fname = fname + str(idx)

        return fname

    @staticmethod
    def columns_autodetect(filename: str, cfg: dict | None) -> dict:  # NOQA
        raise NotImplementedError("Static method columns_autodetect() must be overloaded.")

    @classmethod
    def schema_build(cls, cfg: dict = None, filename: str = None) -> dict:
        """
        Build a schema description from source (autodetected) and configuration.

        A Schema description is a dict with the following structure :
        - 'columns' :
            - 'type' : a valid type name (as a string)
            - 'data' : a valid expression (as a string)
        """
        cfg = cfg or {}

        schema = {'name': cfg['name'], 'columns': {}}

        # Add manually defined columns
        columns_cfg: dict = cfg.get('column', {})
        for column_name, column_def in columns_cfg.items():
            # Ensure configuration is valid
            ...

            # Verify 'data' expression (syntax & used columns names)
            data = column_def.get('data')
            if data:
                if isinstance(data, str):
                    expression = SmartExpression(data)
                    if not expression.syntax_is_valid(list(schema['columns'].keys())):
                        warning(_("Expression '{}' is invalid.").format(data))
                else:
                    warning(
                        _("data value for columns '{}' in table '{}' is not valid: {}").format(column_name, cfg['name'], repr(data))
                    )

            schema['columns'][column_name] = {
                'type': column_def.get('type', 'string'),
                'optional': column_def.get('optional', False),
            }
            if schema['columns'][column_name]['type'] == 'foreign_key':
                schema['columns'][column_name]['foreign_table'] = column_def.get('foreign_table', '__unknown__')
                schema['columns'][column_name]['foreign_column'] = column_def.get('foreign_column', 'pk')
            src_column = column_def.get('src_column')
            if src_column:
                schema['columns'][column_name]['src_column'] = src_column
            column_data = column_def.get('data')
            if column_data:
                schema['columns'][column_name]['data'] = column_data

        # Add key column(s)
        schema['key'] = cfg.get('key')

        return schema

    def __init__(self, schema: dict):
        self.schema = copy.deepcopy(schema)
        for colname, coldef in self.schema['columns'].items():
            expression_str = coldef.get('data')
            if expression_str:
                if isinstance(expression_str, str):
                    coldef['expr'] = SmartExpression(expression_str)

        # Check and set (primary) key
        ...
        self.key = schema['parser_opts'].get('key')
        self.preprocess = schema['parser_opts'].get('preprocess')

    def read_into_model(self, filename: str, model: Type[Model], log, progress) -> int:
        raise NotImplementedError("Method read_into_model() must be overloaded.")

    def update(self, log=None, progress=None, options={}):
        raise NotImplementedError("Method update() must be overloaded.")


class FileExtableEngine(ExtableEngine, ABC):
    @staticmethod
    def filename_match(filename: str) -> bool:  # NOQA: U101
        raise NotImplementedError("Static method filename_match() must be overloaded.")

    def update(self, log=None, progress=None, options={}):
        from extable.models import Table  # noqa

        # pprint(self.schema)
        # print('~' * 132)
        model = self.schema['model']
        table = Table.objects.get(table_name=model._meta.db_table)
        # print(table, table.update_ts)
        filename: str = self.schema['parser_opts'].get('filename')
        if (
            'path' in self.schema['parser_opts']
            and config.get('paths')
            and config.get('paths').get(self.schema['parser_opts']['path'])
        ):
            root = config.get('paths').get(self.schema['parser_opts']['path'], '')
        else:
            root = ''
        if filename.startswith('last:'):
            filenames = sorted(
                [(fn, datetime.datetime.fromtimestamp(os.stat(fn).st_mtime, tz=utc)) for fn in glob(root + filename[5:])],
                key=lambda a: a[1],
            )[-1:]
        elif filename.startswith('all:'):
            filenames = sorted(
                [(fn, datetime.datetime.fromtimestamp(os.stat(fn).st_mtime, tz=utc)) for fn in glob(root + filename[4:])],
                key=lambda a: a[1],
            )
        else:
            if os.path.exists(root + filename):
                filenames = [
                    (
                        root + filename,
                        datetime.datetime.fromtimestamp(os.stat(root + filename).st_mtime, tz=utc),
                    )
                ]
            else:
                log(BiomAidCommand.WARNING, _("  File '{}' does not exists. Skipping update.").format(root + filename))
                filenames = []
        # print(filenames)
        for filename in filenames:
            # print('=>', filename)
            if not table.update_ts or table.update_ts < filename[1] or options['force']:
                # print('====>', filename)
                if self.key is None or options['clear']:
                    # Empty the model/table
                    log(BiomAidCommand.FINE, _("  Emptying table..."))
                    model.objects.all().delete()
                else:
                    log(BiomAidCommand.FINE, _("  Keeping table records and updating using key {}...").format(repr(self.key)))
                log(BiomAidCommand.FINE, _("  Reading file: '{}'...").format(filename[0]))
                n_records = self.read_into_model(filename[0], model, log, progress)
                table.update_ts = filename[1]
                table.save()
                log(BiomAidCommand.INFO, _("  {} records read and stored.").format(n_records))
            else:
                log(BiomAidCommand.INFO, _("  File '{}' is older the extable data. Skipping.").format(filename[0]))

        # raise NotImplementedError("Method update() must be overloaded.")


repository: dict[str, Type[ExtableEngine]] = {}

try:
    from extable.engine_csv import CsvEngine

    repository['csv'] = CsvEngine
except ImportError as exception:
    print(_("Unable to initialize CSV extable engine: {}").format(repr(exception)))

try:
    from extable.engine_excel import ExcelEngine

    repository['excel'] = ExcelEngine
except ImportError as exception:
    print(_("Unable to initialize Excel extable engine: {}").format(repr(exception)))

try:
    from extable.engine_database import DatabaseEngine

    repository['database'] = DatabaseEngine
except ImportError as exception:
    print(_("Unable to initialize Database extable engine: {}").format(repr(exception)))

try:
    from extable.engine_tps import TpsEngine

    repository['tps'] = TpsEngine
except ImportError as exception:
    print(_("Unable to initialize TPS extable engine: {}").format(repr(exception)))
