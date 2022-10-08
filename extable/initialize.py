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
The init() function is called from the main urls.py module. So, when it's called, the databases
are fully initialized, which is not the case for AppConfig.ready() method.

This is important for tests as, at this point, the tests database need to be set up.
"""

import copy
import sys
from logging import warning
from typing import List

from django.apps import apps
from django.contrib import contenttypes
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations import migration
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

import extable
from common import config
from extable import engines
from extable.apps import EXTABLE_PREFIX

models_initialized = False


def update_models():

    schemas = {}

    # print(f"Databases {connections.databases}, DEFAULT:{DEFAULT_DB_ALIAS}, {conn._alias}")
    # Let's use the default database to store our external tables...
    connection = connections[DEFAULT_DB_ALIAS]

    # Hook for backends needing any database preparation
    connection.prepare_database()

    # to 'sync' between database (SQL) and configuration file ('extable.toml' for instance)
    # we build, for each table, at most 2 'definitions'/'descriptions' :
    #   one for each table in the database, stored in in tables_def_db
    #   and one for each table found in config file, stored in tables_def_cfg
    # a 'definition' is just a dict with one entry (key = 'columns') which is a dict which keys are
    # just a dict {'type': FIELDTYPE } where fieldtype is the name (as a string) of the Django field type
    # eg:
    # {'extable_extmytable':
    #     {'columns': {
    #         'first_field': {'type': 'TextField'}},
    #         'second_field': {'type': 'IntegerField'},
    #         'third_field': {'type': 'DateTimeField'},
    #         'fourth_field': {'type': 'FloatField'},
    #     }}
    # }
    #
    # If a table is found in the database *AND* in the configuration *AND* if its definitions are identicals :
    #   => table and its data are kept unchanged
    #
    # In the other cases, table is either deleted, created or (deleted and recreated)
    #

    # Get & build extable SQL tables descriptions
    tables_def_db = {}

    for table_name in filter(
        lambda tn: tn.startswith('extable_'),
        set(connection.introspection.table_names()) - {m._meta.db_table for m in apps.get_models()},
    ):
        tables_def_db[table_name] = {'columns': {}}
        curs = connection.cursor()
        columns_desc = connection.introspection.get_table_description(curs, table_name)
        for column_desc in columns_desc:
            tables_def_db[table_name]['columns'][column_desc.name] = {
                'type': connection.introspection.get_field_type(column_desc.type_code, column_desc)
            }
            # SQLite specific workaround (always return 'AutoField'...)
            if tables_def_db[table_name]['columns'][column_desc.name]['type'] == 'AutoField':
                tables_def_db[table_name]['columns'][column_desc.name]['type'] = 'BigAutoField'

    # Get & build extable config tables descriptions
    tables_def_cfg = {}
    tables_cfg: List[dict] = config.get('extable', {}).get('tables', [])
    for table_def in tables_cfg:
        engine_name = table_def.get('engine')
        if engine_name in engines.repository:
            engine_class = engines.repository[engine_name]

            # filename: str = table_def.get('filename', '__DATABASE__')
            # if 'path' in table_def and config.get('paths') and config.get('paths').get(table_def['path']):
            #     filename = config.get('paths').get(table_def['path'], '') + filename
            schema = engine_class.schema_build(table_def)
            if schema:
                model_class = engine_class.create_model_class(schema, EXTABLE_PREFIX, extable.models)

                schemas[table_def['name']] = schema
                schemas[table_def['name']]['parser_opts'] = copy.deepcopy(table_def)
                schemas[table_def['name']]['model'] = model_class
                schemas[table_def['name']]['engine'] = engine_class(schema)

                tables_def_cfg[model_class._meta.db_table] = {'columns': {}}
                for column in model_class._meta.fields:
                    django_type = column.get_internal_type()
                    if django_type == 'ForeignKey':
                        django_type = 'BigIntegerField'  # Temporary implementation ??
                    tables_def_cfg[model_class._meta.db_table]['columns'][column.attname] = {'type': django_type}
        else:
            warning(
                _("Extable {}{}: Engine not found in repository ({}). Availables engines : {}.").format(
                    EXTABLE_PREFIX,
                    table_def['name'],
                    engine_name,
                    ', '.join(list(engines.repository.keys())),
                )
            )

    # Tables registred in ContentType subsystem
    tables_def_ct = {
        'extable_' + tn: tn
        for tn in contenttypes.models.ContentType.objects.filter(~Q(model='table'), app_label='extable').values_list(
            'model', flat=True
        )
    }

    # Helper dict to access schemas with db_table keys
    db_name_schemas = {d['model']._meta.db_table: d for d in schemas.values()}

    # print(f"Extable.update_tables: db:{tables_def_db.keys()} cfg:{tables_def_cfg.keys()}")

    # Apply definition modifications to database

    # This looks simpler but DO NOT preserve tables_def_cfg.keys(), which is BAD in case of usage of foreign keys
    # <for table_name in set(tables_def_db.keys()) | set(tables_def_cfg.keys() | set(tables_def_ct.keys())):>
    # Same result as above BUT preserve tables_def_cfg order
    for table_name in list(tables_def_cfg.keys()) + list(
        (set(tables_def_db.keys()) | set(tables_def_ct.keys())) - set(tables_def_cfg.keys())
    ):
        # print(f"extable '{table_name}'...")
        if table_name not in tables_def_cfg:
            # table no longer needed, remove it from SQL database
            if table_name in tables_def_db:
                with connection.schema_editor(atomic=migration.atomic) as schema_editor:
                    print(_("  Deleting table: {} from database").format(table_name))
                    schema_editor.execute(schema_editor.sql_delete_table % {'table': table_name})
                    instances = extable.models.Table.objects.filter(table_name=table_name)
                    if instances.exists():
                        instances.delete()
            # And if it's in ContentType, remove it too
            if table_name in tables_def_ct:
                ct = contenttypes.models.ContentType.objects.filter(app_label='extable', model=tables_def_ct[table_name])
                if ct.count() > 0:
                    ct.delete()
        else:
            if table_name in tables_def_db:
                # Table is in both db and cfg
                if tables_def_db[table_name] != tables_def_cfg[table_name]:
                    # But they are different => delete & recreate
                    with connection.schema_editor(atomic=migration.atomic) as schema_editor:
                        print(_("  Deleting & recreating table: {}").format(table_name))
                        schema_editor.execute(schema_editor.sql_delete_table % {'table': table_name})
                        instances = extable.models.Table.objects.filter(table_name=table_name)
                        if instances.exists():
                            instances.delete()
                        extable.models.Table(
                            table_name=table_name,
                            definition={'columns': db_name_schemas[table_name]['columns']},
                        ).save()
                        schema_editor.create_model(db_name_schemas[table_name]['model'])
                        if not contenttypes.models.ContentType.objects.filter(
                            app_label='extable',
                            model=db_name_schemas[table_name]['model']._meta.model_name,
                        ).exists():
                            # For ContentType, create only if table does not exist (no structure recorded in this table)
                            ct = contenttypes.models.ContentType(
                                app_label='extable',
                                model=db_name_schemas[table_name]['model']._meta.model_name,
                            )
                            ct.save()
                else:
                    # Table in db and cfg and identical in db and cfg
                    # Only ensure table is in Table() model (only useful if table is corrupted)
                    # print(_("  Only checking: {}").format(table_name))
                    instances = extable.models.Table.objects.filter(table_name=table_name)
                    if not instances.exists():
                        extable.models.Table(table_name=table_name, definition={}).save()
                    # same for content_type
                    model_name = table_name.split('_', 1)[1]
                    instances = contenttypes.models.ContentType.objects.filter(app_label='extable', model=model_name)
                    if not instances.exists():
                        contenttypes.models.ContentType(app_label='extable', model=model_name).save()

            else:
                # table_name is in tables_def_cfg ONLY (new table) => do not delete anything
                with connection.schema_editor(atomic=migration.atomic) as schema_editor:
                    print(_("  Creating table: {}").format(table_name))
                    schema_editor.create_model(db_name_schemas[table_name]['model'])
                    extable.models.Table(table_name=table_name, definition={}).save()
                    model_name = db_name_schemas[table_name]['model']._meta.model_name
                    # print("*"*32, '\n', model_name)
                    ct = contenttypes.models.ContentType(app_label='extable', model=model_name)
                    ct.save()

    # Close opened connection to allow reset_db command to work as expected
    connection.close()

    # Keep track of schemas for future use (import...)
    apps.get_app_config('extable').schemas = schemas


# print(f"Extable Initialize: Here we are {sys.argv}")
# print(f"connections {connections} {connection}")
# print(f"{connections['default'].get_connection_params()}")
# print("ExtableConfig.ready...", sys.argv)


def init():
    # If the command isn't 'makemigrations' (to avoid creating wrong and useless migrations)
    if len(sys.argv) < 2 or (sys.argv[1] not in ('makemigrations', 'migrate', 'reset_db')):
        # print("ExtableConfig.ready (2)...", sys.argv[1])
        # Create extable dynamic models
        global models_initialized

        if not models_initialized:
            update_models()
            models_initialized = True
