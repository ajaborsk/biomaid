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
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms import ModelForm

from generic_comment.models import GenericComment
from smart_view.smart_fields import SmartFormat, ComputedSmartField

sv_app_config = apps.get_app_config('smart_view')


class CommentsSmartFormat(SmartFormat):
    class Media:
        js = (
            "smart_view/js/luxon.min.js",
            "smart_view/js/smart-view-comments.js",
        )

    def get_definition(self, target=None, view_params: dict = None):
        settings = super().get_definition(target, view_params)
        settings['formatter'] = "'comments'"
        settings['mutator'] = "'json'"
        settings['mutator_params'] = {}
        settings['editor'] = "'comments'"
        if 'editor_params' not in settings:
            settings['editor_params'] = {}
        settings['css_class'] = 'smart-view-vdiv-cell'
        return settings


class CommentsInlineForm(ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


class CommentsSmartField(ComputedSmartField):

    formset_model = GenericComment
    subform_template = '%s/layout/generic_comment_subform.html'

    @classmethod
    def get_formset(cls):
        formset_class = generic_inlineformset_factory(GenericComment, form=CommentsInlineForm, extra=1)
        formset_class.smart_field_class = cls
        return formset_class

    @classmethod
    def formset_initial(cls, user=None, **kwargs):
        return [{'user': user}]

    def __init__(self, *args, user=None, **kwargs):
        kwargs['format'] = 'comments'
        self.user = user
        super().__init__(*args, **kwargs)

    def update_instance(self, request, instance, fieldname, updater, allowed=True):
        # print("Updating instance {} with {}".format(instance, updater))
        comment_data = updater['set'][fieldname]
        # TODO : Three possibilities : Update a existing comment, append a new one or reply to a existing comment
        if 'add' in comment_data:
            if comment_data['add']:  # Do not create a empty comment
                comment = GenericComment(
                    content_object=instance,
                    user=request.user,
                    comment_type='DEFAULT',
                    comment_text=comment_data['add'],
                )
                comment.save()
            return {}


sv_app_config.register_formats({'comments': CommentsSmartFormat})
