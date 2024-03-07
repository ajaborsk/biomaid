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
"""
Formulaires

"""
import logging
import django.forms as forms

# from django import forms
from django.contrib.auth import get_user_model

from .models import (
    Dossier,
    Dra,
    Previsionnel,
    LigneCommande,
    ContactLivraison,
)
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget

from drachar.fields import ListTextWidget

logger = logging.getLogger(__name__)


class NouveauDossierForm(ModelForm, LoginRequiredMixin):

    participants = forms.ModelMultipleChoiceField(
        widget=FilteredSelectMultiple(_('participants'), False),
        queryset=get_user_model().objects.all(),
        label=_('Select tags'),
        required=False,
    )

    class Meta:
        model = Dossier
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = [
            'nom_dossier',
            # 'document',
            'participants',
            'proprietaire',
            'priorite_status',
            'priorite_classement',
            'deadline',
            'commentaire',
        ]
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }

    class Media:  # https://djangosnippets.org/snippets/2466/
        css = {
            'all': ['admin/css/widgets.css', 'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    """ _______________________Travail en cours récupération de la liste des experts__________________________
    """

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['document'].queryset = Document.objects.filter(createur=user, status=False)

    #    Roles = UserUfRole.objects.filter(role_code='EXP').values_list("id", flat=True)
    #    print(Roles)
    #    c = []
    #    for role in Roles:
    #        pk = UserUfRole.objects.get(pk=role).extension_user_id
    #        c.append(pk)
    #    print(c)
    #    self.fields['proprietaire'].queryset = ExtensionUser.objects.filter(pk__in=pk)
    """solution à étudier :"""
    #    all_experts = ExtensionUser.objects.filter(
    #        pk__in=Domaine.objects.all().values_list("expert").distinct()
    #    )
    #    experts = [
    #        {"id": str(expert.pk), "code": str(expert.initiales), "nom": str(expert)}
    #        for expert in all_experts
    #    ]

    # def save(self, commit=True):
    #    filter_by_qsets = {}
    #    for key in ['nom_dossier', 'document', 'proprietaire','priorite_status',
    #                'priorite_classement', 'date_deadline', 'participants']:
    #        val = self.cleaned_data.pop(key, None)  # The key is always gonna be in 'cleaned_data',
    #                                                # even if as an empty query set, so providing a default is
    #                                                # kind of... useless but meh... just in case
    #        if val:
    #            filter_by_qsets[key] = val  # This 'val' is still a queryset
    #
    #    # Manually populate the coupon's instance filter_by dictionary here
    #    self.instance.filter_by = {key: list(val.values_list('id', flat=True).order_by('id'))
    #                               for key, val in filter_by_qsets.items()}
    #    return super(NouveauDossier, self).save(commit=commit)
class XYZ_DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%d/%m/%Y"
        super().__init__(**kwargs)

class NouvelleDraForm(forms.ModelForm, LoginRequiredMixin):

    class Meta:
        model = Dra
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /

        # inscrits
        fields = [
            'intitule',
            'fournisseur',
            'contact_fournisseur',
            'num_devis',
            'date_devis',
            'num_marche',
            'programme',
            'expert_metier',
            'num_bon_commande',
            'date_commande',
            'num_dossier',
            # 'documents',
            'contact_livraison',
        ]
        widgets = {
            # 'intitule': forms.TextInput(attrs={ # Code pour ajout,
            #   'value':'test',
            # })
            # ici placer les surcharge des champs par défaut
            'date_devis': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'},
            ),
            #'date_devis': XYZ_DateInput(format=["%d/%m/%Y"],),
            'date_commande': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            )
        }

    def __init__(self, *args, **kwargs):
        _fournisseurs_list = kwargs.pop('four_list', None)
        _contact_fournisseur_list = kwargs.pop('contact_four_list', None)
        _marche_list = kwargs.pop('marche_list', None)
        _contact_liv_list = kwargs.pop('contact_liv_list', None)
        _expert_metier_list = kwargs.pop('expert_metier_list', None)
        _dossier_list = kwargs.pop('dossier_list', None)
        _user = kwargs.pop('user', None)
        _programme_list = kwargs.pop('programme_list', None)
        super(NouvelleDraForm, self).__init__(*args, **kwargs)
        if _fournisseurs_list is not None:
            self.fields['fournisseur'].widget = ListTextWidget(data_list=_fournisseurs_list, name='fournisseurs-list')
        if _contact_fournisseur_list is not None:
            self.fields['contact_fournisseur'].widget = ListTextWidget(
                data_list=_contact_fournisseur_list, name='contact_fournisseur-list'
            )
        if _marche_list is not None:
            self.fields['num_marche'].widget = ListTextWidget(data_list=_marche_list, name='marche-list')
        if _contact_liv_list is not None:
            self.fields['contact_livraison'].widget = ListTextWidget(data_list=_contact_liv_list, name='contact_liv-list')
        if _expert_metier_list is not None:
            self.fields['expert_metier'].widget = ListTextWidget(
                data_list=_expert_metier_list,
                name='expert_metier-list',
                attrs={'value': _user.id},
            )
            # self.initial['expert_metier'] = user
        if _dossier_list is not None:
            self.fields['num_dossier'].widget = ListTextWidget(data_list=_dossier_list, name='num_dossier-list')
        if _programme_list is not None:
            self.fields['programme'].widget = ListTextWidget(data_list=_programme_list, name='programme-list')

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class NouvelleLigneForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = [
            'num_previsionnel',
            'num_dra',
            'famille_achat',
            'num_compte',
            'a_inventorier',
            'classe',
            'cneh',
            'modele',
            'marque',
            'reference',
            'descriptif',
            'prix_unitaire_ht',
            'tva',
            'ref_mut',
            'eqpt_recup',
            'pv_reforme',
            'garantie',
            'date_reception',
            'date_mes',
        ]
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'num_dra': forms.HiddenInput(),
        }

        def __init__(self, kwargs):
            self.progid = kwargs.get('progid', None)
            self.numdra = kwargs.get('numdra', None)
            super(NouvelleLigneForm, self).__init__(kwargs)
            self.fields['num_previsionnel'].queryset = Previsionnel.objects.filter(num=self.progid)
            self.fields['num_dra'] = self.numdra

        #    def __init__(self, user, *args, **kwargs):
        #_numdra = kwargs.pop('numdra', None)
        #_numprevisionnel = kwargs.pop('num_previsionnel', None)
        #super(NouvelleLigneForm, self).__init__(*args, user, **kwargs)
        #if _numprevisionnel is not None:
        #    self.fields['num_previsionnel'].widget = ListTextWidget(data_list=_numprevisionnel, name='num_previsionnel')
        #if _numdra is not None:
        #    self.fields['num_dra'] = _numdra


class ContactLivForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = ContactLivraison
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


class Previsionnel(ModelForm, LoginRequiredMixin):
    class Meta:
        model = Previsionnel
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = []
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


# class DocForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
#         # inscrits
#         fields = '__all__'
#         widgets = {
#             # ici placer les surcharge des champs par défaut
#             # 'proprietaire': forms.HiddenInput(),
#         }


# class DocFormliendra(forms.ModelForm):
#     class Meta:
#         model = DocumentDracharLink
#         # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
#         # inscrits
#         fields = [
#             'dra',
#             'document',
#         ]
#         widgets = {
#             # ici placer les surcharge des champs par défaut
#             # 'proprietaire': forms.HiddenInput(),
#         }
