import os
from logging import warning
from typing import Type

from pandas import read_excel

from django.utils.translation import gettext as _

from extable.engine_pandas import DataFrameExtableEngine
from overoly.base import OverolyModel as OModel


class ExcelEngine(DataFrameExtableEngine):
    @staticmethod
    def filename_match(filename: str) -> bool:
        return filename.endswith('.xlsx')

    @staticmethod
    def columns_autodetect(filename: str, cfg: dict = None) -> dict:
        cfg = cfg or {}
        if os.path.exists(filename):
            if filename.endswith('.xlsx'):
                # read the file (1000 first rows)
                header_row = cfg.get('header_row', 1) - 1
                df = read_excel(filename, header=header_row, nrows=2000)
                df_ct = df.convert_dtypes()
                return DataFrameExtableEngine.schema_from_dataframe(df_ct)
        # Nothing can be guessed...
        else:
            warning(_("File not found: '{}'. No schema guessing.").format(filename))
        return {}

    def read_into_model(self, filename: str, model: Type[OModel], log, progress) -> int:
        header_row = self.schema['parser_opts'].get('header_row', 1) - 1
        df = read_excel(filename, header=header_row)
        return self.dataframe_to_model(df, model, log, progress)
