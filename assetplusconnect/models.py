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

from __future__ import unicode_literals

import datetime
from typing import Any

from django.db import models
from django.db.models import DateField
from django.utils.translation import gettext as _

# Create your models here.


class AssetPlusDate1(DateField):
    """
    Convertit une date stockée sous la forme d'une chaîne de format 'YYYY-MM-DD' dans Asset+
    vers un véritable datetime.date() Python
    """

    def from_db_value(self, value, expression, connection):
        if value:
            return datetime.date(int(value[0:4]), int(value[5:7]), int(value[8:10]))
        else:
            return None


class AssetPlusDate2(DateField):
    """
    Convertit un datetime stockée sous la forme d'une chaîne de format 'YYYYMMDDhhmmsslll' dans Asset+
    YYYY = Année
    MM = Mois
    DD = Jour du mois
    hh = heure
    mm = minutes
    lll = millisecondes
    vers un véritable datetime.datetime() Python
    """

    def get_prep_value(self, value: Any) -> Any:
        if value:
            return value.strftime('%Y%m%d%H%M%S%f')[:17]

    def from_db_value(self, value, expression, connection):
        try:
            if isinstance(value, str):
                if len(value) == 17:
                    return datetime.datetime(
                        int(value[0:4]),
                        int(value[4:6]),
                        int(value[6:8]),
                        hour=int(value[8:10]),
                        minute=int(value[10:12]),
                        second=min(59, int(value[12:14])),
                        microsecond=int(value[14:17]) * 1000,
                    )
                elif len(value) == 14:
                    return datetime.datetime(
                        int(value[0:4]),
                        int(value[4:6]),
                        int(value[6:8]),
                        hour=int(value[8:10]),
                        minute=int(value[10:12]),
                        second=min(59, int(value[12:14])),
                    )
                else:
                    print("Unable to extract timestamp from Asset+ value '{}'".format(value))
                    return datetime.datetime(2000, 1, 1)
        except ValueError:
            print("Unable to extract timestamp from Asset+ value '{}'".format(value))
            return datetime.datetime(2000, 1, 1)


class AssetPlusDate3(DateField):
    """
    Convertit une date stockée sous la forme d'une chaîne de format 'YYYYMMDD' dans Asset+
    YYYY = Année
    MM = Mois
    DD = Jour du mois
    vers un véritable datetime.date() Python
    """

    def get_prep_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return datetime.date.fromisoformat(value).strftime('%Y%m%d')
        else:
            return value.strftime('%Y%m%d')

    def from_db_value(self, value, expression, connection):
        try:
            if isinstance(value, str):
                if len(value) == 8:
                    return datetime.date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
                else:
                    print("Unable to extract timestamp from Asset+ value '{}'".format(value))
                    return datetime.date(2000, 1, 1)
        except ValueError:
            print("Unable to extract timestamp from Asset+ value '{}'".format(value))
            return datetime.date(2000, 1, 1)


class SuiviUpdates(models.Model):
    table: models.CharField = models.CharField(
        verbose_name=_("Table modifiée"),
        max_length=128,
        null=False,
        blank=False,
    )
    date_modification: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name=_("date de modification"))


# TABLE DES MARQUES DANS ASSET+
class Marques(models.Model):
    ma_nom: models.TextField = models.TextField(primary_key=True)
    insert_date = AssetPlusDate2(blank=True, null=True)
    update_date = AssetPlusDate2(blank=True, null=True)
    date_refor: models.DateField = models.DateField(blank=True, null=True)
    multi_marc: models.TextField = models.TextField(blank=True, null=True)
    technical_id: models.TextField = models.TextField(blank=True, null=True)
    auto_id: models.BigIntegerField = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'marques'

    def __str__(self):
        return self.ma_nom, self.insert_date


# TABLE DES TYPES/MODELS DANS ASSET+
class Types(models.Model):
    tp_type: models.TextField = models.TextField(primary_key=True)
    marque: models.TextField = models.TextField()
    four_type: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    cneh_type: models.TextField = models.TextField(blank=True, null=True)
    nom2: models.TextField = models.TextField(blank=True, null=True)
    code_ecri: models.TextField = models.TextField(blank=True, null=True)
    nom2_ecri: models.TextField = models.TextField(blank=True, null=True)
    para1: models.TextField = models.TextField(blank=True, null=True)
    para2: models.TextField = models.TextField(blank=True, null=True)
    para3: models.TextField = models.TextField(blank=True, null=True)
    para4: models.TextField = models.TextField(blank=True, null=True)
    para5: models.TextField = models.TextField(blank=True, null=True)
    insert_date = AssetPlusDate2(blank=True, null=True)
    update_date = AssetPlusDate2(blank=True, null=True)
    voc_fonc: models.TextField = models.TextField(blank=True, null=True)
    criticite: models.TextField = models.TextField(blank=True, null=True)
    classe_eqp: models.TextField = models.TextField(blank=True, null=True)
    asset_part_type: models.TextField = models.TextField(blank=True, null=True)
    date_refor: models.TextField = models.TextField(blank=True, null=True)
    multi_marc: models.TextField = models.TextField(blank=True, null=True)
    fk_techfamily_code_fam: models.TextField = models.TextField(blank=True, null=True)
    is_rfid_tag: models.BooleanField = models.BooleanField(null=True)
    remp_prix: models.TextField = models.TextField(blank=True, null=True)
    typ_obsolescence_date: models.TextField = models.TextField(blank=True, null=True)
    technical_id: models.TextField = models.TextField(blank=True, null=True)
    auto_id: models.BigIntegerField = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'types'
        unique_together = (('tp_type', 'marque'),)

    def __str__(self):
        return self.ma_tp


class Fournis2(models.Model):
    code_four: models.CharField = models.CharField(primary_key=True, max_length=10)
    f_cle_comp: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    fourni: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_resp: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_adr: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_pays: models.CharField = models.CharField(max_length=3, blank=True, null=True)
    f_codp: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    f_vill: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_mailing: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_adr_1_2: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_tel: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_fax: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_resp2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_adr2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_pays2: models.CharField = models.CharField(max_length=3, blank=True, null=True)
    f_codp2: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    f_vill2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_tel2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_fax2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    xx: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_form_jur: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_rc: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_siret: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ape: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_adr_obs: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    xxxx: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_trav_ent: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_spec_ent: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_trav_equ: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_qualif: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_classif: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_opqcb: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_spec: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_qual_obs: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    yyy: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_ass_rc: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ass_cons: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ca_kf: models.IntegerField = models.IntegerField(blank=True, null=True)
    f_jurid: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    f_jurid_ob: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_rouge: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_rouge_da: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_rouge_ob: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_obs_gen: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_marche_i: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_comm: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    actif: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    f_seuil: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    ad_email: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_site: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    f_state: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_state2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    supplier_parent_number: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    supplier_tree_path: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    supplier_tree_level: models.IntegerField = models.IntegerField(blank=True, null=True)
    financial_account_id: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler6: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler8: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler9: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler10: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id: models.BigIntegerField = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'fournis2'


# TABLE DE L'INVENTAIRE DANS ASSET+
class BEq1996(models.Model):
    n_imma: models.CharField = models.CharField(max_length=64, primary_key=True)  # This field type is a guess.
    n_nom_cneh: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    ef_typ: models.CharField = models.CharField(max_length=25, blank=True, null=True)
    poste_w: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    typ_mod: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    mes1: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    dpo: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    fdg: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    mhs: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    fdg_constr: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    date_refor: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    ind_maint: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_maint: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    c_ind_main: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    unit_st: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix_fau: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_m_an_bas: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    n_marche: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    m_an_effet: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    p_m_tempor: models.IntegerField = models.IntegerField(blank=True, null=True)
    p_m_vetust: models.IntegerField = models.IntegerField(blank=True, null=True)
    p_m_prix_n: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    h_exploit: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    vac_ht: models.CharField = models.CharField(max_length=6, blank=True, null=True)
    fre_mp: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    pd_mp: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    nb_vcm: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    dmcd_b: models.IntegerField = models.IntegerField(blank=True, null=True)
    pd_mc: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    pd_seuil: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_ar_bl: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    dmi: models.IntegerField = models.IntegerField(blank=True, null=True)
    t_im: models.CharField = models.CharField(max_length=7, blank=True, null=True)
    crit_ac: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    crit_act: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    dit_tc: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    dit_disf: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    nbt_ab_tc: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbt_ab_dis: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vp: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbh_vp: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vc: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vcu: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbh_vc: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vat: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vatu: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbh_vat: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    dm_di: models.IntegerField = models.IntegerField(blank=True, null=True)
    dm_cd: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_co_en: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_pd: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_mo: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_dep: models.IntegerField = models.IntegerField(blank=True, null=True)
    dit_tci: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    dit_disfi: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    nbt_ab_tci: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbt_b_disi: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vpi: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbh_vpi: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vci: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vcui: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbh_vci: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vati: models.IntegerField = models.IntegerField(blank=True, null=True)
    nb_vatui: models.IntegerField = models.IntegerField(blank=True, null=True)
    nbh_vati: models.IntegerField = models.IntegerField(blank=True, null=True)
    dm_dii: models.IntegerField = models.IntegerField(blank=True, null=True)
    dm_cdi: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_co_eni: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_pdi: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_moi: models.IntegerField = models.IntegerField(blank=True, null=True)
    mt_depi: models.IntegerField = models.IntegerField(blank=True, null=True)
    d_dern_int: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    d_der_i_c: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    d_der_i_p: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    nbh_fonc: models.IntegerField = models.IntegerField(blank=True, null=True)
    date_syst: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    be1numseco: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    be2implant: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    equal_lib1: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    equal_lib2: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    equal_lib3: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    equal_lib4: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    lib1_min: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib1_max: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib1_param: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib2_min: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib2_max: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib2_param: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib3_min: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib3_max: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib3_param: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib4_min: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib4_max: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    lib4_param: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    qual_r_p: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    qual_r_m: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    qual_i_e: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    secu_indus: models.CharField = models.CharField(max_length=50, blank=True, null=True)
    secu_nbvis: models.IntegerField = models.IntegerField(blank=True, null=True)
    secu_act: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    secu_cpt: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    ex_n_uf: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    remp_prix: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    remp_obs: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    etiquetage: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    filler1: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler6: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    id_usertable2: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    id_usertable3: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    id_usertable4: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    id_usertable5: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    workgroup: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    ip_address: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    mat_address: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_plug: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_port: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_it_user: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    fk_etabli_n_etab: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_in_site: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    eq_amt_com: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    criticite: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_eqp: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_produit_four: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_client_four: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic: models.IntegerField = models.IntegerField(blank=True, null=True)
    from_module: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    d_pro_i_p: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_request_refor: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_request_int: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_order: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_recept_order: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_request_int: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_order: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo: models.CharField = models.CharField(max_length=4, blank=True, null=True)
    n_imma_replace: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler_eco_1: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler_eco_2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler_eco_3: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_eco_1: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_eco_2: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_eco_3: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    tagid: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    zoneid: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    zonegroupid: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    zoneowning_id: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    dwell_time: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    x_ft: models.IntegerField = models.IntegerField(blank=True, null=True)
    y_ft: models.IntegerField = models.IntegerField(blank=True, null=True)
    is_tester: models.IntegerField = models.IntegerField(blank=True, null=True)
    el_fix_generic_quantity: models.IntegerField = models.IntegerField(blank=True, null=True)
    asset_status: models.IntegerField = models.IntegerField(blank=True, null=True)
    asset_sub_status: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    mac_address: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_rfid_tag = models.BooleanField(null=True)
    nb_vcq: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    interface: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd_mp_int = models.BooleanField(null=True)
    pd_mc_int = models.BooleanField(null=True)
    id_usertable6: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    id_usertable7: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    id_usertable8: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    fk_all_pictures_id: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    udi: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    eqp_secondary_td: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id: models.BigIntegerField = models.BigIntegerField(unique=True)
    fabriquant: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    centrale_achat: models.TextField = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_asset_status: models.IntegerField = models.IntegerField(blank=True, null=True)
    lib_assetstatus = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_dgos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'b_eq1996'

    def __str__(self):
        return self.n_imma


class EqCneh(models.Model):
    n_nom_cneh = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specc = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ret: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    eq_amt_com = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_ac = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    remp_prix = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch5: models.IntegerField = models.IntegerField(blank=True, null=True)
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    riskcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    ecr_modcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'eq_cneh'

    def __str__(self):
        return self.n_nom_cneh


class Contact(models.Model):
    nu_contact: models.CharField = models.CharField(primary_key=True, max_length=10)
    nu_four: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    adr = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_p = models.TextField(blank=True, null=True)  # This field type is a guess.
    ville = models.TextField(blank=True, null=True)  # This field type is a guess.
    tel1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fax1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    tel2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    cout_dep = models.TextField(blank=True, null=True)  # This field type is a guess.
    cout_mo = models.TextField(blank=True, null=True)  # This field type is a guess.
    fonction = models.TextField(blank=True, null=True)  # This field type is a guess.
    description: models.IntegerField = models.IntegerField(blank=True, null=True)
    ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    state = models.TextField(blank=True, null=True)  # This field type is a guess.
    contact_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact'

    def __str__(self):
        return self.nom


class ContactDescription(models.Model):
    id: models.IntegerField = models.IntegerField(primary_key=True)  # AutoField?
    name = models.TextField(unique=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact_description'

    def __str__(self):
        return self.name


class ContactPerson(models.Model):
    id: models.BigIntegerField = models.BigIntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fax = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_address_id: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    fk_territory_id: models.BigIntegerField = models.BigIntegerField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact_person'

    def __str__(self):
        return self.name


class Budget(models.Model):
    nu_compte = models.TextField(primary_key=True)  # This field type is a guess.
    lib_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_cumul = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_an: models.IntegerField = models.IntegerField(blank=True, null=True)
    an_exo: models.CharField = models.CharField(max_length=4)
    mt_annuel = models.TextField(blank=True, null=True)  # This field type is a guess.
    obs_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    financial_period_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    financial_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_expenses_calculated = models.BooleanField(null=True)
    total_expenses_input = models.TextField(blank=True, null=True)  # This field type is a guess.
    latest_expenses_input_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    latest_expenses_input_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'budget'
        unique_together = (('nu_compte', 'an_exo'),)

    def __str__(self):
        return self.nu_compte


class EnCours(models.Model):
    nu_int: models.CharField = models.CharField(max_length=64, primary_key=True)  # This field type is a guess.
    nu_bon_c: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    nu_imm: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    n_uf: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    n_ef: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    da_ap = AssetPlusDate1(blank=True, null=True)
    he_ap: models.CharField = models.CharField(max_length=8, blank=True, null=True)
    da_int = AssetPlusDate1(blank=True, null=True)
    he_int: models.CharField = models.CharField(max_length=8, blank=True, null=True)
    da_hs = AssetPlusDate1(blank=True, null=True)
    he_hs: models.CharField = models.CharField(max_length=8, blank=True, null=True)
    da_dis = AssetPlusDate1(blank=True, null=True)
    he_dis: models.CharField = models.CharField(max_length=8, blank=True, null=True)
    da_fin = AssetPlusDate1(blank=True, null=True)
    he_fin: models.CharField = models.CharField(max_length=8, blank=True, null=True)
    urg = models.CharField(max_length=1, blank=True, null=True)
    disp_ef_at: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    disp_ap_at: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    compt: models.IntegerField = models.IntegerField(blank=True, null=True)
    cadre: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    nhe = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_fac: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    cod_sais: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    pd1_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd2_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    mo_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    dep_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    hint = models.TextField(blank=True, null=True)  # This field type is a guess.
    cdep = models.TextField(blank=True, null=True)  # This field type is a guess.
    piec = models.TextField(blank=True, null=True)  # This field type is a guess.
    cint: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    ana_def: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    rem_a_disp: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    r_a_d_suit: models.CharField = models.CharField(max_length=50, blank=True, null=True)
    code_four: models.CharField = models.CharField(max_length=10, blank=True, null=True)
    code_techn: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    m_an_effet: models.CharField = models.CharField(max_length=2, blank=True, null=True)
    observ2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    e_refer: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    dit_tcmn: models.IntegerField = models.IntegerField(blank=True, null=True)
    int_statut: models.CharField = models.CharField(max_length=20, blank=True, null=True)
    int_cm: models.CharField = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    int_cause = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_remed = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_contra: models.CharField = models.CharField(max_length=1, blank=True, null=True)
    interloc = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    hlimit: models.CharField = models.CharField(max_length=5, blank=True, null=True)
    w_nature = models.TextField(blank=True, null=True)  # This field type is a guess.
    nhee = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_compte = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    date_syst = models.CharField(max_length=10, blank=True, null=True)
    da_rec = AssetPlusDate1(blank=True, null=True)
    he_rec = models.CharField(max_length=8, blank=True, null=True)
    delai: models.IntegerField = models.IntegerField(blank=True, null=True)
    code_delai = models.CharField(max_length=1, blank=True, null=True)
    da_hdelai = AssetPlusDate1(blank=True, null=True)
    n_devis = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_facture = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_engag = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    da_recp = AssetPlusDate1(blank=True, null=True)
    tot_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_cadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_statut = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    par1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_contact_person_id = models.BigIntegerField(blank=True, null=True)
    fk_address_id = models.BigIntegerField(blank=True, null=True)
    date_of_nu_bon_c = AssetPlusDate1(blank=True, null=True)
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodela = models.IntegerField(blank=True, null=True)
    da_dd = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_dr = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_da = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_web = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimatedduration = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    generic_seq = models.IntegerField(blank=True, null=True)
    tolerance = models.IntegerField(blank=True, null=True)
    tolerance_dmy = models.IntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    mode_calcul_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodicity_occurrence = models.IntegerField(blank=True, null=True)
    periodicity_dmy = models.IntegerField(blank=True, null=True)
    filler6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)
    id_usertable3 = models.BigIntegerField(blank=True, null=True)
    id_usertable4 = models.BigIntegerField(blank=True, null=True)
    id_usertable5 = models.BigIntegerField(blank=True, null=True)
    nb_asset_generic = models.IntegerField(blank=True, null=True)
    nb_tot_asset_generic = models.IntegerField(blank=True, null=True)
    amount_quote = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    wo_parent_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_tree_path = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_tree_level = models.IntegerField(blank=True, null=True)
    quick_wo_use = models.IntegerField(blank=True, null=True)
    quick_wo_result = models.IntegerField(blank=True, null=True)
    wo_updated_historic = models.TextField(blank=True, null=True)
    filler8 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler9 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler11 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler12 = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_buyer_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable2_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable3_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable4_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable5_wo = models.BigIntegerField(blank=True, null=True)
    caller_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_caller_notified = models.IntegerField(blank=True, null=True)
    maxdateresponse = models.TextField(blank=True, null=True)  # This field type is a guess.
    maxtimeresponse = models.TextField(blank=True, null=True)  # This field type is a guess.
    old_counter = models.IntegerField(blank=True, null=True)
    periode = models.CharField(max_length=1, blank=True, null=True)
    is_digital_sign = models.BooleanField(
        null=True,
    )
    is_wo_sign_mandatory = models.BooleanField(
        null=True,
    )
    competency_is_activated = models.BooleanField(
        null=True,
    )
    id_usertable6 = models.BigIntegerField(blank=True, null=True)
    id_usertable7 = models.BigIntegerField(blank=True, null=True)
    id_usertable8 = models.BigIntegerField(blank=True, null=True)
    wo_forward_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_decontaminated = models.TextField(blank=True, null=True)  # This field type is a guess.
    response_time_calcul_mode = models.BooleanField(
        null=True,
    )
    udi = models.TextField(blank=True, null=True)  # This field type is a guess.
    call_creator = models.TextField(blank=True, null=True)  # This field type is a guess.
    autodispatch_notif_status = models.BooleanField(
        null=True,
    )
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_prev_eqp = models.BigIntegerField(blank=True, null=True)
    date_prev_calculated = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_ge_wonum = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_user_creator = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_prep_id = models.BigIntegerField(blank=True, null=True)
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)
    order_amount = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc_plus_ord_am = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'en_cours'


class BFt1996(models.Model):
    nu_int = models.CharField(max_length=64, primary_key=True)  # This field type is a guess.
    nu_bon_c = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    nu_imm = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    n_ef = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    da_ap = AssetPlusDate1(blank=True, null=True)
    he_ap = models.CharField(max_length=8, blank=True, null=True)
    da_int = AssetPlusDate1(blank=True, null=True)
    he_int = models.CharField(max_length=8, blank=True, null=True)
    da_hs = AssetPlusDate1(blank=True, null=True)
    he_hs = models.CharField(max_length=8, blank=True, null=True)
    da_dis = AssetPlusDate1(blank=True, null=True)
    he_dis = models.CharField(max_length=8, blank=True, null=True)
    da_fin = AssetPlusDate1(blank=True, null=True)
    he_fin = models.CharField(max_length=8, blank=True, null=True)
    urg = models.CharField(max_length=1, blank=True, null=True)
    disp_ef_at = models.CharField(max_length=1, blank=True, null=True)
    disp_ap_at = models.CharField(max_length=1, blank=True, null=True)
    compt = models.IntegerField(blank=True, null=True)
    cadre = models.CharField(max_length=1, blank=True, null=True)
    nhe = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_fac = models.CharField(max_length=1, blank=True, null=True)
    cod_sais = models.CharField(max_length=1, blank=True, null=True)
    pd1_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd2_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    mo_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    dep_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    hint = models.TextField(blank=True, null=True)  # This field type is a guess.
    cdep = models.TextField(blank=True, null=True)  # This field type is a guess.
    piec = models.TextField(blank=True, null=True)  # This field type is a guess.
    cint = models.CharField(max_length=1, blank=True, null=True)
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    ana_def = models.CharField(max_length=1, blank=True, null=True)
    rem_a_disp = models.CharField(max_length=1, blank=True, null=True)
    r_a_d_suit = models.CharField(max_length=50, blank=True, null=True)
    code_four = models.CharField(max_length=10, blank=True, null=True)
    code_techn = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    m_an_effet = models.CharField(max_length=2, blank=True, null=True)
    observ2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    e_refer = models.CharField(max_length=1, blank=True, null=True)
    dit_tcmn = models.IntegerField(blank=True, null=True)
    int_statut = models.CharField(max_length=20, blank=True, null=True)
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cause = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_remed = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_contra = models.CharField(max_length=1, blank=True, null=True)
    interloc = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    hlimit = models.CharField(max_length=5, blank=True, null=True)
    w_nature = models.TextField(blank=True, null=True)  # This field type is a guess.
    nhee = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    dm_dii = models.IntegerField(blank=True, null=True)
    dm_di = models.IntegerField(blank=True, null=True)
    nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_syst = AssetPlusDate1(blank=True, null=True)
    da_rec = AssetPlusDate1(blank=True, null=True)
    he_rec = models.CharField(max_length=8, blank=True, null=True)
    delai = models.IntegerField(blank=True, null=True)
    code_delai = models.CharField(max_length=1, blank=True, null=True)
    da_hdelai = models.CharField(max_length=10, blank=True, null=True)
    n_devis = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_facture = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_engag = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_recp = AssetPlusDate1(blank=True, null=True)
    div_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_cadre = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    lib_statut = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    par1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_contact_person_id = models.BigIntegerField(blank=True, null=True)
    fk_address_id = models.BigIntegerField(blank=True, null=True)
    date_of_nu_bon_c = models.CharField(max_length=10, blank=True, null=True)
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodela = models.IntegerField(blank=True, null=True)
    da_dd = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_dr = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_da = models.TextField(blank=True, null=True)  # This field type is a guess.
    from_web = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimatedduration = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    generic_seq = models.IntegerField(blank=True, null=True)
    tolerance = models.IntegerField(blank=True, null=True)
    tolerance_dmy = models.IntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    mode_calcul_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodicity_occurrence = models.IntegerField(blank=True, null=True)
    periodicity_dmy = models.IntegerField(blank=True, null=True)
    filler6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)
    id_usertable3 = models.BigIntegerField(blank=True, null=True)
    id_usertable4 = models.BigIntegerField(blank=True, null=True)
    id_usertable5 = models.BigIntegerField(blank=True, null=True)
    nb_asset_generic = models.IntegerField(blank=True, null=True)
    nb_tot_asset_generic = models.IntegerField(blank=True, null=True)
    amount_quote = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    wo_parent_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_tree_path = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_tree_level = models.IntegerField(blank=True, null=True)
    quick_wo_use = models.IntegerField(blank=True, null=True)
    quick_wo_result = models.IntegerField(blank=True, null=True)
    wo_updated_historic = models.TextField(blank=True, null=True)
    filler8 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler9 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler11 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler12 = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_buyer_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable2_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable3_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable4_wo = models.BigIntegerField(blank=True, null=True)
    id_usertable5_wo = models.BigIntegerField(blank=True, null=True)
    caller_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_caller_notified = models.IntegerField(blank=True, null=True)
    maxdateresponse = models.TextField(blank=True, null=True)  # This field type is a guess.
    maxtimeresponse = models.TextField(blank=True, null=True)  # This field type is a guess.
    old_counter = models.IntegerField(blank=True, null=True)
    periode = models.CharField(max_length=1, blank=True, null=True)
    is_digital_sign = models.BooleanField(
        null=True,
    )
    is_wo_sign_mandatory = models.BooleanField(
        null=True,
    )
    competency_is_activated = models.BooleanField(
        null=True,
    )
    id_usertable6 = models.BigIntegerField(blank=True, null=True)
    id_usertable7 = models.BigIntegerField(blank=True, null=True)
    id_usertable8 = models.BigIntegerField(blank=True, null=True)
    wo_forward_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_decontaminated = models.TextField(blank=True, null=True)  # This field type is a guess.
    response_time_calcul_mode = models.BooleanField(
        null=True,
    )
    udi = models.TextField(blank=True, null=True)  # This field type is a guess.
    call_creator = models.TextField(blank=True, null=True)  # This field type is a guess.
    autodispatch_notif_status = models.BooleanField(
        null=True,
    )
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_prev_eqp = models.BigIntegerField(blank=True, null=True)
    date_prev_calculated = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_ge_wonum = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_user_creator = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_prep_id = models.BigIntegerField(blank=True, null=True)
    order_amount = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc_plus_ord_am = models.TextField(blank=True, null=True)  # This field type is a guess.
    init_pm_date_before = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'b_ft1996'


class Docliste(models.Model):
    nu_doc = models.CharField(max_length=1024, blank=True, null=True)  # This field type is a guess.
    nom_doc = models.CharField(max_length=1024, blank=True, null=True)  # This field type is a guess.
    type_doc = models.IntegerField(blank=True, null=True)
    commentair = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    nu_int = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    eqouint = models.IntegerField(blank=True, null=True)
    applicat = models.CharField(max_length=50, blank=True, null=True)
    n_uf = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    n_ef = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_contrat = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    nu_contact = models.CharField(max_length=10, blank=True, null=True)
    code_techn = models.CharField(max_length=64, blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    tp_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_prevent = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    primaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    printable = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_cause = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_remede = models.TextField(blank=True, null=True)  # This field type is a guess.
    keyword = models.TextField(blank=True, null=True)  # This field type is a guess.
    description_doc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    visibility_by_web = models.IntegerField(blank=True, null=True)
    request_id = models.BigIntegerField(blank=True, null=True)
    request_item_id = models.BigIntegerField(blank=True, null=True)
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    numdemm = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_id_training = models.IntegerField(blank=True, null=True)
    is_stored_in_db = models.TextField(blank=True, null=True)  # This field type is a guess.
    dol_content = models.BinaryField(blank=True, null=True)
    marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    dol_id_pk = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'docliste'


class Contrat(models.Model):
    """
    Ce modèle est utilisé pour stocker les contrats (/marchés) de maintenance.
    """

    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    code_type = models.CharField(max_length=10, blank=True, null=True)
    n_presta = models.CharField(max_length=10, blank=True, null=True)
    n_cont_p = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_client = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_cont_c = models.TextField(blank=True, null=True)  # This field type is a guess.
    datedeb = AssetPlusDate3(blank=True, null=True)  # This field type is a guess.
    datefin = AssetPlusDate3(blank=True, null=True)  # This field type is a guess.
    duree = models.TextField(blank=True, null=True)  # This field type is a guess.
    tacite = models.CharField(max_length=1, blank=True, null=True)
    preavis = models.IntegerField(blank=True, null=True)
    date_preav = models.TextField(blank=True, null=True)  # This field type is a guess.
    prestation = models.TextField(blank=True, null=True)  # This field type is a guess.
    exclusion = models.TextField(blank=True, null=True)  # This field type is a guess.
    remise = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    vac_ht = models.CharField(max_length=6, blank=True, null=True)
    fre_mp = models.CharField(max_length=2, blank=True, null=True)
    nb_vcm = models.CharField(max_length=2, blank=True, null=True)
    pd_mp = models.CharField(max_length=1, blank=True, null=True)
    pd_mc = models.CharField(max_length=1, blank=True, null=True)
    pd_seuil = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_ar_bl = models.CharField(max_length=2, blank=True, null=True)
    dmcd_b = models.TextField(blank=True, null=True)  # This field type is a guess.
    dmi = models.TextField(blank=True, null=True)  # This field type is a guess.
    t_mi = models.CharField(max_length=7, blank=True, null=True)
    annee_exo = models.IntegerField(blank=True, null=True)
    coeff = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    title = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    n_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_contract_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    contract_cost_updated_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    quote_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    quote_amount = models.TextField(blank=True, null=True)  # This field type is a guess.
    quote_request_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    quote_reception_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    quote_acceptation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    purchase_order_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    purchase_order_sent_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_rx_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_tx_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_tx_status = models.IntegerField(blank=True, null=True)
    id_usertable1 = models.IntegerField(blank=True, null=True)
    id_usertable2 = models.IntegerField(blank=True, null=True)
    id_usertable3 = models.IntegerField(blank=True, null=True)
    id_usertable4 = models.IntegerField(blank=True, null=True)
    id_usertable5 = models.IntegerField(blank=True, null=True)
    duration_unit = models.IntegerField(blank=True, null=True)
    duration_unit_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    account_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vcq = models.CharField(max_length=2, blank=True, null=True)
    financial_period_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    financial_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    defaut = models.CharField(max_length=1, blank=True, null=True)
    contract_comment = models.TextField(blank=True, null=True)
    contract_status = models.IntegerField(blank=True, null=True)
    pd_mp_int = models.BooleanField(null=True)
    pd_mc_int = models.BooleanField(null=True)
    response_time_calcul_mode = models.BooleanField(null=True)
    is_open_all_days = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_all_times = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_open_day7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_deb_day7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    hour_fin_day7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    taxe_code = models.CharField(max_length=1, blank=True, null=True)
    taxe_rate = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_price_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_cost_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    year_period_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    year_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_fixe_price_cost_used = models.IntegerField(blank=True, null=True)
    auto_id: models.BigIntegerField = models.BigIntegerField(unique=True)
    periodicity_contract_mode = models.IntegerField(blank=True, null=True)
    prorata_contract_mode = models.IntegerField(blank=True, null=True)
    is_contract_mode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contrat'


class HistoEq(models.Model):
    """
    Ce modèle est utilisé pour stocker les lients entre les contrats (/marchés) et les équipements.
    """

    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    code_type = models.CharField(max_length=10, blank=True, null=True)
    n_imma = models.TextField()  # This field type is a guess.
    annee_exo = models.IntegerField(blank=True, null=True)
    date_effet = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_echu = models.TextField(blank=True, null=True)  # This field type is a guess.
    prorata = models.IntegerField(blank=True, null=True)
    ttc_annee = models.TextField(blank=True, null=True)  # This field type is a guess.
    ttc_net = models.TextField(blank=True, null=True)  # This field type is a guess.
    ttc_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    ttc_corr = models.TextField(blank=True, null=True)  # This field type is a guess.
    vac_ht = models.CharField(max_length=6, blank=True, null=True)
    fre_mp = models.CharField(max_length=2, blank=True, null=True)
    nb_vcm = models.CharField(max_length=2, blank=True, null=True)
    pd_mp = models.CharField(max_length=1, blank=True, null=True)
    pd_mc = models.CharField(max_length=1, blank=True, null=True)
    pd_seuil = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_ar_bl = models.CharField(max_length=2, blank=True, null=True)
    dmcd_b = models.TextField(blank=True, null=True)  # This field type is a guess.
    dmi = models.TextField(blank=True, null=True)  # This field type is a guess.
    t_mi = models.CharField(max_length=7, blank=True, null=True)
    defaut = models.CharField(max_length=1, blank=True, null=True)
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    commentaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    generic_seq = models.IntegerField()
    fk_lieu_n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    update_date = AssetPlusDate2(blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    asset_annual_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_net_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vcq = models.CharField(max_length=2, blank=True, null=True)
    financial_period_from = models.TextField()  # This field type is a guess.
    financial_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    inactive_contract_asset_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    contract_asset_status = models.IntegerField(blank=True, null=True)
    pd_mp_int = models.BooleanField(null=True)
    pd_mc_int = models.BooleanField(null=True)
    year_period_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    year_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    taxe_code = models.CharField(max_length=1, blank=True, null=True)
    taxe_rate = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_price_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_price_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_price_net = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_cost_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_cost_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_cost_net = models.TextField(blank=True, null=True)  # This field type is a guess.
    previous_taxe_code = models.CharField(max_length=1, blank=True, null=True)
    previous_taxe_rate = models.TextField(blank=True, null=True)  # This field type is a guess.
    previous_discount_rate = models.TextField(blank=True, null=True)  # This field type is a guess.
    previous_prorata = models.IntegerField(blank=True, null=True)
    current_prorata = models.IntegerField(blank=True, null=True)
    prev_asset_annual_price_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    prev_asset_annual_cost_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_fixe_price_cost_used = models.IntegerField(blank=True, null=True)
    auto_id: models.BigIntegerField = models.BigIntegerField(unique=True)
    is_user_change_cost = models.IntegerField(blank=True, null=True)
    ht_net = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'histo_eq'
        unique_together = (('n_contrat', 'n_imma', 'generic_seq', 'financial_period_from'),)
