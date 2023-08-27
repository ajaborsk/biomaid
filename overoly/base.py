"""
Overoly features
================

Add to every model:
- 'live' computed fields (aka parametric annotations), using string expressions and dependencies management
- flexible attributes for every field (customizable via configuration dict/file = toml)
- fine state-based & role-based permissions management :
    - at model level for record creation (without state management :-)
    - row level for record view and delete
    - field level (+ computed values constraints) for record update

Allows very customizable workflow management

Future (or optional ?):
- integrated ctime/atime/mtime/dtime management

Almost all features are implemented via metaclasses, thus computed at launch, without runnning overload
"""

from copy import deepcopy
from functools import partial

from django.db.models import Model, Manager, Expression, Value
from django.db.models.base import ModelBase


class ORolesMapper:
    def __init__(self, **kwargs):
        self.table_roles_map = {}
        self.row_roles_map = {}

    def row_roles_expression(self):
        return Value(',')


class OField:
    def __init__(self, *args, value=None, special=None):
        self.value = value
        self.special = special


class OverolyAllRecordsManager(Manager):
    pass


class OverolyRecordsManager(Manager):
    def __init__(self, *args, **kwargs):
        if 'annotations' in kwargs:
            if isinstance(kwargs['annotations'], dict):
                # Static (ie non parametric) annotations. Computed only from constants and fields values
                # 'annotations' argument must be a annotations dict :
                #   - each key is a identifier string (the annotation name)
                #   - each value is a Django ORM Expression (a instance of django.db.models.Expression)
                self._annotations_dict = deepcopy(kwargs['annotations'])
                self.annotations = lambda query_parameters: self._annotations_dict
            elif callable(kwargs['annotations']):
                # Dynamic (ie parametric) annotations. Computed from constants, fields values and parameters provided at request time
                # The callable should get a unique argument (the parameters dictionnary) and return a annotations dict (see above)
                self.annotations = kwargs['annotations']

            del kwargs['annotations']
        else:
            self.annotations = lambda query_parameters: {}
        self.query_parameters = {}
        super().__init__(*args, **kwargs)

    def setup(self, query_parameters):
        self.query_parameters = query_parameters
        return self

    def get_queryset(self):
        # if self.annotations:
        #     annotations = self.annotations(self.query_parameters)
        #     print(f"    {annotations=}")
        qs = super().get_queryset().annotate(**(self.annotations(self.query_parameters)))
        self.query_parameters = {}
        return qs


class OverolyModelMetaclass(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        # If this model is a abstract one, let it as it is
        if 'Meta' in attrs and getattr(attrs['Meta'], 'abstract', False) == True:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        print(f"Overoly: Creating class {name}")

        if 'OMeta' in attrs:
            for overoly_attrs in attrs['OMeta'].__dict__:
                if not overoly_attrs.startswith('__'):
                    print(f"  {overoly_attrs=}")

        def parametrize(formulae, params):
            return formulae

        annotations = {}
        for attr, val in attrs.items():
            if isinstance(val, OField):
                # print(f"  overoly_field: {attr} => {val}")
                formulae = val.value
                if isinstance(formulae, Expression):
                    annotations[attr] = partial(parametrize, formulae)
                elif callable(formulae):
                    annotations[attr] = formulae
                elif isinstance(formulae, str):
                    pass
                else:
                    pass

        def annotations_function_factory(things):
            def f(things, query_parameters):
                # Fake example for testing
                # annotations_dict = query_parameters
                # annotations_dict.update(things)
                return {name: val_func(query_parameters) for name, val_func in things.items()}

            return partial(f, things)

        if 'records' not in attrs:
            # Add the default Manager (see Django documentation)
            # if annotations:
            #     print(f"  {annotations=}")
            attrs['records'] = OverolyRecordsManager(annotations=annotations_function_factory(annotations))
        else:
            raise RuntimeError("Overoly Model cannot define a 'records' attribute (reserved for default manager)")
        if 'all_records' not in attrs:
            attrs['all_records'] = OverolyAllRecordsManager()
        else:
            raise RuntimeError("Overoly Model cannot define a 'all_records' attribute (reserved for base manager)")

        cl = super().__new__(cls, name, bases, attrs, **kwargs)
        return cl


class OverolyModel(Model, metaclass=OverolyModelMetaclass):
    # ctime = DateTimeField() # creation time
    # atime = DateTimeField() # activation time
    # mtime = DateTimeField() # modification time
    # dtime = DateTimeField() # delete/deactivation time

    class Meta:
        abstract = True

    @classmethod
    def get_attribute(cls, fieldname, attrname, default=None, context=None):
        return 'Attribut :-) !'

    def save(self, *args, **kwargs):
        print("Overoly: Checking rights (TODO)...")
        super().save(*args, **kwargs)
