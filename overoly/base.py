"""
Overoly features
================

Add to every model:
- 'live' computed fields (aka annotations), with string expressions and dependencies management
- flexible attributes for every field (customizable via configuration dict/file = toml)
- fine state-based & role-based permissions management :
    - model level for row creation (without state management :-)
    - row level for view and delete
    - field level (+ computed values limitations) for update

Allows very customizable workflow management

Future (or optional ?):
- integrated ctime/atime/mtime/dtime management

Almost all features are implemented via metaclasses, thus computed at launch, without runnning overload
"""

from django.db.models import Model, Manager
from django.db.models.base import ModelBase


class OverolyManager(Manager):
    pass


class OverolyModelMetaclass(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        if 'records' not in attrs:
            attrs['records'] = OverolyManager()
        else:
            raise RuntimeError("Overoly Model cannot define a 'records' attribute (reserved for default manager)")
        if 'all_records' not in attrs:
            attrs['all_records'] = OverolyManager()
        else:
            raise RuntimeError("Overoly Model cannot define a 'all_records' attribute (reserved for base manager)")
        cl = super().__new__(cls, name, bases, attrs, **kwargs)
        print(f"Overoly: Creating class {name}")
        return cl


class OverolyModel(Model, metaclass=OverolyModelMetaclass):
    # ctime = DateTimeField() # creation time
    # atime = DateTimeField() # activation time
    # mtime = DateTimeField() # modification time
    # dtime = DateTimeField() # delete/deactivation time

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        print("Overoly: Checking rights...")
        super().save(*args, **kwargs)
