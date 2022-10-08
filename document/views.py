#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
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
from __future__ import annotations

from collections.abc import Callable

import django.db.models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Value, TextField, OuterRef, Expression
from django.db.models.functions import Concat, Cast, JSONObject, Coalesce
import functools

# Create your views here.
from common.db_utils import StringAgg
from document.models import GenericDocument


def _all_documents_json(model: django.db.models.Model, name: str | None, view_params: dict) -> Expression:
    """
    Django expression to get generic documents data in a json strings

    Given a model, a (field) name and a view_params,
    returns a Django expression that give (once used in a annotation),
    a json string with a list of document records.

    Each record has the following fields :
       - id : The document id (pk)
       - user : the user who created the document link
       - user_first_name : This user's first name
       - user_last_name : This user's last name

    :param model: The Django model to which documents are attached
    :param name: A arbitrary name (id) of the document ``field`` (to distinct several documents list on the same model).
    :param view_params: Unused view_params

    :returns: A Django expression that give (once used in a querystring ``annotate()`` for instance),
                a json string with a list of document records.
    """
    model_id = ContentType.objects.get_for_model(model).id
    return Concat(
        Value('['),
        Coalesce(
            GenericDocument.objects.filter(content_type_id=model_id, object_id=OuterRef('pk'), name=name)
            .order_by()
            .values('content_type_id', 'object_id')
            .annotate(
                whole_text=StringAgg(
                    Cast(
                        JSONObject(
                            id='id',
                            user='user',
                            user_first_name='user__first_name',
                            user_last_name='user__last_name',
                            description='document__description',
                            type='document__doc_type',
                            filename='document__logical_path',
                            link='document__physical_path',
                            timestamp='creation_datetime',
                        ),
                        output_field=TextField(),
                    ),
                    ',',
                    output_field=TextField(),
                )
            )
            .values('whole_text'),
            Value(''),
            output_field=TextField(),
        ),
        Value(']'),
        output_field=TextField(),
    )


def all_documents_json_partial(model: django.db.models.Model, name: str | None = None) -> Callable[dict, Expression]:
    return functools.partial(_all_documents_json, model, name)
