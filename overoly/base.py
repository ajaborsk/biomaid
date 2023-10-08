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

from django.db.models import Model, Manager, Expression, Value, When, Case, Field, Q, Exists, OuterRef
from django.db.models.functions import Concat
from django.db.models.base import ModelBase

from polyexpr.polyexpr import PolyExpr, django_orm_expression


class ORolesMapper:
    """
    Table roles sources :
      - constant (useless ?)
      - admin (from 'super_user' Django user attribute)
      - manager (from 'is_staff' Django user attribute)
      - global database query (typically : user has a particular role for at least one object in the database)
    """

    @staticmethod
    def is_superuser(u):
        try:
            return u.is_superuser
        except AttributeError:
            return False

    @staticmethod
    def is_staff(u):
        try:
            return u.is_staff
        except AttributeError:
            return False

    @staticmethod
    def q(*args, **kwargs):
        return Q(*args, **kwargs)

    @staticmethod
    def in_scope(user, roles_list, **kwargs):
        """Preliminary implementation, only for french healthcare structure"""
        from common.models import UserUfRole

        axis1_filters_list = []
        if 'uf' in kwargs:
            axis1_filters_list.append(Q(uf__isnull=True) | Q(uf=OuterRef(kwargs['uf'])))
            axis1_filters_list.append(Q(service__isnull=True) | Q(service=OuterRef(kwargs['uf'] + '__service')))
            axis1_filters_list.append(
                Q(centre_responsabilite__isnull=True) | Q(centre_responsabilite=OuterRef(kwargs['uf'] + '__centre_responsabilite'))
            )
            axis1_filters_list.append(Q(pole__isnull=True) | Q(pole=OuterRef(kwargs['uf'] + '__pole')))
            axis1_filters_list.append(Q(site__isnull=True) | Q(site=OuterRef(kwargs['uf'] + '__site')))
            axis1_filters_list.append(Q(etablissement__isnull=True) | Q(etablissement=OuterRef(kwargs['uf'] + '__etablissement')))

        # return True
        return Exists(UserUfRole.records.filter(*axis1_filters_list, user=user, role_code__in=roles_list))

    builtins = {
        'is_superuser': {'django': is_superuser},
        'is_staff': {'django': is_staff},
        'q': {'django': Q},
        'in_scope': {'django': in_scope},
    }

    def __init__(self, field_names: set, const_roles: set = None, **kwargs):
        # TODO : Check parameters validity
        self.field_names = field_names
        self.const_roles = const_roles or list()
        self.table_roles_map = {}
        self.row_roles_map = {}
        self.parameters = set()

        for kwarg, kwval in kwargs.items():
            if isinstance(kwval, str):
                role_expression = PolyExpr(kwval, builtins=self.builtins)
                # print(f" e:{ast.unparse(role_expression.tree)}")
                expr_names = set(role_expression.names())
                # print(f"  1-{expr_names=}")
                expr_names -= set(self.builtins.keys())
                # print(f"  2-{expr_names=}")
                expr_names -= set(self.field_names)
                # print(f"  3-{expr_names=}")
                self.parameters |= expr_names
                self.row_roles_map[kwarg] = role_expression

    def table_roles_list(self, query_parameters: dict):
        return self.const_roles + list(code for code, expr in self.table_roles_map.items() if expr(query_parameters))

    def row_roles_expression(self, query_parameters: dict):
        """
        Returns a Django expression (to be used as a annotation value) that compute for every row a list of the user roles,
        as a string with a comma separated list of roles and starting and ending with a comma ','.
        eg : ',ADM,MAN,OWN,EDT,'
        To determine if the current user has a role (eg. Manager, code 'MAN'),
        one can test if the comma bracketed role code string (',MAN,') is
        a substring of this roles string
        """
        # Get all the needed parameters from query_parameters (setting at None if not found)
        parameters = {param: query_parameters.get(param) for param in self.parameters}

        # print(f"   {query_parameters=} {self.field_names=}")
        return Concat(
            *(
                [Value(',')]
                + [
                    Case(
                        When(
                            django_orm_expression(expr, values=parameters, fieldnames=self.field_names),
                            then=Value(code + ','),
                        ),
                        default=Value(''),
                    )
                    for code, expr in self.row_roles_map.items()
                ]
            )
        )
        # return Value(',' + ','.join(self.table_roles_list(query_parameters)) + ',')


class OField:
    def __init__(self, *args, value=None, special=None):
        self.value = value
        self.special = special


class OverolyAllRecordsManager(Manager):
    pass


class OverolyRecordsManager(Manager):
    """
    Overoly *default* manager. Only returns 'active' records (ie without atime or after it *and* without dtime or before it)
    """

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
                # Dynamic (ie parametric) annotations.
                # Computed from constants, fields values and parameters provided at request time
                # The callable should get a unique argument (the parameters dictionnary) and return a annotations dict (see above)
                self.annotations = kwargs['annotations']

            del kwargs['annotations']
        else:
            self.annotations = lambda query_parameters: {}
        self.query_parameters = {}
        super().__init__(*args, **kwargs)

    def setup(self, **query_parameters):
        """
        The setup method is used to set the queryset/annotations parameters
        (*user*, to allow *permissions* system to work , for instance).
        This is a chaining method (it returns *self*) so it can be used in the first part of the queryset building chain
        """
        self.query_parameters = query_parameters
        return self

    def get_queryset(self):
        # if self.annotations:
        #     annotations = self.annotations(self.query_parameters)
        #     print(f"    {annotations=}")
        qs = super().get_queryset().annotate(**(self.annotations(self.query_parameters)))
        self.query_parameters = {}
        return qs


class OverolyOptions:
    pass


class OverolyModelMetaclass(ModelBase):
    """

    Roles:
      - Only OMeta.roles_mapper ==> Create roles ofield with default name then use it for roles management
      - OMeta.roles_mapper *and* a special roles field set (but not defined)
            ==> Create roles ofield with provided name then use it for roles management
      - No OMeta.roles_mapper *but* roles_fieldname set and defined (either Django Field or OField with value set)
            ==> Use this field for roles management
      - No OMeta.roles_mapper neither roles field/ofield ==> No roles/rights management
      - Every other case ==> Raise a warning and do not use roles/rights management
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        # If this model is a abstract one, let it as it is
        if 'Meta' in attrs and getattr(attrs['Meta'], 'abstract', False):
            return super().__new__(cls, name, bases, attrs, **kwargs)

        # print(f"Overoly: Creating class {name}")
        attrs['_ometa'] = OverolyOptions()

        if 'OMeta' not in attrs:
            attrs['OMeta'] = type('OMeta', tuple(), {})

        attrs['_ometa'].special_id = None
        attrs['_ometa'].special_state = None
        attrs['_ometa'].special_roles = None
        attrs['_ometa'].config = None
        attrs['_ometa'].attributes = None
        attrs['_ometa'].django_field_names = set()
        attrs['_ometa'].annotation_names = set()

        roles_mapper = None
        # 1 - Configure the model using OMeta attributes
        for overoly_attrs in list(attrs['OMeta'].__dict__.keys()):
            if not overoly_attrs.startswith('_'):
                # print(f"  {overoly_attrs=}")
                if overoly_attrs == 'config':
                    print("    " + repr(attrs['OMeta'].config))
                    attrs['_ometa'].config = attrs['OMeta'].config
                    # del attrs['OMeta'].config
                elif overoly_attrs == 'attributes':
                    attrs['_ometa'].attributes = attrs['OMeta'].attributes
                    # del attrs['OMeta'].attributes
                elif overoly_attrs == 'roles_mapper':
                    roles_mapper = attrs['OMeta'].roles_mapper
                elif overoly_attrs in {
                    'ctime_field',
                    'mtime_field',
                    'atime_field',
                    'dtime_field',
                }:
                    pass
                else:
                    warning(f"Unknown OMeta attribute : {overoly_attrs}")

        # After having scanned all attributes, add a roles field
        # if hasattr(attrs['OMeta'], 'roles_mapper') and attrs['OMeta'].roles_mapper is not None:
        #     roles_mapper = attrs['OMeta'].roles_mapper
        #     print("    " + repr(attrs['OMeta'].roles_mapper))
        #     if isinstance(roles_mapper, dict):
        #         attrs['OMeta']._roles_mapper = attrs['OMeta'].roles_mapper
        #         del attrs['OMeta'].roles_mapper
        #     else:
        #         warning("Bad role_mapper type, should be a dict ...more precise message needed...")

        # Scan all attributes to get explicit Overoly primary key (this is not a recommanded practice, default is often better)
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, OField) and attr_value.special == 'id':
                attrs['_ometa'].special_id = attr_name

        # Scan all attributes to get primary key (mimics Django behaviour since the class is not yet created)
        if attrs['_ometa'].special_id is None:
            for attr_name, attr_value in attrs.items():
                if isinstance(attr_value, Field) and attr_value.primary_key:
                    attrs['_ometa'].special_id = attr_name

        # Use default Django created 'id' if needed
        if attrs['_ometa'].special_id is None:
            # No explicit 'special':'id' or explicit primary key found: assume Django will create one
            attrs['_ometa'].special_id = 'id'
            attrs['_ometa'].django_field_names.add('id')

        # Scan all attributes to get explicit Overoly roles field
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, OField) and attr_value.special == 'roles':
                attrs['_ometa'].special_roles = attr_name

        # Create roles field if needed
        if attrs['_ometa'].special_roles is None and roles_mapper is not None:
            if 'o_roles' not in attrs:
                # No explicit 'special':'roles' or explicit primary key found: assume Django will create one
                attrs['_ometa'].special_roles = 'o_roles'
                attrs[attrs['_ometa'].special_roles] = OField(special='roles')
            else:
                warning("Unable to create a roles field ('roles' field already exists and is not a special roles field) !")

        # Scan all attributes and compute annotations expressions if needed
        annotations = {}
        for attr_name, attr_value in attrs.items():

            def parametrize(formulae, params):
                return formulae

            if isinstance(attr_value, Field):
                attrs['_ometa'].django_field_names.add(attr_name)
            if isinstance(attr_value, OField):
                # All the field names of the model (both stored and computed ones)
                field_names = attrs['_ometa'].django_field_names | attrs['_ometa'].annotation_names
                # These are the field names that are available in value expression

                attrs['_ometa'].annotation_names.add(attr_name)
                formulae = attr_value.value
                if attr_value.special == 'id':
                    pass
                elif attr_value.special == 'state':
                    pass
                elif attr_value.special == 'roles':
                    if attr_value.value is None and roles_mapper is not None:
                        formulae = ORolesMapper(field_names, **roles_mapper).row_roles_expression
                # print(f"  overoly_field: {attr} => {val}")

                if isinstance(formulae, Expression):
                    annotations[attr_name] = partial(parametrize, formulae)
                elif callable(formulae):
                    annotations[attr_name] = formulae
                elif isinstance(formulae, str):
                    pass
                else:
                    pass

        def annotations_function_factory(things):
            """
            Factory function that, returns a function that takes query parameters then use them to compute annotation expression
            """

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
        print("Overoly: Checking *create/write* rights (TODO)...")
        super().save(*args, **kwargs)
