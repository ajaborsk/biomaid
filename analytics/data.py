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
# import sys
# from typing import Callable
# from types import FunctionType

from django.apps import apps
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from analytics.models import Data, DbDataSource


def register_data_processor(*args, **kwargs) -> bool:
    return apps.get_app_config('analytics').register_data_processor(*args, **kwargs)


def register_data_source(*args, **kwargs) -> bool:
    return apps.get_app_config('analytics').register_data_source(*args, **kwargs)


def get_data_timestamp(code: str, parameters=None):
    last_data = get_last_data(code, parameters)
    if last_data is not None:
        return last_data.timestamp
    else:
        # let's be explicit
        return None


def put_data(source, data, timestamp=None, parameters=None, link=None, context=None):
    timestamp = timestamp or now()
    parameters = parameters or {}
    link = link or {}
    context = context or {}

    data_rec = Data(
        source=source,
        data=data,
        timestamp=timestamp,
        parameters=parameters,
        link=link,
        context=context,
    )
    data_rec.save()


def get_last_data(code: str, parameters=None):
    if parameters is not None:
        qs = DbDataSource.objects.filter(code=code)
    else:
        qs = DbDataSource.objects.filter(code=code)
    if qs.exists():
        dqs = Data.objects.filter(source=qs[0].pk, parameters=parameters).order_by('-timestamp')
        if dqs.exists():
            return dqs[0]
        else:
            return None
    else:
        raise ValueError(_("Analytic data with '{code}' is not registred in the database.").format(code=code))


def get_data(data_id: str, all_params=None, log=None, progress=None, **parameters):
    """code is the datasource code, parameters"""
    all_params = all_params or {}
    data = None
    qs = DbDataSource.objects.filter(code=data_id)
    if qs.exists():
        data_source = qs[0]
        # Is there a last data with this parameters ?
        last_data = get_last_data(data_id, parameters)
        if last_data is not None:
            # Is this data still valid (=from the storage policy point of view) ?
            ...

        if data is None:
            # Let's compute it
            processor = apps.get_app_config('analytics').data_processors[data_source.processor_name]

            args = []
            for parameter_name, parameter_data in processor['parameters'].items():
                if parameter_name in all_params:
                    args.append(all_params[parameter_name])

            return processor['function'](*args)

        pass
    elif data_id in apps.get_app_config('analytics').data_processors:
        processor = apps.get_app_config('analytics').data_processors[data_id]

        args = []
        for parameter_name in processor['parameters']:
            if parameter_name in all_params:
                args.append(all_params[parameter_name])

        return processor['function'](*args)
    else:
        data_instance = apps.get_app_config('analytics').get_data_instance(data_id, log=log, progress=progress, **parameters)
        if not data_instance:
            raise ValueError(
                _("Analytic data with '{data_id}' is registred nor in engines registry nor in the database.").format(
                    data_id=data_id
                )
            )
        return data_instance.value
