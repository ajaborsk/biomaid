#  Copyright (c) 2020 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#  This file is part of the BiomAid distribution.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
import datetime
import json
import warnings

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from analytics.data import get_data_timestamp
from analytics.models import DataSource

ITERATION_LIMIT = 1000


class Command(BaseCommand):
    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)

        app_config = apps.get_app_config('analytics')
        qs = DataSource.objects.filter(Q(cloture__isnull=True) | Q(cloture__gt=now(), auto__isnull=False))

        datasources = {}
        todo = set()
        for datasource in qs:
            datasources[datasource.code] = datasource
            for auto_params in datasource.auto:
                if True:  # ... check schedule
                    todo.add((datasource.code, json.dumps(auto_params, sort_keys=True, separators=(',', ':'))))

        if verbosity > 2:
            self.stdout.write(
                _("Available engines :\n{}").format(''.join('    ' + str(k) + '\n' for k in app_config.data_processors.keys()))
            )
        if verbosity > 0:
            self.stdout.write(_("Analytics to process : {}.").format(len(todo)))

        iteration = 0
        done = False
        while iteration < ITERATION_LIMIT and not done and todo:
            iteration += 1
            done = True
            next_todo = set()
            while todo:
                datasource_code, auto_params_json = todo.pop()
                inputs = datasources[datasource_code].inputs or {}
                dependencies = set()
                for input_name, input_def in inputs.items():
                    if 'model' in input_def:
                        dependencies.add(input_def['model'])
                    elif 'source' in input_def:
                        dependencies.add(
                            (input_def['source'], json.dumps(input_def['params'], sort_keys=True, separators=(',', ':')))
                        )
                    else:
                        RuntimeError(
                            _("DataSource sources must have either a 'model' or a 'source' item for source '{}': {}").format(
                                input_name, repr(input_def)
                            )
                        )
                if not dependencies.intersection(todo | next_todo):  # Can I process it now or should I wait for a next iteration ?
                    datasource = datasources[datasource_code]
                    done = False  # At least one couple datasource/auto_params is being processed so will loop again
                    processor = app_config.data_processors.get(datasource.processor_name)
                    if isinstance(processor, dict) and 'function' in processor and callable(processor['function']):
                        last_data_timestamp = get_data_timestamp(datasource.code, json.loads(auto_params_json))
                        newest_dependency_timestamp = datetime.datetime(2000, 1, 1)
                        if last_data_timestamp is not None:
                            for dependency in dependencies:
                                if isinstance(dependency, tuple) and len(dependency) == 2:
                                    dependency_timestamp = get_data_timestamp(dependency[0], json.loads(dependency[1]))
                                    newest_dependency_timestamp = max(newest_dependency_timestamp, dependency_timestamp)
                                elif isinstance(dependency, str):
                                    ...
                                    pass
                                else:
                                    pass
                        if last_data_timestamp is None or last_data_timestamp < newest_dependency_timestamp:
                            if verbosity > 1:
                                self.stdout.write(_("  Processing : {}({}).").format(datasource_code, auto_params_json))
                                ...  # Process...
                            f = processor['function']
                            params = json.loads(auto_params_json)

                            # Check parameters signature
                            if verbosity > 2:
                                self.stdout.write(_("{} for {}").format(repr(params), repr(dict(processor['parameters']))))
                            try:
                                f(**dict(params, verbosity=verbosity))
                            except Exception as e:
                                warnings.warn(
                                    _(
                                        "Analytics data '{}' called with parameters {} (processor '{}') raised an exception: {}"
                                    ).format(datasource_code, auto_params_json, datasource.processor_name, repr(e))
                                )

                    else:
                        if verbosity > 0:
                            self.stdout.write(
                                self.style.ERROR(
                                    _("Unable to process analytics {} : processor is undefined and/or not callable : '{}'").format(
                                        datasource.code, processor
                                    )
                                )
                            )
                else:
                    # Keep datasource for a next iteration
                    next_todo.add((datasource_code, auto_params_json))
            todo = next_todo
