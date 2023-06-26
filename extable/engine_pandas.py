from abc import ABC
from typing import Type, Union

import numpy as np
import pandas as pd
from numpy import dtype
from pandas import DataFrame, Int64Dtype, StringDtype, Series
from pandas.core.arrays.floating import Float64Dtype
from django.apps import apps
from django.db import models
from django.db.models import IntegerField
from django.utils.translation import gettext as _

from common import config
from common.command import BiomAidCommand


from extable.engines import FileExtableEngine, ExtableEngine


class DataFrameExtableEngine(FileExtableEngine, ABC):
    @staticmethod
    def schema_from_dataframe(df: Union[DataFrame, Series], cfg: dict = None) -> dict:
        cfg = cfg or {}
        schema: dict = {}
        for src_column in df.columns:
            column = ExtableEngine.fieldname_build(str(src_column), list(schema.keys()))
            if df[src_column].dtype == object:
                col_types = set()
                for val in df[src_column]:
                    col_types.add(type(val))
                if str in col_types:
                    guessed_type = 'string'
                else:
                    raise RuntimeError(
                        "Table {:s}, column '{:s}': Dont know which field type to use with {:s}".format(
                            cfg['name'], src_column, repr(col_types)
                        )
                    )
            elif df[src_column].dtype in {Int64Dtype(), dtype('int64')}:
                guessed_type = 'integer'
            elif df[src_column].dtype in {Float64Dtype(), dtype('float64')}:
                guessed_type = 'float'
            elif df[src_column].dtype in {
                dtype('datetime64[ns]'),
            }:
                guessed_type = 'datetime'
            elif df[src_column].dtype in {
                StringDtype(),
            }:
                guessed_type = 'string'
            else:
                raise RuntimeError(
                    "Table {:s}, column '{:s}': Dont know which field type to use with {:s}".format(
                        cfg['name'], src_column, repr(df[src_column].dtype)
                    )
                )
            schema[column] = {'type': guessed_type, 'src_column': src_column}
        return schema

    def dataframe_to_model(self, df: DataFrame, model: Type[models.Model], log, progress, **kwargs) -> int:
        """Read pandas DataFrame and records every line as a record in the given (Django) model. Returns the number of rows
        recorded.
        """
        n_records = 0

        # Normalize dataframe : normalize types, localize datetime and replace all kinds of NaN with a more pythonic None
        df = DataFrame(df.convert_dtypes())
        for column in df.columns:
            if df[column].dtype == dtype('datetime64[ns]'):
                df[column] = df[column].dt.tz_localize(config.settings.TIME_ZONE)
        df = df.fillna(np.nan).replace([np.nan], [None]).replace([pd.NA], [None])

        foreign_tables = {}
        for column, col_def in self.schema['columns'].items():
            # print(f"{col_def=}")
            if col_def['type'] == 'foreign_key':
                if col_def['foreign_table'] not in foreign_tables:
                    foreign_model = apps.get_model(col_def['foreign_table'])
                    field_type = int if isinstance(foreign_model._meta.get_field(col_def['foreign_column']), IntegerField) else str
                    foreign_tables[col_def['foreign_table']] = {'model': foreign_model, 'field_type': field_type}

        for src_index, src_record in df.iterrows():
            # Columns from file
            record_dict = {
                column: (src_record[col_def['src_column']] if not src_record[col_def['src_column']] is pd.NA else None)
                for column, col_def in self.schema['columns'].items()
                if 'src_column' in col_def and (col_def['src_column'] in df.columns or not col_def.get('optional', False))
            }

            computed = {}
            for column_name, column_def in self.schema['columns'].items():
                try:
                    if 'expr' in column_def:
                        computed[column_name] = column_def['expr'].python_eval(expr_vars=record_dict)
                except NameError as exc:
                    if not column_def.get('optional', False):
                        log(
                            BiomAidCommand.WARN,
                            _("NameError '{}' while evaluating '{}', namespace:{}").format(
                                str(exc), str(column_def['expr']), repr(record_dict)
                            ),
                        )
            # computed = {
            #     column: col_def['expr'].python_eval(expr_vars=record_dict)
            #     for column, col_def in self.schema['columns'].items()
            #     if 'expr' in col_def
            # }
            record_dict.update(computed)

            for column, col_def in self.schema['columns'].items():
                if col_def['type'] == 'foreign_key' and 'src_column' in col_def and col_def['src_column'] in df.columns:
                    foreign_object_qs = foreign_tables[col_def['foreign_table']]['model'].objects.filter(
                        **{col_def['foreign_column']: foreign_tables[col_def['foreign_table']]['field_type'](record_dict[column])}
                    )
                    if foreign_object_qs.count() == 1:
                        foreign_object = foreign_object_qs[0]
                    else:
                        log(
                            BiomAidCommand.FINE,
                            "Key not found for column {}: {} (type {}, count:{})".format(
                                column, repr(record_dict[column]), type(record_dict[column]), foreign_object_qs.count()
                            ),
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
            if n_records % 100 == 0:
                progress(n_records, len(df))

        return n_records
