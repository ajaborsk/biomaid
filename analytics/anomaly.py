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
from django.utils.timezone import now

from analytics.data import put_data

# A anomaly is a simple dict with the following keys :
# - 'code': str, the anomaly code (mandatory)
# - 'level': int, the anomaly level (mandatory), from 0 to 5
# - 'score': int, the anomaly relative 'weigh' (in a sense)
# - 'message': str, the anomaly message for the user (mandatory)


def print_anomalies(anomalies, indent=0):
    for anomaly in anomalies:
        print(' ' * indent, anomaly['code'], ' - ', anomaly['message'], sep='')


class AnomaliesStorage:
    def add(self, anomaly):
        pass


class JsonAnomaliesStorage(AnomaliesStorage):
    """Store anomalies in a JSON field in a model/table"""

    def __init__(self, record, column, append_mode=False):
        # If append_mode is True then do not replace the JSON field value but instead append
        #  new anomalies
        super().__init__()
        self.record = record
        self.column = column
        if append_mode:
            self.anomalies = getattr(self.record, self.column).get('anomalies') or []
        else:
            self.anomalies = []

    def add(self, anomaly):
        self.anomalies.append(anomaly)

    def __del__(self):
        if self.anomalies:
            self.anomalies.sort(key=lambda a: a['level'], reverse=True)
            max_level = self.anomalies[0]['level']
            setattr(
                self.record,
                self.column,
                {'max_level': max_level, 'anomalies': self.anomalies, 'timestamp': now().isoformat()},
            )
        else:
            setattr(self.record, self.column, {'max_level': 0, 'timestamp': now().isoformat()})
        self.record.save(update_fields=[self.column])


class DataSourceAnomaliesStorage(AnomaliesStorage):
    def __init__(self, datasource, aggregator, timestamp):
        super().__init__()
        self.datasource = datasource
        self.timestamp = timestamp
        self.aggregator = aggregator
        self.aggregate = {}
        self.records = []

    def add(self, record):
        self.records.append(record)

    def __del__(self):
        if self.records:
            aggregates = self.aggregator(self.records)
            for aggregate in aggregates:
                put_data(
                    self.datasource,
                    data=aggregate[1],
                    timestamp=self.timestamp,
                    parameters=aggregate[0],
                )


class AnomalySubCheckerMixin:
    """
    A class mixin for a checker that run all its subcheckers
    """

    subcheckers = tuple()

    def get_subdata(self):
        return []

    def subcheck(self, storage=None, verbosity=1):
        for subdata in self.get_subdata():
            storage = storage or self.storage
            for checker_class in self.subcheckers:
                try:
                    checker_class(subdata, storage=storage).check(verbosity)
                except Exception:
                    print(("Anomaly Checker {} raised a exception").format(checker_class))

    def check(self, verbosity=1):
        self.subcheck(verbosity=verbosity)
        return self


class AnomalyChecker:
    """
    A class for anomaly checker.

    Get a 'data' (a python object), a (optional) anomalies storage instance and some parameters (kwargs) at instanciation

    Calling 'check()' method (which must be overloaded) scan/analyse the data object and append anomalies into a
    (inside) list. This list can be accessed via the 'anomalies' property. If a storage object has been provided,
    anomalies are also send to this storage object.

    Subclasses must provide the following class attributes :
    - base_score : default score for anomalies detected by instances (but a score can be set for each anomaly)
    - code : a anomaly identifier (should be unique)
    - label : human-readable label/name for the anomaly detector
    - message : message template toward a user (
    - description : description (human-readable string) including the way anomalies are detected (used rules)
    - tips : a string that give user some tips to help him to resolve the detected anomal(y/ies)
    """

    base_score = 0

    def __init__(self, data, storage=None, **kwargs):
        self.data = data
        self.storage = storage
        self.kwargs = kwargs
        self._anomalies = []

    def add(self, **kwargs):
        """Create an anomaly and append it to the list/storage"""
        self._anomalies.append(
            {
                'code': self.code,
                'score': kwargs.get('score', self.base_score),
                'level': self.level,
                'message': self.message.format(**kwargs),
                'data': kwargs.get('data'),
            }
        )
        if self.storage:
            self.storage.add(self._anomalies[-1])

    def append(self, anomalies):
        """Append an already created anomalies list (from a subchecker for instance)"""
        for anomaly in anomalies:
            self._anomalies.append(anomaly)
            if self.storage:
                self.storage.add(anomaly)

    def check(self, verbosity=1):
        return self

    @property
    def anomalies(self):
        return self._anomalies


class SimpleAnomalyChecker(AnomalyChecker):
    base_score = 0
    code = ''
    label = ''
    message = ''
    description = ''
    tips = ''


class RecordAnomalyChecker(AnomalyChecker):
    """
    Anomaly checker that process a record (data provided at instanciation is a record as a dict).
    """
