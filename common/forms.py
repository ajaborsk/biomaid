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
from django import forms
from django.contrib.auth import get_user_model

from common.models import (
    Fournisseur,
    ContactFournisseur,
    Type,
    Marque,
    Compte,
    Uf,
    Pole,
    Service,
    CentreResponsabilite,
    Site,
    Etablissement,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = [
#             'first_name',
#             'last_name',
#             'email',
#         ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'titre',
            'first_name',
            'last_name',
            'email',
            'intitule_fonction',
            'initiales',
            'tel_fixe',
            'tel_dect',
            'tel_mobile',
        ]


class BiomAidUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'email',
        )
        model = get_user_model()

    intitule_fonction = forms.CharField(
        label=get_user_model().intitule_fonction.field.verbose_name,
        help_text=get_user_model().intitule_fonction.field.help_text,
        max_length=get_user_model().intitule_fonction.field.max_length,
        required=False,
    )
    initiales = forms.CharField(
        label=get_user_model().initiales.field.verbose_name,
        help_text=get_user_model().initiales.field.help_text,
        max_length=get_user_model().initiales.field.max_length,
        required=False,
    )
    tel_fixe = forms.CharField(
        label=get_user_model().tel_fixe.field.verbose_name,
        help_text=get_user_model().tel_fixe.field.help_text,
        max_length=get_user_model().tel_fixe.field.max_length,
        required=False,
    )
    tel_dect = forms.CharField(
        label=get_user_model().tel_dect.field.verbose_name,
        help_text=get_user_model().tel_dect.field.help_text,
        max_length=get_user_model().tel_dect.field.max_length,
        required=False,
    )
    tel_mobile = forms.CharField(
        label=get_user_model().tel_mobile.field.verbose_name,
        help_text=get_user_model().tel_mobile.field.help_text,
        max_length=get_user_model().tel_mobile.field.max_length,
        required=False,
    )


class FournisseurForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Fournisseur
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


class ContactFournisseurForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = ContactFournisseur
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


class TypeForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Type
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


class MarqueForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Marque
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


class CompteForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Compte
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }


class UfForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Uf
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }

    def __init__(self, kwargs):
        self.etabid = kwargs.get('etabid', None)
        super(UfForm, self).__init__(kwargs)
        self.fields['etablissement'].queryset = Etablissement.objects.filter(code=self.etabid)
        self.fields['pole'].queryset = Pole.objects.filter(etablissement=self.etabid)
        self.fields['site'].queryset = Site.objects.filter(etablissement=self.etabid)
        self.fields['centre_responsabilite'].queryset = Site.objects.filter(etablissement=self.etabid)
        self.fields['service'].queryset = Site.objects.filter(etablissement=self.etabid)


class PoleForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Pole
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }

    def __init__(self, kwargs):
        self.etabid = kwargs.get('etabid', None)
        super(PoleForm, self).__init__(kwargs)
        self.fields['etablissement'].queryset = Etablissement.objects.filter(code=self.etabid)


class ServiceForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Service
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }

    def __init__(self, kwargs):
        self.etabid = kwargs.get('etabid', None)
        super(ServiceForm, self).__init__(kwargs)
        self.fields['etablissement'].queryset = Etablissement.objects.filter(code=self.etabid)


class CentreResponsabiliteForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = CentreResponsabilite
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }

    def __init__(self, kwargs):
        self.etabid = kwargs.get('etabid', None)
        super(CentreResponsabiliteForm, self).__init__(kwargs)
        self.fields['etablissement'].queryset = Etablissement.objects.filter(code=self.etabid)


class SiteForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Site
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }

    def __init__(self, kwargs):
        self.etabid = kwargs.get('etabid', None)
        super(SiteForm, self).__init__(kwargs)
        self.fields['etablissement'].queryset = Etablissement.objects.filter(code=self.etabid)


class EtablissementForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Etablissement
        # ici placer les champs du model à traiter dans le formulaire : les champs automatiques ne doivent pas être /
        # inscrits
        fields = '__all__'
        widgets = {
            # ici placer les surcharge des champs par défaut
            # 'proprietaire': forms.HiddenInput(),
        }
