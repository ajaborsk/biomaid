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


class Document(models.Model):
    class Meta:
        indexes = [models.Index(fields=['hash'])]

    DOC_TYPE_CHOICES = (
        ('DE', "Devis"),
        ('CO', "Doc commerciale"),
        ('CR', "Email, courrier"),
        ('IM', "Photo"),
        ('AS', "Article scientifique"),
        ('TR', "Texte réglementaire"),
        ('RE', "Recommandations"),
        ('RC', "Compte-rendu"),
        ('PM', "Planning de mutualisation"),
        ('BP', "Business Plan"),
        ('ME', "Etude médico-économique"),
        ('TE', "Doc technique"),
        ('DRA', "Demande de Réalisation d'Achat"),
        ('REF', "Bon de demande de réforme"),
        ('DI', "Autre document"),
        ('PL', "Plan, schéma"),
    )

    # Where the file is stored
    physical_path = models.CharField(max_length=2048)

    # Where the file looks like stored
    logical_path = models.CharField(max_length=2048)

    # Who did upload the file
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # A file description
    description = models.TextField(null=True, blank=True)

    hash = models.CharField(max_length=256, null=True, blank=True)
    mime_type = models.CharField(max_length=2048, null=True, blank=True)

    doc_type = models.CharField(  # type de document
        max_length=8,
        choices=DOC_TYPE_CHOICES,
        blank=True,
        verbose_name=_("Type"),
        help_text=_("Choisissez le type du document à joindre"),
    )

    creation = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    modification = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    desactivation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_doc_type_display()}: '{self.logical_path}' ({self.description})"


class GenericDocument(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name='generic_document')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Créateur du lien"),
    )
    comment = models.TextField(verbose_name=_("Remarque sur le lien (facultatif)"), null=True, blank=True)

    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    modification_datetime = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    desactivation_datetime = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')
