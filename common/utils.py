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
"""
Utilitaires divers :
--------------------

  - Exportation
"""
from __future__ import annotations

from abc import ABC
from html.parser import HTMLParser
from logging import warning

from django.apps import apps
from django.db.models import QuerySet, Model
from django.http import HttpRequest
from pandas import DataFrame
from xlsxwriter import Workbook


class HTMLFilter(HTMLParser, ABC):
    """
    A simple no dependency HTML -> TEXT converter.
    Usage:
          str_output = HTMLFilter.convert_html_to_text(html_input)
    """

    def __init__(self, *args, **kwargs):
        self.text = ''
        super().__init__(*args, **kwargs)

    def handle_data(self, data):
        self.text += data

    @classmethod
    def convert_html_to_text(cls, html: str) -> str:
        f = cls()
        f.feed(html)
        return f.text.strip()


class DataWorksheet:
    def __init__(
        self: DataWorksheet,
        wb: Workbook,
        ws_name: str,
        formats: None | dict = None,
        converters: None | dict = None,
    ) -> None:
        self.wb = wb
        self.ws = self.wb.add_worksheet(ws_name)
        self.formats = formats or {}
        self.columns = list(self.formats.keys())
        self.converters = converters or {}
        self.last_row = -1

    def prepare(self: DataWorksheet) -> DataWorksheet:
        current_col_idx = 0
        for column in self.columns:
            self.ws.set_column(
                current_col_idx,
                current_col_idx,
                width=self.formats.get(column, {}).get('width', 10),
                cell_format=self.wb.add_format(
                    dict(
                        {
                            'text_wrap': True,
                            'bottom': 1,
                            'top': 1,
                            'left': 1,
                            'right': 1,
                            'text_v_align': 2,
                        },
                        **self.formats.get(column, {}).get('cell', {}),
                    )
                ),
            )
            header_format = self.wb.add_format(
                dict(
                    {
                        'text_wrap': False,
                        'bottom': 1,
                        'top': 1,
                        'left': 1,
                        'right': 1,
                        'text_v_align': 2,
                        'text_h_align': 2,
                        'bold': True,
                        'bg_color': '#CCEEFF',
                    },
                    **self.formats.get(column, {}).get('header', {}),
                )
            )
            self.ws.write(
                0,
                current_col_idx,
                self.formats.get(column, {}).get('title', column.title()),
                header_format,
            )
            current_col_idx += 1
        self.last_row = 0
        return self

    def put_data_frame(self: DataWorksheet, data_frame: DataFrame, check_columns=True) -> DataWorksheet:
        if check_columns:
            if set(data_frame.columns) - set(self.columns):
                warning(f"Some DataFrame columns not found : {set(data_frame.columns) - set(self.columns)} in {set(self.columns)}")
        current_row_idx = self.last_row + 1
        for idx, row in data_frame.iterrows():
            current_col_idx = 0
            for column in self.columns:
                cell_value = row[column]
                self.ws.write(current_row_idx, current_col_idx, cell_value)
                current_col_idx += 1
            current_row_idx += 1
        self.last_row = current_row_idx - 1
        return self

    def put_query_set(self: DataWorksheet, query_set: QuerySet) -> DataWorksheet:
        current_row_idx = self.last_row + 1
        for instance in query_set:
            current_col_idx = 0
            for column in self.columns:
                cell_value = getattr(instance, column)
                if isinstance(cell_value, Model):
                    cell_value = str(cell_value)
                else:
                    if column in self.converters:
                        cell_value = self.converters[column](cell_value)
                self.ws.write(current_row_idx, current_col_idx, cell_value)
                current_col_idx += 1
            current_row_idx += 1
        self.last_row = current_row_idx - 1
        return self

    def put_row(self: DataWorksheet, row_data: dict) -> DataWorksheet:
        current_row_idx = self.last_row + 1
        current_col_idx = 0
        for column in self.columns:
            cell_value = row_data.get(column)
            self.ws.write(current_row_idx, current_col_idx, cell_value)
            current_col_idx += 1
        self.last_row = current_row_idx
        return self

    def finalize(self: DataWorksheet) -> DataWorksheet:
        if self.last_row > 0 and len(self.columns) > 0:
            self.ws.autofilter(0, 0, self.last_row, len(self.columns) - 1)
        self.ws.freeze_panes(1, 0)
        return self


def url_prefix_parse(kwargs: dict, request: HttpRequest, user_roles: set()):
    if 'url_prefix' in kwargs:
        url_prefix = kwargs['url_prefix']
    else:
        # the url_prefix is not given via kwargs
        # So try to guess from url
        # This part is used for error pages (not handled via django resolver)
        url_prefix = request.path.split('/')[1]

    if url_prefix == 'default':
        # Fallback...
        url_prefix = list(apps.app_configs['common'].configs.keys())[0] + '-' + list(apps.app_configs['common'].portals.keys())[0]

    portal_name, config_name, prefix_theme_name = (url_prefix.split('-', 2) + [None, None])[:3]

    available_portal_names = list(apps.app_configs['common'].portals.keys())

    # provided portal name
    portal = apps.app_configs['common'].portals.get(portal_name)

    # Is provided portal name ok ?
    if portal is not None and set(portal['permissions']).isdisjoint(user_roles):
        portal = None

    # Let's try to find a better one
    if portal is None:
        for tentative_portal_name in available_portal_names:
            if not set(apps.app_configs['common'].portals[tentative_portal_name]['permissions']).isdisjoint(user_roles):
                portal_name = tentative_portal_name
                portal = apps.app_configs['common'].portals.get(portal_name)
                break
    # idx = 0
    # while portal is None and idx < len(available_portal_names):
    #     if not set(apps.app_configs['common'].portals[available_portal_names[idx]]['permissions']).isdisjoint(user_roles):
    #         portal_name = available_portal_names[idx]
    #         portal = apps.app_configs['common'].portals.get(portal_name)
    #     idx += 1

    # Fallback in case no suitable portal is found
    if portal is None:
        portal_name = available_portal_names[0]
        portal = apps.app_configs['common'].portals.get(portal_name)

    local_config = apps.app_configs['common'].configs.get(config_name)
    if local_config is None:
        config_name = list(apps.app_configs['common'].configs.keys())[0]
        local_config = apps.app_configs['common'].configs.get(config_name)
    local_config['name'] = config_name

    theme_name = prefix_theme_name or portal.get('theme-name') or local_config.get('default-theme')

    # rebuild url_prefix with corrected values
    url_prefix = portal_name + '-' + config_name + ('' if prefix_theme_name is None else ('-' + prefix_theme_name))

    return url_prefix, portal, local_config, prefix_theme_name, theme_name


def url_prefix_make():
    return 'geqip-chuap'
