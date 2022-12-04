import os
from io import StringIO
from logging import warning
from typing import Type

import pandas as pd
from django.db import models
from django.utils.translation import gettext as _
from numpy import dtype
from pandas import read_csv

from extable.engine_pandas import DataFrameExtableEngine


class CsvEngine(DataFrameExtableEngine):
    @staticmethod
    def filename_match(filename: str) -> bool:
        return filename.endswith('.csv')

    @staticmethod
    def columns_autodetect(filename: str, cfg: dict = None) -> dict:
        cfg = cfg or {}
        if os.path.exists(filename):
            if filename.endswith('.csv'):

                # read the file (1000 first rows)
                separator = cfg.get('separator', ',')
                df = read_csv(filename, engine='python', sep=separator, decimal=',', nrows=1000)

                # read again the file but try to parse dates for columns of type 'Object'
                df = read_csv(
                    filename,
                    quoting=1,
                    sep=separator,
                    engine='python',
                    nrows=1000,
                    parse_dates=list(filter(lambda i: df.dtypes[i] == dtype('O'), range(len(df.columns)))),
                    dayfirst=True,
                    decimal=',',
                    on_bad_lines='skip',
                )
                df_ct = df.convert_dtypes()
                return DataFrameExtableEngine.schema_from_dataframe(df_ct)

        # Nothing can be guessed...
        else:
            warning(_("File not found: '{}'. No schema guessing.").format(filename))
        return {}

    def read_into_model(self, filename: str, model: Type[models.Model], msg_callback=None, **kwargs) -> int:
        separator = self.schema['parser_opts'].get('separator', ',')

        # A dict that associate src_columns (= CSV columns headers) to columns id
        rev_colnames = {value['src_column']: col_id for col_id, value in self.schema['columns'].items() if 'src_column' in value}

        if self.preprocess is None:
            file = open(filename, encoding='utf8')
        elif self.preprocess == 'fix_nb_columns':
            n_columns = None
            with open(filename, encoding='utf8') as src:
                file = StringIO()
                for line in src.readlines():
                    line = line[:-1].replace('"', "'")  # remove trailing "\n" & remove '"'
                    # print(line)
                    if n_columns is None:
                        columns = line.split(separator)
                        n_columns = len(columns)
                        # print(f"n_columns: {n_columns}")
                    else:
                        columns = line.split(separator, maxsplit=n_columns - 1)
                    # print(f"  columns:{len(columns)} / {n_columns}")
                    line = '"' + ('"' + separator + '"').join(columns) + '"'
                    # print(line)
                    file.write(line + '\n')
                file.seek(0)
        else:
            warning(_("Unknown preprocess mode :'{}' ; Ignoring it.").format(self.preprocess))
            file = open(filename, encoding='utf8')

        # Get only columns names
        colnames = list(
            read_csv(
                file,
                sep=separator,
                quoting=1,
                quotechar='"',
                engine='python',
                nrows=10,
            ).columns
        )

        # Read the file
        file.seek(0)
        df = read_csv(
            file,
            sep=separator,
            quoting=1,
            quotechar='"',
            engine='python',
            parse_dates=[
                idx
                for idx, key in enumerate(colnames)
                if key in rev_colnames
                and 'src_column' in self.schema['columns'][rev_colnames[key]]
                and 'datetime' == self.schema['columns'][rev_colnames[key]]['type']
            ],
            dayfirst=True,
            decimal=',',
            on_bad_lines='warn',
        )
        df.fillna(value=pd.NA, inplace=True)
        df.replace(pd.NA, None, inplace=True)
        # print(df)
        n_records = self.dataframe_to_model(df, model, msg_callback, **kwargs)
        return n_records
