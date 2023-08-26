from zoneinfo import ZoneInfo

from django.apps import apps
from django.db import DatabaseError
from django.utils.translation import gettext as _
from common.command import BiomAidCommand

from extable.engines import ExtableEngine


class DatabaseEngine(ExtableEngine):
    @staticmethod
    def filename_match(filename: str) -> bool:
        if filename.endswith('__DATABASE__'):
            return True
        return False

    def update(self, log, progress, options={}):
        database = self.schema['parser_opts'].get('database', 'default')
        try:
            src_model = apps.get_model(self.schema['parser_opts'].get('model'))
        except LookupError:
            log(
                BiomAidCommand.WARNING,
                _("  source model {} not found. Ignoring this extable.").format(self.schema['parser_opts'].get('model')),
            )
            return
        columns = {
            column_val.get('src_column'): column_id
            for column_id, column_val in self.schema['parser_opts'].get('column', {}).items()
        }
        dst_model = apps.get_model('extable.Ext' + self.schema['parser_opts']['name'])
        try:
            qs = src_model.records.using(database).values(*columns.keys())
            qs._fetch_all()
        except DatabaseError:
            log(
                BiomAidCommand.WARNING,
                _("  Unable to connect to database '{}'. Ignoring this extable.").format(
                    self.schema['parser_opts'].get('database')
                ),
            )
            return
        print(f"Loaded !\n{options=}\n{self.schema['parser_opts']=}\n{database=}\n{src_model=}\n{columns=}")
        if self.schema['parser_opts'].get('key', []):
            log(
                BiomAidCommand.WARNING,
                _("  Primary Key not implemented. Ignoring this extable."),
            )
            return
        else:
            tz = ZoneInfo(self.schema['parser_opts'].get('timezone', 'UTC'))
            dst_model.records.all().delete()
            columns_desc = self.schema['parser_opts'].get('column', {})
            for src_record in qs:
                values = {}
                for dst_col, col_desc in columns_desc.items():
                    v = src_record[col_desc['src_column']]
                    if col_desc['type'] == 'datetime' and v is not None:
                        values[dst_col] = v.astimezone(tz)
                    else:
                        values[dst_col] = v

                # print(src_record)
                dst_record = dst_model(**values)
                dst_record.save()

        # log(BiomAidCommand.WARNING, _("  Database engine not yet implemented. Ignoring this extable."))
