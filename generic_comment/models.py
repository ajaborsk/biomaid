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
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from overoly.base import OverolyModel as Model

class GenericComment(Model):
    # If not null, the comment of wich it's a reply
    reply = models.ForeignKey(
        'generic_comment.GenericComment',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    # The comment recipient (optional, can be NULL)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Destinataire"),
        null=True,
        blank=True,
        related_name='recipient_comments',
    )

    # If a comment is private, it's only visible to the recipient
    private = models.BooleanField(verbose_name=_("Privé"), default=False)

    # The comment author
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Rédacteur"))

    # ? Unused
    comment_type = models.CharField(max_length=256, null=True, blank=True)

    # The comment (text ; no HTML for now)
    comment_text = models.TextField()

    creation_timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    modification_timestamp = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    desactivated_timestamp = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.CharField(max_length=256)
    content_object = GenericForeignKey('content_type', 'object_id')

    # AJA: Définir une méthode __str__ conduit parfois à un plantage que je ne comprends pas...
    #       Peut-être à explorer un jour...
    # def __str__(self):
    #     return (
    #         repr(self.user)
    #         + " / "
    #         + self.comment_type
    #         + " : "
    #         + self.comment_text[:64]
    #         + ('...' if len(self.comment_text) > 64 else '')
    #     )
