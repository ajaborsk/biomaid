#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2023 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
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
"""
Ensemble d'utilitaires (constantes, classes et fonctions)
destiné à être utilisé avec la base de données (plus précisément l'ORM) de Django
"""
import json
import sys
import logging
from types import FunctionType

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import (
    Expression,
    Exists,
    Subquery,
    Q,
    OuterRef,
    Aggregate,
    Case,
    When,
    F,
    Value,
    ExpressionWrapper,
    CharField,
    Model,
)
from django.db.models.functions import Concat, Left, Length, Cast
from django.db.utils import ProgrammingError
from django.utils.translation import gettext as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.aggregates import StringAgg as PsqlStringAgg

from common import config
from common.models import (
    Programme,
    Uf,
    UserUfRole,
    Etablissement,
    Site,
    Pole,
    Service,
    CentreResponsabilite,
    User,
    GenericRole,
)
from dem.models import Campagne, Demande

logger = logging.getLogger(__name__)


def debug(*args, **kwargs):
    logger.debug(" ".join(map(str, args)))


def server_ready():
    for app_cfg in apps.get_app_configs():
        if hasattr(app_cfg, 'server_ready') and callable(app_cfg.server_ready):
            app_cfg.server_ready()


STRUCTURE_LEVELS = {
    "etablissement": Etablissement,
    "site": Site,
    "pole": Pole,
    "centre_responsabilite": CentreResponsabilite,
    "service": Service,
}


class SqliteStringAgg(Aggregate):
    """
    Cette classe définit la fonction d'aggrégation 'StringAgg' = concaténation de chaînes de caractères pour SQLite3
    Elle est assez imparfaite et en particulier ne permet pas d'utiliser à la fois
    un séparateur autre que celui par défaut et qui est la virgule ','
    et le mot clef 'distinct'

    Pour PostGreSQL, l'équivalent est django.contrib.postgres.aggregates.StringAgg
    """

    function = "GROUP_CONCAT"
    template = "%(function)s(%(distinct)s%(expressions)s)"
    allow_distinct = True

    def __init__(self, expression, delimiter=",", **extra):
        if delimiter == ",":
            super().__init__(expression, **extra)
        else:
            delimiter_expr = Value(str(delimiter))
            super().__init__(expression, delimiter_expr, **extra)

    def convert_value(self, value, expression, connection):
        if not value:
            return ""
        return value


if "postgres" in config.settings.DATABASES["default"]["ENGINE"]:
    StringAgg = PsqlStringAgg
elif "sqlite3" in config.settings.DATABASES["default"]["ENGINE"]:
    StringAgg = SqliteStringAgg
else:
    raise RuntimeError(_("PostgreSQL and SQLite3 are the only supported database engines"))


def user_lookup(*args, **kwargs):
    """Fonction qui retourne une liste avec tous les utilisateurs, sous forme de fonction Django"""
    return (
        get_user_model()
        .objects.all()
        .order_by('last_name')
        .values_list(
            'pk',
            Concat(
                F('first_name'),
                Value(' '),
                F('last_name'),
                Value(" ("),
                F('username'),
                Value(")"),
            ),
        )
    )


def user_choices(*args, **kwargs):
    """Méthode qui retourne une liste de choix avec tous les utilisateurs ACTIFS, sous forme de fonction Django"""
    return (
        get_user_model()
        .objects.filter(is_active=True)
        .order_by('last_name')
        .values_list(
            'pk',
            Concat(
                F('first_name'),
                Value(' '),
                F('last_name'),
                Value(" ("),
                F('username'),
                Value(")"),
            ),
        )
    )


def uf_choices(*args, only_active=False, **kwargs):
    """Méthode qui retourne une liste de choix avec toutes les UF (actives), sous forme de fonction Django"""
    if only_active:
        return get_user_model().active_objects.order_by('code').values_list('pk', Concat(F('code'), Value(' '), F('nom')))
    else:
        return get_user_model().objects.all().order_by('code').values_list('pk', Concat(F('code'), Value(' '), F('nom')))


def filter_choices_from_column_values(klass, fieldname, label_expr=None, order_by=None):
    """
    Cette fonction renvoie une fonction qui renvoie liste de dictionnaires, prête à être utilisée comme paramètre 'choices'
    dans un filtre utilisateur de SmartView.
    La classe à fournir est celle de la SmartView
    le fieldname (qui peut comporter des 'lookups') est généralement celui qui sert à la définition 'data' de la colonne à filtrer
    """

    if label_expr is None:
        label_expr = F(fieldname)

    if order_by is None:
        order_by = fieldname

    def choices(request, *args, **kwargs):
        return [{'value': '{}', 'label': 'Tous'}] + [
            {'value': json.dumps({fieldname: item[0]}), 'label': '{}'.format(item[1])}
            for item in klass.objects.all()
            .order_by()
            .distinct()
            .order_by(order_by)
            .annotate(_filter_label=label_expr)
            .values_list(fieldname, '_filter_label')
        ]

    return choices


#
# Unused function for now. Role sources can be :
# - Constant (always included)
# - Conditional : Includes a given role code if a condition is filled (this does not depend of the row/record):
#     - 'superuser' : The current user is a Django superuser
#     - 'staff' : The current user is a site staff member (see Django user managment)
# - Explicit : Includes all role codes given via ContentType GenericRole model
#
def get_roles_expression_function(model_class: Model, roles_sources: list) -> FunctionType:
    """Create and return a function that can be used with Django ORM to compute for each row of a Model/SmartView a list of
    effective role code.

    This function is meant to be called at Django launch. It returns a instance_role_expression function, designed to be called
    at View instanciation (with view_params as only parameter). This late function then return a Django ORM expression, which can
    be used in a QuerySet annotation ('annotate' method) to get, for each row of the queryset, a field that give a list of
    effective role codes, as a string like ",OWN,ADM,". PLease note the "," (comma) at the start and the end of the string. This
    is meant to detect safely a role code by testing if ",CODE," is included in this string.

    :param model_class: The model class that will
    :type model_class: Model
    :param roles_sources: _description_
    :type roles_sources: list
    """

    # This trick allow to launch migrations from a empty database and reset_db command
    # main_content_type = None
    # if set(sys.argv).isdisjoint({'reset_db', 'migrate', 'makemigrations'}):
    #     try:
    #         main_content_type = ContentType.objects.get_for_model(model_class)
    #         pass
    #     except ProgrammingError:
    #         pass

    def instance_roles_expression(view_attrs: dict) -> Expression:
        args = []

        args.append(Value(','))

        if len(args) > 1:
            return ExpressionWrapper(Concat(*args), CharField())
        else:
            return ExpressionWrapper(args[0], CharField())

    return instance_roles_expression


def class_roles_expression(
    model_class: Model,
    owner_field: str = None,
    uf_field: str = None,
    domaine_field: str = None,
    programme_field: str = None,
    campagne_field: str = None,
    expert_field: str = None,
    discipline_field: str = None,
):
    """
    Fonction destinée à être utilisée lors de la définition de SmartViews pour la colonne des rôles
    Il faut donner comme valeur à l'attribut 'data' du champ spécial 'roles' (peu importe son nom), la valeur de retour
    de cette fonction, avec les paramètres qui vont bien en fonction de la nature de la SmartView.

    Elle retourne une fonction (qui sera appelée à l'instanciation de la SmartView) qui elle-même retourne une expression
    QuerySet/Django qui sera intégrée dans la requête pour retourner dans chaque enregistrement de la SmartView la liste
    (sous le format attendu par SmartView : chaîne de caractères avec la liste des codes de rôle, séparés par une virgule) des rôles
    qu'a l'utilisateur sur cet enregistrement.

    ATTENTION: Le champ discipline est utilisé pour déterminer le responsable technique, pas l'expert.
    Pour la discipline de l'expert, cela passe par le champ 'domaine_field', qui a un champ 'discipline' de lui-même...
    """
    # This trick allow to launch migrations from a empty database and reset_db command
    main_content_type = None
    if set(sys.argv).isdisjoint({'reset_db', 'migrate', 'makemigrations'}):
        try:
            main_content_type = ContentType.objects.get_for_model(model_class)
            programme_content_type = ContentType.objects.get_for_model(Programme)
            campagne_content_type = ContentType.objects.get_for_model(Campagne)
        except ProgrammingError:
            pass

    # noinspection PyListCreation
    def instance_roles_expression(view_attrs):
        args = []

        # L'utilisateur est-il administrateur ?
        args.append(Value(',ADM,') if view_attrs['user'].is_staff else Value(','))

        # L'utilisateur est-il expert potentiel ?
        # TODO: Grosse bidouille à corriger avec une vraie gestion des rôles potentiels
        #       En particulier ici, tenir compte de l'axe 'structure' (UF, pôle, etc.) voire de la discipline...
        # args.append(Value('P-EXP,')if UserUfRole.objects.filter(user=view_attrs['user'], role_code='EXP').exists() else Value(''))
        args += [Value('P-' + role_code + ',') for role_code in view_attrs['user_roles'] if role_code != 'ADM']

        # L'enregistrement possède-t-il la notion de 'propriétaire' (fournir le paramètre 'owner_field') ?
        if owner_field is not None:
            args.append(
                Case(
                    When(**{owner_field: view_attrs['user']}, then=Value('OWN,')),
                    default=Value(''),
                )
            )

        # L'enregistrement possède-t-il la notion de 'programme' (pour arbitrage) ?
        if programme_field is not None:
            args.append(
                Case(
                    When(
                        **{programme_field + '__arbitre': view_attrs['user']},
                        then=Value('ARB,'),
                    ),
                    When(
                        Exists(
                            Subquery(
                                GenericRole.active_objects.filter(
                                    content_type=programme_content_type,
                                    object_id=Cast(OuterRef(programme_field), output_field=CharField()),
                                    role_code='ARB',
                                    user_id=view_attrs['user'].id,
                                )
                            )
                        ),
                        then=Value('ARB,'),
                    ),
                    default=Value(''),
                )
            )

        # l'enregitrement possède-t-il la notion de 'campagne/calendrier' (pour dispatcher) ?
        if campagne_field is not None:
            args.append(
                Case(
                    When(
                        **{campagne_field + '__dispatcher': view_attrs['user']},
                        then=Value('DIS,'),
                    ),
                    When(
                        Exists(
                            Subquery(
                                GenericRole.active_objects.filter(
                                    content_type=campagne_content_type,
                                    object_id=Cast(OuterRef(campagne_field), output_field=CharField()),
                                    role_code='DIS',
                                    user_id=view_attrs['user'].id,
                                )
                            )
                        ),
                        then=Value('DIS,'),
                    ),
                    default=Value(''),
                )
            )

        # l'enregitrement possède-t-il la notion de 'discipline' (pour le **responsable technique**) ?
        # Les rôles généralement utilisés ici sont des rôles liés aux responsabilité (et non à l'expertise) : DIR, CAD, RESPD...
        if discipline_field is not None:
            if uf_field is not None:
                args.append(
                    Subquery(
                        UserUfRole.active_objects.filter(
                            (
                                (
                                    Q(uf__isnull=True)
                                    & Q(service__isnull=True)
                                    & Q(centre_responsabilite__isnull=True)
                                    & Q(pole__isnull=True)
                                    & Q(site__isnull=True)
                                    & Q(etablissement__isnull=True)
                                )
                                | Q(uf=OuterRef(uf_field))
                                | Q(service=OuterRef(uf_field + '__service'))
                                | Q(centre_responsabilite=OuterRef(uf_field + '__centre_responsabilite'))
                                | Q(pole=OuterRef(uf_field + '__pole'))
                                | Q(site=OuterRef(uf_field + '__site'))
                                | Q(etablissement=OuterRef(uf_field + '__etablissement'))
                            )
                            & (Q(discipline__isnull=True) | Q(discipline=OuterRef(discipline_field))),
                            user_id=view_attrs['user'].id,
                        )
                        .values('user')
                        .annotate(
                            m_roles=StringAgg(
                                "role_code",
                                ",",
                                distinct=True,
                                output_field=CharField(),
                            )
                        )
                        .values("m_roles")
                    )
                )
            else:
                args.append(
                    Subquery(
                        UserUfRole.active_objects.filter(
                            (Q(discipline__isnull=True) | Q(discipline=OuterRef(discipline_field))),
                            user_id=view_attrs['user'].id,
                        )
                        .values('user')
                        .annotate(
                            m_roles=StringAgg(
                                "role_code",
                                ",",
                                distinct=True,
                                output_field=CharField(),
                            )
                        )
                        .values("m_roles")
                    )
                )

        # l'enregitrement possède-t-il la notion d'expert ?
        # Ce rôle s'ajoute à celui d'expert dans le domaine et/ou la discipline. On est expert si
        #   - on est *désigné explicitement* expert de l'enregistrement (il faut alors fournir le paramètre 'expert_field')
        #   - *OU* si on est expert dans la discipline et le domaine (il faut fournir le paramètre 'domaine_field')
        if expert_field is not None:
            args.append(
                Case(
                    When(**{expert_field: view_attrs['user']}, then=Value('EXP,')),
                    default=Value(''),
                )
            )

        if uf_field is not None:
            if domaine_field is not None:
                args.append(
                    Subquery(
                        UserUfRole.active_objects.filter(
                            (
                                (
                                    Q(uf__isnull=True)
                                    & Q(service__isnull=True)
                                    & Q(centre_responsabilite__isnull=True)
                                    & Q(pole__isnull=True)
                                    & Q(site__isnull=True)
                                    & Q(etablissement__isnull=True)
                                )
                                | Q(uf=OuterRef(uf_field))
                                | Q(service=OuterRef(uf_field + '__service'))
                                | Q(centre_responsabilite=OuterRef(uf_field + '__centre_responsabilite'))
                                | Q(pole=OuterRef(uf_field + '__pole'))
                                | Q(site=OuterRef(uf_field + '__site'))
                                | Q(etablissement=OuterRef(uf_field + '__etablissement'))
                            )
                            & (
                                (Q(discipline__isnull=True) & Q(domaine_prefix__isnull=True))
                                | (Q(discipline=OuterRef(domaine_field + '__discipline')) & Q(domaine_prefix__isnull=True))
                                # Cette ligne ci-dessous peut certainement être améliorée
                                # car elle n'utilise pas LIKE en SQL à cause de l'ordre des arguments
                                # de la fonction Q() : la OuterRef() est forcément à droite...
                                # Il faudrait reproduire l'équivalent de
                                # OuterRef(domaine_field + '__code') LIKE domaine_prefix | '%' ...
                                | (
                                    Q(discipline=OuterRef(domaine_field + '__discipline'))
                                    & Q(
                                        domaine_prefix=Left(
                                            OuterRef(domaine_field + '__code'),
                                            Length('domaine_prefix'),
                                        )
                                    )
                                )
                            ),
                            user_id=view_attrs['user'].id,
                        )
                        .values('user')
                        .annotate(
                            m_roles=StringAgg(
                                'role_code',
                                ",",
                                distinct=True,
                                output_field=CharField(),
                            )
                        )
                        .values('m_roles')
                    )
                )
            else:
                args.append(
                    Subquery(
                        UserUfRole.active_objects.filter(
                            (
                                Q(uf__isnull=True)
                                & Q(service__isnull=True)
                                & Q(centre_responsabilite__isnull=True)
                                & Q(pole__isnull=True)
                                & Q(site__isnull=True)
                                & Q(etablissement__isnull=True)
                            )
                            | Q(uf=OuterRef(uf_field))
                            | Q(service=OuterRef(uf_field + '__service'))
                            | Q(centre_responsabilite=OuterRef(uf_field + '__centre_responsabilite'))
                            | Q(pole=OuterRef(uf_field + '__pole'))
                            | Q(site=OuterRef(uf_field + '__site'))
                            | Q(etablissement=OuterRef(uf_field + '__etablissement')),
                            user_id=view_attrs['user'].id,
                        )
                        .values('user')
                        .annotate(
                            m_roles=StringAgg(
                                'role_code',
                                ",",
                                distinct=True,
                                output_field=CharField(),
                            )
                        )
                        .values('m_roles')
                    )
                )
        else:
            if domaine_field is not None:
                args.append(
                    Subquery(
                        UserUfRole.active_objects.filter(
                            (
                                (Q(discipline__isnull=True) & Q(domaine_prefix__isnull=True))
                                | (Q(discipline=OuterRef(domaine_field + '__discipline')) & Q(domaine_prefix__isnull=True))
                                # Cette ligne ci-dessous peut certainement être améliorée
                                # car elle n'utilise pas LIKE en SQL à cause de l'ordre des arguments
                                # de la fonction Q() : la OuterRef() est forcément à droite...
                                # Il faudrait reproduire l'équivalent de
                                # OuterRef(domaine_field + '__code') LIKE domaine_prefix | '%' ...
                                | (
                                    Q(discipline=OuterRef(domaine_field + '__discipline'))
                                    & Q(
                                        domaine_prefix=Left(
                                            OuterRef(domaine_field + '__code'),
                                            Length('domaine_prefix'),
                                        )
                                    )
                                )
                            ),
                            user_id=view_attrs['user'].id,
                        )
                        .values('user')
                        .annotate(
                            m_roles=StringAgg(
                                'role_code',
                                ",",
                                distinct=True,
                                output_field=CharField(),
                            )
                        )
                        .values('m_roles')
                    )
                )

        args.append(Value(','))
        # The generic roles (can be attached to any object)
        args.append(
            Subquery(
                GenericRole.active_objects.filter(
                    content_type=main_content_type,
                    object_id=Cast(OuterRef('pk'), output_field=CharField()),
                    user_id=view_attrs['user'].id,
                )
                .values('user')
                .annotate(
                    m_roles=StringAgg(
                        'role_code',
                        ",",
                        distinct=True,
                        output_field=CharField(),
                    )
                )
                .values('m_roles')
            )
        )
        args.append(Value(','))

        if len(args) > 1:
            return ExpressionWrapper(Concat(*args), CharField())
        else:
            return ExpressionWrapper(args[0], CharField())

    return instance_roles_expression


def get_uf_list(structure, closed=False):
    """Renvoie la liste des UF (sous forme d'un QuerySet) d'une
    structure donnée

    si closed=True, retourne aussi les UF fermées
    """
    ufs = None
    if isinstance(structure, Uf):
        ufs = Uf.objects.filter(pk=structure.id)

    for level, klass in STRUCTURE_LEVELS.items():
        if isinstance(structure, klass):
            ufs = Uf.objects.filter(**{level: structure.id})

    if ufs is None:
        raise Exception("Structure invalide", structure)
    else:
        if closed:
            return ufs
        else:
            return ufs.filter(cloture__isnull=True)


def get_uf_role_user(uf, role_code):
    return UserUfRole.objects.filter(uf=uf, role_code=role_code)


def get_uf_roles(src, obj):
    """Returns the roles set of a object (single uf)."""

    if isinstance(src, get_user_model()):
        user = src.user
    elif isinstance(src, str):
        if get_user_model().objects.get(username=src).exists():
            user = get_user_model().objects.get(username=src)
        else:
            return set()  # If user has no ext user has no role !
    elif isinstance(src, get_user_model()):
        user = src
    elif isinstance(src, WSGIRequest):
        user = src.user
    else:
        raise RuntimeError("src should be a ext_user, username, a user or a request.")

    # debug("AJA obj:", obj, type(obj))

    if isinstance(obj, Uf):
        uf = obj
    elif isinstance(obj, str):
        uf = Uf.objects.get(code=obj)
    elif isinstance(obj, Demande):
        uf = obj.uf
    else:
        raise RuntimeError("obj should be a Uf, Uf code (as str) or a Demande.")

    roles_query = UserUfRole.objects.filter(user=user, uf=uf)

    role_codes = set(roles_query.values_list("role_code", flat=True))
    return role_codes


def get_roles(src, obj=None):
    """Returns the roles set of a object :
    list of (uf, {'role':rode_name})
    """

    if isinstance(src, User):
        user = src
    elif isinstance(src, str):
        user = get_user_model().objects.get(username=src)
    elif isinstance(src, get_user_model()):
        user = src
    elif isinstance(src, WSGIRequest):
        user = src.user
    else:
        raise RuntimeError("src should be a ext_user, username, a user or a request.")

    # debug("AJA obj:", obj, type(obj))

    if obj is None:
        # roles_query = UserUfRole.objects.filter(extension_user=ext_user)
        uf_filter = [Q(cloture__isnull=True)]
    else:
        if isinstance(obj, Uf):
            # uf = [obj]
            uf_filter = [Q(pk=obj)]
        elif isinstance(obj, str):
            # uf = Uf.objects.filter(code=obj)
            uf_filter = [Q(code=obj)]
        elif isinstance(obj, Demande):
            # uf = [obj.uf]
            uf_filter = [Q(pk=obj.uf), Q(cloture__isnull=True)]
        elif isinstance(obj, Etablissement):
            # uf = Uf.objects.filter(etablissement=obj)
            uf_filter = [Q(etablissement=obj), Q(cloture__isnull=True)]
        elif isinstance(obj, Site):
            # uf = Uf.objects.filter(site=obj)
            uf_filter = [Q(site=obj), Q(cloture__isnull=True)]
        elif isinstance(obj, Pole):
            # uf = Uf.objects.filter(pole=obj)
            uf_filter = [Q(pole=obj), Q(cloture__isnull=True)]
        elif isinstance(obj, Service):
            # uf = Uf.objects.filter(service=obj)
            uf_filter = [Q(service=obj), Q(cloture__isnull=True)]
        else:
            raise RuntimeError("obj should be None, a structure, a Uf, Uf code (str) or a Demande.")
        # roles_query = UserUfRole.objects.filter(extension_user=ext_user, uf__in=uf)

    new_qs = (
        Uf.objects.filter(cloture__isnull=True)
        .annotate(r=F('userufrole__role_code'), u=F('userufrole__user'))
        .filter(*uf_filter, u=user.pk)
        .values(mcode=F('pk'), r=F('r'))
        .union(
            Service.objects.annotate(r=F('userufrole__role_code'), u=F('userufrole__user'))
            .filter(u=user.pk)
            .values(mcode=F('uf__pk'), r=F('r'))
            .filter(mcode__in=Uf.objects.filter(*uf_filter))
        )
        .union(
            CentreResponsabilite.objects.annotate(r=F('userufrole__role_code'), u=F('userufrole__user'))
            .filter(u=user.pk)
            .values(mcode=F('uf__pk'), r=F('r'))
            .filter(mcode__in=Uf.objects.filter(*uf_filter))
        )
        .union(
            Pole.objects.annotate(r=F('userufrole__role_code'), u=F('userufrole__user'))
            .filter(u=user.pk)
            .values(mcode=F('uf__pk'), r=F('r'))
            .filter(mcode__in=Uf.objects.filter(*uf_filter))
        )
        .union(
            Site.objects.annotate(r=F('userufrole__role_code'), u=F('userufrole__user'))
            .filter(u=user.pk)
            .values(mcode=F('uf__pk'), r=F('r'))
            .filter(mcode__in=Uf.objects.filter(*uf_filter))
        )
        .union(
            Etablissement.objects.annotate(r=F('userufrole__role_code'), u=F('userufrole__user'))
            .filter(u=user.pk)
            .values(mcode=F('uf__pk'), r=F('r'))
            .filter(mcode__in=Uf.objects.filter(*uf_filter))
        )
        .order_by('mcode')
        .values_list('mcode', 'r')
    )

    # print("AJA> new_qs", new_qs)
    return [(Uf.objects.get(pk=role[0]), {'role': role[1]}) for role in new_qs]

    # return [(role.uf, {"role": role.role_code}) for role in roles_query]

    # role_codes = roles_query.values_list("role_code", flat=True).distinct()
    # roles = {role_code: {role.uf for role in roles_query.filter(role_code=role_code)} for role_code in role_codes}
    # return roles


def group_by_entities(uf_datalist, class_list=(Pole, Service)):
    """Cette fonction est destinée à regrouper 'intelligemment' des UF
    en fonction des structures (organisations, poles, service, CR...)

    En entrée :
       * _uf_datalist_ est une liste de couples (_uf_, _data_)
            !! _data_ doit être un dict à un seul niveau (pas de dict de dict !)
       * _class_list_ est la liste des classes d'entité à tester (dans cet ordre : Il faut les plus "grosses" en premier)

    En sortie :
       * retourne une liste de couples (_entité_, _data_) où _entité_ est une instance de Pole, Service, Uf, etc.

     si _data_ est identique pour toutes les UF d'un service ou d'un pôle, par exemple
     la fonction va retourner un seul couple pour toutes ces UF.
    """

    # On crée un dictionnaire 'inverse' pour avoir, pour chaque jeu de _data_ la liste des UF :

    inv_datalist = {}
    if uf_datalist and isinstance(uf_datalist[0], Uf):
        # Si datalist est une liste/QuerySet de Uf (avec data comme champ supplémentaire - annotation ou raw SQL) :
        for uf in uf_datalist:
            inv_datalist[uf.data] = inv_datalist.get(uf.data, set()) | {uf}
    else:
        # uf_datalist[1] = data doit sinon être un dict à un seul niveau (pas de dict de dict !)
        for uf, data in uf_datalist:
            # L'utilisation d'un frozenset(dict.items()) permet d'avoir des 'dict's hashables et consistents (et réversibles).
            val = frozenset(data.items())
            inv_datalist[val] = inv_datalist.get(val, set()) | {uf}

    outlist = []

    # entities_uf_sets = []
    for klass in class_list:
        # Toutes les structures actives de ce type/niveau
        all_entities = klass.objects.filter(cloture__isnull=True)
        for entity in all_entities:
            # Récupère la liste de toutes les UF actives de la structure
            ent_uf_set = set(entity.uf_set.filter(cloture__isnull=True))
            # Remplace :
            # if klass == Pole:
            #     ent_uf_set = set(Uf.objects.filter(pole=entity))
            # elif klass == Service:
            #     ent_uf_set = set(Uf.objects.filter(service=entity))

            # balaye les listes d'UF en entrée pour voir si elle contient les
            # UF de la structure
            for fdata, src_uf_set in inv_datalist.items():
                if ent_uf_set and ent_uf_set.issubset(src_uf_set):
                    # La structure n'est pas vide et elle est incluse dans la liste d'entrée !
                    # on l'ajoute à la liste de sortie
                    outlist.append(
                        (
                            entity,
                            fdata if not isinstance(fdata, frozenset) else dict(fdata),
                        )
                    )
                    # On épure la liste d'entrée (suppression des UF de la structure trouvée)
                    inv_datalist[fdata] = src_uf_set - ent_uf_set

    # Ajoute dans la liste de sortie toutes les UF seules qui n'ont pas été trouvées :
    # (et qui sont restées dans la liste d'entrée)
    for fdata, src_uf_set in inv_datalist.items():
        for uf in src_uf_set:
            outlist.append((uf, fdata if not isinstance(fdata, frozenset) else dict(fdata)))

    return outlist
