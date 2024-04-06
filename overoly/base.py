"""
Overoly features
================

Add to every model:
- 'live' computed fields (aka parametric annotations), using string expressions and dependencies management
- flexible attributes for every field (customizable via configuration dict/file = toml)
- fine state-based & role-based permissions management :
    - at model level for record creation (without state management :-)
    - row level for record view and delete
      - A weak field level view permission management is however possible : A field on a row is
        visible only if the user has any role that allow row access OR any role that allow field access.
        This limitation comes from ORM & SQL queries implementation (SQL only returns 'rectangular' results).
        True 'per row and per field' read permission can be implemented on a higher level (but is less safe).
    - field level (+ computed values constraints) for record update

Allows very customizable workflow management

Future (or optional ?):
- integrated ctime/atime/mtime/dtime management

Almost all features are implemented via metaclasses, thus computed at launch, without runnning overload

Implementation roadmap :

  v read permissions (row level)
  o- read permissions (field level)
  o delete permissions
  o modification permissions (fields write access)
  o- modification permissions (fields values constraints)
  o creation permissions
  o field attributes management
  o configuration management
  o generic role scope
  o string and/or litteral based role rule
  o atime/dtime management
  o- ctime/mtime management

"""

from copy import deepcopy
from functools import partial
from logging import warning
from math import ceil, log10

from django.db.models import Model, Expression, Value, When, Case, Field, Q, Exists, OuterRef, F
from django.db.models.functions import Cast, Substr
from django.db.models.base import ModelBase
from django.db.models import IntegerField
from django.utils.timezone import now

# from overoly.queryset import OQuerySet

from polyexpr.polyexpr import PolyExpr, django_orm_expression

try:
    from django_pandas.managers import DataFrameManager as Manager
except ImportError:
    from django.db.models import Manager


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
        # print(f"is_superuser(u): u=")
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
                Q(centre_responsabilite__isnull=True)
                | Q(centre_responsabilite=OuterRef(kwargs['uf'] + '__centre_responsabilite'))
            )
            axis1_filters_list.append(Q(pole__isnull=True) | Q(pole=OuterRef(kwargs['uf'] + '__pole')))
            axis1_filters_list.append(Q(site__isnull=True) | Q(site=OuterRef(kwargs['uf'] + '__site')))
            axis1_filters_list.append(Q(etablissement__isnull=True) | Q(etablissement=OuterRef(kwargs['uf'] + '__etablissement')))

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
        # self.const_roles = const_roles or list()
        # self.table_roles_map = {}
        self.row_roles_map = {}
        self.parameters = set()

        for kwarg, kwval in kwargs.items():
            if isinstance(kwval, str):
                role_expression = PolyExpr(kwval, names=self.builtins)
                # print(f" e:{ast.unparse(role_expression.tree)}")
                expr_names = set(role_expression.used_names())
                # print(f"  1-{expr_names=}")
                expr_names -= set(self.builtins.keys())
                # print(f"  2-{expr_names=}")
                expr_names -= set(self.field_names)
                # print(f"  3-{expr_names=}")
                self.parameters |= expr_names
                self.row_roles_map[kwarg] = role_expression

    def table_roles_list(self, query_parameters: dict):
        return self.const_roles + list(code for code, expr in self.table_roles_map.items() if expr(query_parameters))

    def row_roles_int_expression(self, query_parameters: dict):
        """
        Returns a Django ORM expression (to be used as a annotation value) that compute for every row a map of the user roles,
        as a integer which is a sum of powers of 2 (one for each effective role defined)
        eg : if effective defined roles for this manager are ['ADM','MAN','OWN','VAL'], the expression evaluated for a record will
        be 7 if the user has role ADM (2**0), MAN (2**1) and OWN (2**2) but not VAL (2**3).
        To check if the current user has a given role (eg. Manager, code 'MAN', rank 1),
        one can check if ((2**rank) & (this value)) is different from 0.
        """
        # print("{}", list((code, expr) for (code, expr) in enumerate(self.row_roles_map.keys())))

        # Get all the needed parameters from query_parameters (setting at None if not found)
        parameters = {param: query_parameters.get(param) for param in self.parameters}

        # print(f"   {query_parameters=} {self.field_names=}")
        django_expression = sum(
            [
                Case(
                    When(
                        django_orm_expression(expr, values=parameters, fieldnames=self.field_names),
                        then=Value(2**code),
                    ),
                    default=Value(0),
                )
                for code, expr in enumerate(self.row_roles_map.values())
            ]
        )

        # for code, expr in self.row_roles_map.items():
        #     print(f"  {code=} : {expr=}")
        # print(f"{self.parameters=} {query_parameters=} {parameters=}:  {django_expression=}")
        return django_expression


class OField:
    def __init__(self, *args, value=None, special=None):
        self.value = value
        self.special = special


class OFieldState(OField):
    pass


class OFieldRoles(OField):
    pass


class OverolyAllRecordsManager(Manager):
    def __init__(self, *args, **kwargs):
        self.read = tuple()
        if 'read' in kwargs:
            if isinstance(self.read, tuple):
                self.read = kwargs['read']
            else:
                pass  # Should issue a warning here
            del kwargs['read']
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
        All parameter names are converted to upper char so this is a case insensible method
        """
        self.query_parameters = {k.upper(): v for k, v in query_parameters.items()}
        return self

    def get_queryset(self):
        self.query_parameters['NOW'] = now()
        annotations = self.annotations(self.query_parameters)
        qs = super().get_queryset().annotate(**annotations)

        self.query_parameters = {}
        # return OQuerySet(qs)
        return qs


class OverolyRecordsManager(OverolyAllRecordsManager):
    """
    Overoly *default* manager. Only returns 'active' records (ie without atime or after it *and* without dtime or before it)
    and which are accessible (readable) to the provided user via the settings.
    **If no 'read' permissions is given then everyone can see all records !**
    """

    def get_queryset(self):
        # if self.annotations:
        #     annotations = self.annotations(self.query_parameters)
        #     print(f"    {annotations=}")
        # read_condition_args = []
        # if self.read:
        #     read_condition = None
        #     for role_str in self.read:
        #         if read_condition is None:
        #             read_condition = Q(o_roles__contains=role_str)
        #         else:
        #             read_condition |= Q(o_roles__contains=role_str)
        #     read_condition_args = [read_condition]
        #     # print(f"{read_condition_args}")
        # annotations = self.annotations(self.query_parameters)
        qs = super().get_queryset()
        if '_o_can_read' in qs.query.annotations:
            read_condition_args = [Q(_o_can_read__gt=0)]
        else:
            read_condition_args = []

        qs = qs.filter(*read_condition_args)

        # erase query parameters so a subsequent call will not use them
        self.query_parameters = {}
        # return OQuerySet(qs)
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
        attrs['_ometa'].permissions = None
        attrs['_ometa'].config = None
        attrs['_ometa'].attributes = None
        attrs['_ometa'].django_field_names = set()
        attrs['_ometa'].annotation_names = set()

        roles_mapper = None
        # 1 - Configure the model using OMeta attributes
        for overoly_attrs in list(attrs['OMeta'].__dict__.keys()):
            if not overoly_attrs.startswith('_'):
                # print(f"  {overoly_attrs=}")
                if overoly_attrs == 'permissions':
                    attrs['_ometa'].permissions = attrs['OMeta'].permissions
                    # del attrs['OMeta'].attributes
                elif overoly_attrs == 'config':
                    # print("    " + repr(attrs['OMeta'].config))
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
            if '_o_roles' not in attrs:
                # No explicit 'special':'roles' or explicit primary key found: assume Django will create one
                attrs['_ometa'].special_roles = '_o_roles'
                attrs[attrs['_ometa'].special_roles] = OField(special='roles')
            else:
                warning(
                    "Unable to create a roles field ('_o_roles' field already exists "
                    "and is not a special roles field) in class {name}!".format(name=name)
                )

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
                        formulae = ORolesMapper(field_names, **roles_mapper).row_roles_int_expression
                # print(f"  overoly_field: {attr} => {val}")

                if isinstance(formulae, Expression):
                    annotations[attr_name] = partial(parametrize, formulae)
                elif callable(formulae):
                    annotations[attr_name] = formulae
                elif isinstance(formulae, str):
                    # The value of the field (annotation) is a string that need to be interpreted as a expression
                    print("#### OField str expression:", repr(formulae))
                    try:
                        polyexpr = PolyExpr(formulae)
                        print("#### Expression:", repr(polyexpr))
                        print("#### Expression:", repr(polyexpr.used_names()), field_names)
                        # expression names must be either field names or valid function names
                        # Tomporary stub
                        annotations[attr_name] = lambda params: Value('Unimplemented')
                    except SyntaxError:
                        warning("Syntax Error")
                else:
                    pass

        if '_o_roles' in annotations and '_o_state' in annotations and roles_mapper is not None:
            # We could use a 'alias' instead of a 'annotation' for these computed fields.
            attrs['_o_can_read'] = OField(value=F('_o_can_read'))
            attrs['_ometa'].annotation_names.add('_o_can_read')
            attrs['_o_can_modify'] = OField(value=F('_o_can_modify'))
            attrs['_ometa'].annotation_names.add('_o_can_modify')
            attrs['_o_can_delete'] = OField(value=F('_o_can_delete'))
            attrs['_ometa'].annotation_names.add('_o_can_delete')
            n_states = 18
            n_roles = len(roles_mapper)
            substr_lenght = ceil(log10(2**n_roles))
            read_str = ''
            modify_str = ''
            delete_str = ''
            everyone_mask = 2**n_roles - 1
            for s in range(n_states):
                # compute mask from state number and permissions dict
                # TODO
                # temporary implementation = every role !
                read_str += str(everyone_mask).zfill(substr_lenght)
                modify_str += str(everyone_mask).zfill(substr_lenght)
                delete_str += str(everyone_mask).zfill(substr_lenght)
            # fictional example where state in [0,1] and Nr < 5
            # read allowed for role 2 (2**2=4) in state 0
            annotations['_o_can_read'] = lambda p: Cast(
                Substr(Value(read_str), 1 + F('_o_state') * substr_lenght, substr_lenght), output_field=IntegerField()
            ).bitand(F('_o_roles'))
            annotations['_o_can_modify'] = lambda p: Cast(
                Substr(Value(modify_str), 1 + F('_o_state') * substr_lenght, substr_lenght), output_field=IntegerField()
            ).bitand(F('_o_roles'))
            annotations['_o_can_delete'] = lambda p: Cast(
                Substr(Value(delete_str), 1 + F('_o_state') * substr_lenght, substr_lenght), output_field=IntegerField()
            ).bitand(F('_o_roles'))

            # print("annotations:", annotations)

        def annotations_function_factory(things):
            """
            Factory function that, returns a function that takes query parameters then use them to compute annotation expression
            """

            def f(things, query_parameters):
                return {name: val_func(query_parameters) for name, val_func in things.items()}

            return partial(f, things)

        if 'records' not in attrs:
            # Add the default Manager (see Django documentation)
            # read_permissions = tuple()
            # if attrs['_ometa'].permissions:
            #     if isinstance(attrs['_ometa'].permissions, dict):
            #         if attrs['_ometa'].permissions.get('read'):
            #             # Works with 'read' permission as a tuple, a list or a dict
            #             read_permissions = tuple(',' + role + ',' for role in attrs['_ometa'].permissions.get('read'))
            #             # print(f"{attrs['_ometa'].permissions.get('read')=} ==> {read_permissions=}")
            # attrs['records'] = OverolyRecordsManager(annotations=annotations_function_factory(annotations), read=read_permissions)
            attrs['records'] = OverolyRecordsManager(annotations=annotations_function_factory(annotations))
        else:
            raise RuntimeError("Overoly Model cannot define a 'records' attribute (reserved for default manager)")
        if 'all_records' not in attrs:
            attrs['all_records'] = OverolyAllRecordsManager(annotations=annotations_function_factory(annotations))
        else:
            raise RuntimeError("Overoly Model cannot define a 'all_records' attribute (reserved for base manager)")

        cl = super().__new__(cls, name, bases, attrs, **kwargs)
        return cl


class OverolyModel(Model, metaclass=OverolyModelMetaclass):
    """ """

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
        print(f"Overoly: Checking *create/write* rights: {self=} {args=} {kwargs=} (TODO)...")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print(f"Overoly: Checking *delete* rights: {self=} {args=} {kwargs=} (TODO)...")
        super().delete(*args, **kwargs)
