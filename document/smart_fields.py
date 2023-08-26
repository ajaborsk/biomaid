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
from django.apps import apps
from django.forms import ModelForm

import json

from django import forms
from django.utils.translation import gettext as _
from django.contrib.contenttypes.forms import generic_inlineformset_factory

from common import config
from document.models import GenericDocument, Document as NewDocument
from document.utils import document_get_or_create
from smart_view.smart_fields import ComputedSmartField, SmartFormat

sv_app_config = apps.get_app_config('smart_view')


class DocumentsSmartFormat(SmartFormat):
    class Media:
        js = (
            "smart_view/js/luxon.min.js",
            "smart_view/js/smart-view-documents.js",
        )

    def get_definition(self, target=None, view_params: dict = None):
        settings = super().get_definition(target, view_params)
        settings['mutator'] = "'json'"
        settings['mutator_params'] = {}
        settings['formatter'] = "'documents'"
        settings['formatter_params'] = {
            'media_url': config.settings.MEDIA_URL,
            'choices': {k: v for k, v in NewDocument.DOC_TYPE_CHOICES},
        }
        # settings['editor'] = "'documents'"
        # if 'editor_params' not in settings:
        #     settings['editor_params'] = {}
        settings['css_class'] = 'smart-view-vdiv-cell'
        return settings


class DocumentInlineForm(ModelForm):
    document_type = forms.ChoiceField(
        choices=NewDocument.DOC_TYPE_CHOICES,
        required=False,
        help_text=_("Choisissez le type de document"),
    )
    document_file = forms.FileField(required=False)
    document_comment = forms.CharField(required=False)
    # We don't use the formset DELETE feature since we want full control of action (to delete document and not only link)
    to_delete = forms.CharField(required=False)

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # print("Created form")
        # print("  fields", self.fields)
        if self.instance.pk is not None:
            # print("    instance !")
            self.fields['document_type'].initial = self.instance.document.doc_type
            self.fields['document_comment'].initial = self.instance.document.description

    def save(self, commit=True):
        # print("  files", self.files)
        if self.instance.pk is not None:
            # Only try to save user documents links
            if self.instance.user == self.user:
                if self.cleaned_data.get('to_delete'):
                    # For now, just delete the link. A reference counting system is needed to allow document deletion
                    self.instance.delete()
                else:
                    document = NewDocument.records.get(generic_document__pk=self.instance.pk)  # noqa
                    # print("Saving doc form...", dir(self))
                    # print("  instance", self.instance)
                    # print("  instance doc", document)
                    # print("  data", self.cleaned_data)
                    if (
                        self.cleaned_data['document_comment'] != document.description
                        or self.cleaned_data['document_type'] != document.doc_type
                    ):
                        document.description = self.cleaned_data['document_comment']
                        document.doc_type = self.cleaned_data['document_type']
                        document.save()
                        # print("    saved", document)
            else:
                pass
        else:
            # Save a new document anly if a file is provided...
            if self.cleaned_data['document_file']:
                document = document_get_or_create(
                    self.cleaned_data['document_file'],
                    owner=self.cleaned_data['user'],
                    doc_type=self.cleaned_data['document_type'],
                    description=self.cleaned_data['document_comment'],
                )
                self.instance.document = document
                super().save()

        return None


class DocumentsSmartField(ComputedSmartField):
    formset_model = GenericDocument
    subform_template = '%s/layout/generic_document_subform.html'
    extra = 10

    @classmethod
    def get_formset(cls):
        formset_class = generic_inlineformset_factory(
            cls.formset_model,
            form=DocumentInlineForm,
            exclude=['document'],
            extra=cls.extra,
        )
        formset_class.smart_field_class = cls
        return formset_class

    @classmethod
    def formset_initial(cls, user=None, **kwargs):
        return [{'user': user}]

    def __init__(self, *args, **kwargs):
        kwargs['format'] = 'documents'
        super().__init__(*args, **kwargs)

    @property
    def form_media(self):
        return forms.Media(
            css={
                'all': ['document/css/document-subform.css'],
            },
            js=[
                'document/js/document-subform.js',
            ],
        )

    def update_instance(self, request, instance, fieldname, updater, allowed=True):
        ######
        # WARNING : Ne fonctionne PAS !!!
        # L'ajout d'un document n'est pas aussi simple qu'un commentaire !!!
        ######
        # print("Updating instance {} with {}".format(instance, updater))
        document_data = json.loads(updater['set'][fieldname])
        # TODO : Three possibilities : Update a existing comment, append a new one or reply to a existing comment
        if 'add' in document_data:
            if document_data['add']:  # Do not create a empty comment
                document = GenericDocument(
                    content_object=instance,
                    user=request.user,
                    comment_type='DEFAULT',
                    comment_text=document_data['add'],
                )
                document.save()
            return {}

    def get_form_helper_rules(self, request, form_prefix=''):
        rules = {}

        for i in range(1, self.extra - 1):
            rules['document-show-{}'.format(i + 1)] = {
                'input_selectors': '.document-show-row-{} input'.format(i + 1),
                'func': 'show-if',
                'targets': ['.new-document-row-{}'.format(i + 1)],
            }

        return rules


sv_app_config.register_formats({'documents': DocumentsSmartFormat})
