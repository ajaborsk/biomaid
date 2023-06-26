from _ast import Attribute
from copy import copy
from datetime import timedelta
import inspect
from types import CodeType
from typing import Any
from warnings import warn
from ast import parse, unparse, NodeVisitor
from dataclasses import dataclass, InitVar
from django.apps import AppConfig, apps
from django.utils.timezone import now
from common import config


@dataclass
class Schedule:
    """Schedule definition, initialize with onCalendar systemd format string"""

    cal_expr: InitVar[str]
    dow: int | None = -1  # Day Of Week, -1 in this field means 'never', 0 is monday, 6 is sunday
    year: int | None = None
    month: int | None = None
    day: int | None = None
    hour: int | None = 0
    minute: int | None = 0
    second: int | None = 0

    def __post_init__(self, cal_expr):
        cal_expr = str(cal_expr)
        print(f"Analyzing {cal_expr=}...")
        if cal_expr and cal_expr != 'never':
            for part in cal_expr.split(' '):
                # print(f" {part=}")
                if len(date_part := part.split('-')) == 3:
                    # Part is a date
                    if date_part[0] == '*':
                        pass  # Use default
                    else:
                        try:
                            self.year = int(date_part[0])
                            if self.year < 1970:
                                raise ValueError
                        except ValueError:
                            warn("Incorrect schedule time format '{}' (year), set to 'never'".format(cal_expr))
                            self.dow = -1
                            break
                    if date_part[1] == '*':
                        pass  # Use default
                    else:
                        try:
                            self.month = int(date_part[1])
                            if self.month < 1 or self.month > 12:
                                raise ValueError
                        except ValueError:
                            warn("Incorrect schedule time format '{}' (month), set to 'never'".format(cal_expr))
                            self.dow = -1
                            break
                    if date_part[2] == '*':
                        pass  # Use default
                    else:
                        try:
                            self.day = int(date_part[2])
                            if self.day < 1 or self.day > 31:
                                raise ValueError
                        except ValueError:
                            warn("Incorrect schedule time format '{}' (days), set to 'never'".format(cal_expr))
                            self.dow = -1
                            break
                elif len(time_part := part.split(':')) == 3:
                    # Part is a time
                    if time_part[0] == '*':
                        self.hour = None
                    else:
                        try:
                            self.hour = int(time_part[0])
                            if self.hour < 0 or self.hour > 23:
                                raise ValueError
                        except ValueError:
                            warn("Incorrect schedule time format '{}' (hours), set to 'never'".format(cal_expr))
                            self.dow = -1
                            break
                    if time_part[1] == '*':
                        self.minute = None
                    else:
                        try:
                            self.minute = int(time_part[1])
                            if self.minute < 0 or self.minute > 59:
                                raise ValueError
                        except ValueError:
                            warn("Incorrect schedule time format '{}' (minutes), set to 'never'".format(cal_expr))
                            self.dow = -1
                            break
                    if time_part[2] == '*':
                        self.second = None
                    else:
                        try:
                            self.second = int(time_part[2])
                            if self.second < 0 or self.second > 59:
                                raise ValueError
                        except ValueError:
                            warn("Incorrect schedule time format '{}' (seconds), set to 'never'".format(cal_expr))
                            self.dow = -1
                            break
                elif part == '*' or len(part) == 3:
                    # Part is DOW
                    self.dow = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6, '*': None}.get(
                        part.upper(), -1
                    )
                    if self.dow == -1:
                        warn("Incorrect schedule time format '{}' (day of week), set to 'never'".format(cal_expr))
                else:
                    warn("Incorrect schedule time format '{}', set to 'never'".format(cal_expr))
                    self.dow = -1
        else:
            print("  Empty schedule ==> Never")
        print(repr(self))

    def __repr__(self):
        if self.dow == -1:
            return "Schedule('never')"
        else:
            return (
                f"Schedule('{ {None:'*', 0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}[self.dow]}"
                f" {'*' if self.year is None else '{:04}'.format(self.year)}"
                f"-{'*' if self.month is None else '{:02}'.format(self.month)}"
                f"-{'*' if self.day is None else '{:02}'.format(self.day)}"
                f" {'*' if self.hour is None else '{:02}'.format(self.hour)}"
                f":{'*' if self.minute is None else '{:02}'.format(self.minute)}"
                f":{'*' if self.second is None else '{:02}'.format(self.second)}"
                "')"
            )

    def next_occurence(self, dt=None):
        if self.dow == -1:
            return None
        # replace None by now() if needed
        dt = dt or now()
        dt = dt.replace(microsecond=0)
        iters = 0
        while iters < 1000:
            # print(dt)
            if self.year is None or dt.year == self.year:
                if self.month is None or dt.month == self.month:
                    if (self.day is None or dt.day == self.day) and (self.dow is None or dt.weekday() == self.dow):
                        if self.hour is None or dt.hour == self.hour:
                            if self.minute is None or dt.minute == self.minute:
                                if self.second is None or dt.second == self.second:
                                    return dt
                                else:
                                    dt += timedelta(seconds=1)
                            else:
                                dt += timedelta(minutes=1)
                                dt = dt.replace(second=0)
                        else:
                            dt += timedelta(hours=1)
                            dt = dt.replace(minute=0, second=0)
                    else:
                        dt += timedelta(hours=24)
                        dt = dt.replace(hour=0, minute=0, second=0)
                else:
                    if dt.month < 12:
                        dt = dt.replace(month=dt.month + 1, day=1, hour=0, minute=0, second=1)
                    else:
                        dt = dt.replace(year=dt.year + 1, month=1, day=1, hour=0, minute=0, second=1)
            else:
                dt = dt.replace(year=dt.year + 1, month=1, day=1, hour=0, minute=0, second=1)
            iters += 1
        # Too many iterations... something went wrong, let's say there is no solution
        return None

    def previous_occurence(self, dt=None):
        if self.dow == -1:
            return None
        # replace None by now() if needed and remove a second to prevent return this very moment as a match
        dt = (dt or now()) - timedelta(seconds=1)
        dt = dt.replace(microsecond=0)
        iters = 0
        while iters < 1000:
            # print(dt)
            if self.year is None or dt.year == self.year:
                if self.month is None or dt.month == self.month:
                    if (self.day is None or dt.day == self.day) and (self.dow is None or dt.weekday() == self.dow):
                        if self.hour is None or dt.hour == self.hour:
                            if self.minute is None or dt.minute == self.minute:
                                if self.second is None or dt.second == self.second:
                                    return dt
                                else:
                                    dt -= timedelta(seconds=1)
                            else:
                                dt -= timedelta(minutes=1)
                                dt = dt.replace(second=59)
                        else:
                            dt -= timedelta(hours=1)
                            dt = dt.replace(minute=59, second=59)
                    else:
                        dt -= timedelta(hours=24)
                        dt = dt.replace(hour=23, minute=59, second=59)
                else:
                    if dt.month > 1:
                        dt = dt.replace(day=1, hour=23, minute=59, second=59)
                        dt -= timedelta(hours=24)
                    else:
                        dt = dt.replace(year=dt.year - 1, month=12, day=31, hour=23, minute=59, second=59)
            else:
                dt = dt.replace(year=dt.year - 1, month=12, day=31, hour=23, minute=59, second=59)
            iters += 1
        # Too many iterations... something went wrong, let's say there is no solution
        return None


class CollectNames(NodeVisitor):
    """Helper class to prepare data expressions"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.names = []

    def visit_keyword(self, node):
        # do not visit node.arg
        self.visit(node.value)

    def visit_Name(self, node):
        self.names.append(node.id)
        self.generic_visit(node)

    # Probably something to do with attributes. Let as is for now.
    def visit_Attribute(self, node: Attribute) -> Any:
        return self.generic_visit(node)


class AnalyticsEngine:
    """A engine is a"""

    @property
    def signature(self):
        return {}

    def __init__(self):
        # Last run timestamp
        self._last_run_ts = None
        # Engine ouputs/results
        self.values = {}

    def log(self, level, message, color=None):
        pass

    def run(self, verbosity=0, logger=None):
        pass


class DataProxy:
    """
    storage can be:
    - None (or 0 or [] or {} or False) => no storage at all
    - 'database' ==> storage in the database (history is possible)
    - 'attached_file' ==> storage in the file system, attached to a entity
    - 'field' ==> storage in a field of the model(types sould be compatibles)
    - 'alert' ==> storage in the alert system
    - ('model' ==> storage in a temporary table ?)

    The use of parameters needs a compatible storage system:
    - None
    - 'database'
    """

    def __init__(self, definition, **parameters):
        self.definition = definition
        self.parameters = {
            p: parameters.get(p, v.get('default'))
            for p, v in definition.get('parameters', {}).items()
            if p in parameters or 'default' in v
        }
        self.from_expr = definition['from']
        self.values = {}
        # print(f"{self.definition['id']} {parameters}")

    @property
    def value(self):
        try:
            names = {}
            # Try to get every names needed in the expression
            for dependency in self.definition['__names']:
                if dependency in apps.get_app_config('analytics').data_engines_cls:
                    # The name is a engine class
                    names[dependency] = apps.get_app_config('analytics').data_engines_cls[dependency]
                elif dependency in self.parameters:
                    # will be given by local paramters
                    pass
                else:
                    # If a 'data' is used alone (no parameters), it looks like a variable in the expression (not like a function)
                    data_instance = apps.get_app_config('analytics').get_data_instance(dependency)
                    # If a 'data' is used as a function (parameters)
                    # TODO
                    # data_instance = apps.get_app_config('analytics').get_data_instance(dependency, the_data_instance_parameters)
                    # use the data value in the expression
                    if data_instance:
                        names[dependency].value
                    else:
                        warn("Undefined dependency: {} in analytics data '{}'".format(dependency, self.definition['id']))
                        return None

            names = copy(apps.get_app_config('analytics').data_engines_cls)
            v = eval(self.from_expr, names, self.parameters)
        except NameError as exp:
            warn("Error evaluating '{}' data : {}".format(self.definition['id'], str(exp)))
            return None
        return v


class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # New system
        self.data_def_registry = {}
        # self.data_processor_def_registry = {}
        self.data_engines = {}
        self.data_engines_cls = {}
        # kind of caching
        self.datasource_instances = {}
        self.data_instances = {}
        # Old system
        self.data_processors = {}
        self.data_sources = {}

    # Old system
    def register_data_processor(self, name: str, f: CodeType) -> bool:
        if name not in self.data_processors:
            self.data_processors[name] = {'function': f, 'parameters': inspect.signature(f).parameters}
            return True
        else:
            return False

    # Old system
    def register_data_source(self, name: str, f: CodeType) -> bool:
        if name not in self.data_source:
            self.data_sources[name] = {'function': f, 'parameters': inspect.signature(f).parameters}
            return True
        else:
            return False

    # New system
    def register_data_engine(self, name: str, c: type) -> bool:
        if name not in self.data_engines:
            self.data_engines[name] = {'class': c, 'parameters': inspect.signature(c).parameters}
            self.data_engines_cls[name] = c
            return True
        else:
            return False

    def get_data_engine(self, name: str, *args, **kwargs):
        if name in self.data_engines:
            # TODO: ensure args and kwargs are correct
            return self.data_engines[name]['class'](*args, **kwargs)
        else:
            return None

    def get_data_processor(self, dp_id):
        if dp_id in self.datasource_instances:
            return self.datasource_instances[dp_id]
        elif dp_id in self.data_processor_def_registry:
            return AnalyticsEngine(self.data_processor_def_registry[dp_id])
        else:
            warn("unable to get data processor with id {}".format(dp_id))
            return None

    def get_data_instance(self, name: str, **kwargs):
        if name in self.data_def_registry:
            # TODO: some sort of caching (do not forget the args !) ?
            return DataProxy(self.data_def_registry[name], **kwargs)
        else:
            return None

    def register_data_id(self, data_id: str, data_def: dict):
        # ensure data id is set in the definition
        data_def['id'] = data_id
        try:
            # ensure 'from' attribute correct syntax
            tree = parse(data_def['from'])
            names_extractor = CollectNames()
            names_extractor.visit(tree)
            data_def['__names'] = names_extractor.names
            data_def['from'] = unparse(tree)
            data_def['__schedule'] = Schedule(data_def.get('schedule', ''))
            print(f"  from={unparse(tree)}\n  names={data_def['__names']}")
        except KeyError:
            warn("analytics '{}' has no 'from' attribute !".format(data_id))
            raise ValueError
        except SyntaxError as exp:
            warn("analytics '{}' has incorrect 'from' attribute: {}".format(data_id, str(exp)))
            raise ValueError
        if data_id in self.data_def_registry:
            warn("Data processor output already in registry: {}".format(data_id))
            raise ValueError
        else:
            self.data_def_registry[data_id] = data_def

    def ready(self):
        for cfg_data_def in config.get('analytics.data', []):
            data_def = dict(cfg_data_def)
            # print(f'{dict(data_def)}')
            data_id = data_def.get('id')
            if data_id is None:
                warn("Analytics data has no id ! ({})".fromat(str(dict(data_def))))
                break
            else:
                print(f"Data '{data_id}':")
                try:
                    data_def['def_source'] = 'config'
                    self.register_data_id(data_id, data_def)
                except ValueError:
                    pass

        if config.settings.DEBUG:
            print("data defs:")
            for dd, d_def in self.data_def_registry.items():
                print(f"  {dd}: {dict(d_def)}")
