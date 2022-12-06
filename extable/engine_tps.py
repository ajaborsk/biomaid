import os
import locale
from typing import Type
from datetime import datetime, timedelta
from decimal import Decimal

from tpsread.tpsread import TPS

from django.db import models
from django.db.models import IntegerField
from django.utils import timezone
from django.apps import apps

from extable.engines import FileExtableEngine

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def to_money(value):
    return float(value)


def to_code_uf(value):
    if value:
        return '{:04d}'.format(int(float(value)))


def to_no_reforme(value):
    if value:
        return "{:04d}/{:04d}".format(int(value) // 10000, int(value) % 10000)


def to_datetime(value):
    """Les dates sont stockées dans Clarion en nombre de jours depuis le 28/12/1800.
    Personne ne sait pourquoi."""
    return datetime(1800, 12, 28, tzinfo=timezone.utc) + timedelta(int(value))


def to_bool_from_str(value):
    if value:
        return {'OUI': True, 'NON': False}[value.upper()]


def get_tps_data(input_fn):
    tps = TPS(
        input_fn,
        encoding='iso8859-1',
        cached=True,
        check=True,
        current_tablename='UNNAMED',
    )
    records = []
    for record in tps:
        # remove 'XX:' prefix from keys
        rec = dict(zip([k.split(':')[1] for k in record.keys()], record.values()))
        # print(rec)
        records.append(rec)
        # if 'NUMERO' in rec and rec['NUMERO'] and int(rec['NUMERO']) in [20210157, 20210174, 20210206, 20210199]:
        #     print("    REC:", repr(rec))
    return records


class TpsEngine(FileExtableEngine):
    @staticmethod
    def filename_match(filename: str) -> bool:
        if filename.lower().endswith('.tps'):
            return True
        return False

    def columns_autodetect(filename: str, cfg: dict | None = None):
        cfg = cfg or {}
        schema: dict = {}
        if os.path.exists(filename):
            if filename.lower().endswith('.tps'):
                # read the file (1000 first rows)
                tps = TPS(
                    filename,
                    encoding='iso8859-1',
                    cached=True,
                    check=True,
                    current_tablename='UNNAMED',
                )
                for k, v in next(iter(tps)).items():
                    if isinstance(k, bytes):
                        k = k.decode('iso8859-1')
                    k = k.split(':')[1]
                    if isinstance(v, int):
                        guessed_type = 'integer'
                    elif isinstance(v, float):
                        guessed_type = 'float'
                    else:
                        guessed_type = 'string'
                    schema[k] = {'type': guessed_type, 'src_column': k}
                return schema

    def read_into_model(self, filename: str, model: Type[models.Model], msg_callback=None, **kwargs) -> int:
        n_records = 0

        records = get_tps_data(filename)

        foreign_tables = {}
        for column, col_def in self.schema['columns'].items():
            if col_def['type'] == 'foreign_key':
                if col_def['foreign_table'] not in foreign_tables:
                    foreign_model = apps.get_model(col_def['foreign_table'])
                    field_type = int if isinstance(foreign_model._meta.get_field(col_def['foreign_column']), IntegerField) else str
                    foreign_tables[col_def['foreign_table']] = {'model': foreign_model, 'field_type': field_type}

        for src_record in records:
            # Columns from file
            record_dict = {}
            for column, col_def in self.schema['columns'].items():
                if 'src_column' in col_def and col_def['src_column'] in src_record.keys():
                    if col_def['type'] == 'datetime':
                        record_dict[column] = to_datetime(src_record[col_def['src_column']])
                    elif col_def['type'] == 'integer':
                        record_dict[column] = int(src_record[col_def['src_column']])
                    elif col_def['type'] == 'money':
                        record_dict[column] = Decimal(float(src_record[col_def['src_column']])).quantize(Decimal('1.00'))
                    else:
                        v = src_record[col_def['src_column']]
                        if isinstance(v, str) and '\0' in v:
                            v = None
                        record_dict[column] = v

            computed = {
                column: col_def['expr'].python_eval(expr_vars=record_dict)
                for column, col_def in self.schema['columns'].items()
                if 'expr' in col_def
            }
            record_dict.update(computed)

            for column, col_def in self.schema['columns'].items():
                if col_def['type'] == 'foreign_key':
                    foreign_object_qs = foreign_tables[col_def['foreign_table']]['model'].objects.filter(
                        **{col_def['foreign_column']: foreign_tables[col_def['foreign_table']]['field_type'](record_dict[column])}
                    )
                    if foreign_object_qs.count() == 1:
                        foreign_object = foreign_object_qs[0]
                    else:
                        msg_callback(
                            "Key not found for column {}: {} (type {}, count:{})".format(
                                column, repr(record_dict[column]), type(record_dict[column]), foreign_object_qs.count()
                            )
                        )
                        foreign_object = None
                    record_dict[column] = foreign_object

            if self.key:
                records = model.objects.filter(**{k: record_dict[k] for k in self.key})
                # stdout.write("  key: {}".format(repr({k:record_dict[k] for k in self.key})))
                if records.count() == 1:
                    # Get record from database
                    record = records.get()
                    # stdout.write("  record found: {}".format(record))
                    for k, v in record_dict.items():
                        setattr(record, k, v)
                else:
                    # Create record from scratch
                    record = model(**record_dict)
            else:
                # Create record from scratch
                record = model(**record_dict)
            # Save record to the database
            record.save()
            n_records += 1
            if n_records % 100 == 0 and msg_callback is not None:
                msg_callback("  records written: {}".format(n_records), ending='\r')

        return n_records
