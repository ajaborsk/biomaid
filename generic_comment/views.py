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
import functools

from django.db.models import Value, TextField, Func, OuterRef, CharField
from django.db.models.functions import Concat, JSONObject, Cast, Coalesce
from django.contrib.contenttypes.models import ContentType

from common.db_utils import StringAgg
from generic_comment.models import GenericComment


class DateToChar(Func):
    function = 'to_char'

    def __ror__(self, other):
        raise NotImplementedError()

    def __rand__(self, other):
        raise NotImplementedError()


def _all_comments_json(model, view_params):  # NOQA (view_params is not used)
    model_id = ContentType.objects.get_for_model(model).id
    return Concat(
        Value('['),
        Coalesce(
            GenericComment.records.filter(
                content_type_id=model_id,
                object_id=Cast(OuterRef('pk'), output_field=CharField()),
            )
            .order_by()
            .values('content_type_id', 'object_id')
            .annotate(
                whole_text=StringAgg(
                    Cast(
                        JSONObject(
                            id='id',
                            reply='reply',
                            user='user',
                            user_first_name='user__first_name',
                            user_last_name='user__last_name',
                            text='comment_text',
                            type='comment_type',
                            timestamp='creation_timestamp',
                        ),
                        output_field=TextField(),
                    ),
                    ',',
                    output_field=TextField(),
                ),
            )
            .values('whole_text'),
            Value(''),
            output_field=TextField(),
        ),
        Value(']'),
        output_field=TextField(),
    )


def all_comments_json_partial(model):
    return functools.partial(_all_comments_json, model)
