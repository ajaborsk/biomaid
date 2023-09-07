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
from logging import warning

from django.db.models import Model, Manager, Expression, Value
from django.db.models.base import ModelBase


class ORolesMapper:
    """
    Table roles sources :
      - constant (useless ?)
      - admin (from 'super_user' Django user attribute)
      - manager (from 'is_staff' Django user attribute)
      - global database query (typically : user has a particular role for at least one object in the database)
    """

    def __init__(self, const_roles=None, table_roles_map=None, row_roles_map=None):
        # TODO : Check parameters validity
        self.const_roles = const_roles or list()
        self.table_roles_map = table_roles_map or {}
        self.row_roles_map = row_roles_map or {}

    def table_roles_list(self, query_parameters: dict):
        return self.const_roles + list(code for code, expr in self.table_roles_map.items() if expr(query_parameters))

    def row_roles_expression(self, query_parameters: dict):
        """
        Returns a Django expression (to be used as a annotation value) that compute for every row a list of the user roles,
        as a string with a comma separated list of roles and starting and ending with a comma ','.
        eg : ',ADM,MAN,OWN,EDT,'
        To determine if the current user has a role (eg. Manager, code 'MAN'), one can test if the comma bracketed role code string (',MAN,') is
        a substring of this roles string
        """
        return Value(',' + ','.join(self.table_roles_list(query_parameters)) + ',')


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

        if 'OMeta' not in attrs:
            attrs['OMeta'] = type('OMeta', tuple(), {})

        attrs['OMeta']._config = None
        attrs['OMeta']._attributes = None
        attrs['OMeta']._roles_mapper = None

        for overoly_attrs in list(attrs['OMeta'].__dict__.keys()):
            if not overoly_attrs.startswith('_'):
                print(f"  {overoly_attrs=}")
                if overoly_attrs == 'config':
                    print("    " + repr(attrs['OMeta'].config))
                    attrs['OMeta']._config = attrs['OMeta'].config
                    del attrs['OMeta'].config
                elif overoly_attrs == 'roles_mapper':
                    if not hasattr(attrs['OMeta'], 'roles_field'):
                        attrs['OMeta'].roles_field = 'o_roles'
                    roles_mapper = attrs['OMeta'].roles_mapper
                    print("    " + repr(attrs['OMeta'].roles_mapper))
                    if isinstance(roles_mapper, ORolesMapper):
                        # This is a 'hard' definied roles mapper. Use it as it is
                        attrs['OMeta']._roles_mapper = attrs['OMeta'].roles_mapper
                        del attrs['OMeta'].roles_mapper
                    elif isinstance(roles_mapper, dict):
                        attrs['OMeta']._roles_mapper = ORolesMapper(**attrs['OMeta'].roles_mapper)
                        del attrs['OMeta'].roles_mapper
                    else:
                        warning()
                        pass
                    if attrs['OMeta'].roles_field is not None:
                        attrs[attrs['OMeta'].roles_field] = OField(value=attrs['OMeta']._roles_mapper.row_roles_expression)
                elif overoly_attrs == 'attributes':
                    attrs['OMeta']._attributes = attrs['OMeta'].attributes
                    del attrs['OMeta'].attributes
                else:
                    warning(f"Unknown OMeta attribute : {overoly_attrs}")

        def parametrize(formulae, params):
            return formulae

        annotations = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, OField):
                # print(f"  overoly_field: {attr} => {val}")
                formulae = attr_value.value
                if isinstance(formulae, Expression):
                    annotations[attr_name] = partial(parametrize, formulae)
                elif callable(formulae):
                    annotations[attr_name] = formulae
                elif isinstance(formulae, str):
                    pass
                else:
                    pass

        def annotations_function_factory(things):
            def f(things, query_parameters):
                return {name: val_func(query_parameters) for name, val_func in things.items()}

            return partial(f, things)

        if 'records' not in attrs:
            # Add the default Manager (see Django documentation)
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
