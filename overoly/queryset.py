from django.db.models import QuerySet


class OQuerySet:
    """NOT WORKING Django QuerySet wrapper/proxy"""

    def __init__(self, qs):
        assert isinstance(qs, QuerySet)
        self.__oqs = qs

    def __getattr__(self, attr):
        return getattr(self.__oqs, attr)
        return getattr(super(OQuerySet, self).__getattribute__('__oqs'), attr)

    def __iter__(self):
        return self.__ops.__iter__()
