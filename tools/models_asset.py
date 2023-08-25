
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from overoly.base import OverolyModel as Model

class Absences(Model):
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    pren_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    abs_deb = models.CharField(max_length=10, blank=True, null=True)
    abs_fin = models.CharField(max_length=10, blank=True, null=True)
    typ_abs = models.CharField(max_length=2, blank=True, null=True)
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    confirma = models.CharField(max_length=1, blank=True, null=True)
    code_four = models.CharField(max_length=10, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    abs_allday = models.TextField(blank=True, null=True)  # This field type is a guess.
    abs_starttime = models.TextField(blank=True, null=True)  # This field type is a guess.
    abs_endtime = models.TextField(blank=True, null=True)  # This field type is a guess.
    abs_id = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_customer_id = models.BigIntegerField(blank=True, null=True)
    auto_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'absences'


class Account(Model):
    nu_compte = models.TextField(primary_key=True)  # This field type is a guess.
    account_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'account'


class Activation(Model):
    when_act = models.TextField(primary_key=True)  # This field type is a guess.
    data_act = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'activation'


class ActivityPole(Model):
    id = models.BigIntegerField(primary_key=True)
    fk_customer_id = models.BigIntegerField(unique=True)
    pole_code = models.TextField(unique=True)  # This field type is a guess.
    pole_name = models.TextField(unique=True)  # This field type is a guess.
    pole_chief = models.TextField(blank=True, null=True)  # This field type is a guess.
    pole_chief_phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'activity_pole'


class Address(Model):
    id = models.BigIntegerField(primary_key=True)
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_customer_id = models.BigIntegerField(blank=True, null=True)
    line1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    line2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    city = models.TextField(unique=True)  # This field type is a guess.
    state = models.TextField(blank=True, null=True)  # This field type is a guess.
    country = models.TextField(blank=True, null=True)  # This field type is a guess.
    pincode = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'address'


class Affecoimp(Model):
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    be2implant = models.TextField(primary_key=True)  # This field type is a guess.
    c_refer = models.TextField()  # This field type is a guess.
    code_four = models.CharField(max_length=10)
    qte = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib5 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affecoimp'
        unique_together = (('be2implant', 'c_refer', 'code_four'),)


class Alert(Model):
    alt_id = models.TextField(primary_key=True)  # This field type is a guess.
    alt_title = models.TextField(blank=True, null=True)  # This field type is a guess.
    alt_request = models.TextField(blank=True, null=True)
    alt_ok_condition = models.NullBooleanField()
    alt_display_condition = models.NullBooleanField()
    alt_ordre = models.IntegerField(blank=True, null=True)
    alt_profile_type = models.CharField(max_length=1, blank=True, null=True)
    alt_profile_value = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'alert'


class AlertRedhandSettings(Model):
    p_profile = models.TextField(primary_key=True)  # This field type is a guess.
    is_what = models.TextField(unique=True)  # This field type is a guess.
    warranty = models.NullBooleanField()
    retired = models.NullBooleanField()
    depreciated = models.NullBooleanField()
    contract_expiration = models.NullBooleanField()
    contract_expiration_n_days = models.IntegerField(blank=True, null=True)
    contract_expiration_unit_days = models.IntegerField(blank=True, null=True)
    contract_expiration_duration = models.IntegerField(blank=True, null=True)
    total_renew_price = models.NullBooleanField()
    total_renew_price_pcent = models.IntegerField(blank=True, null=True)
    total_purchase_price = models.NullBooleanField()
    total_purchase_price_pcent = models.IntegerField(blank=True, null=True)
    pm_on_delay = models.NullBooleanField()
    next_pm_from = models.NullBooleanField()
    next_pm_from_n_days = models.IntegerField(blank=True, null=True)
    next_pm_from_unit_days = models.IntegerField(blank=True, null=True)
    next_pm_from_duration = models.IntegerField(blank=True, null=True)
    wo_defect = models.NullBooleanField()
    wo_defect_n_days = models.IntegerField(blank=True, null=True)
    wo_defect_unit_days = models.IntegerField(blank=True, null=True)
    wo_defect_duration = models.IntegerField(blank=True, null=True)
    wo_duplicated = models.NullBooleanField()
    order_on_delay = models.NullBooleanField()
    order_on_delay_n_days = models.IntegerField(blank=True, null=True)
    order_on_delay_unit_days = models.IntegerField(blank=True, null=True)
    order_on_delay_duration = models.IntegerField(blank=True, null=True)
    wo_maxresponsetime_hour = models.IntegerField(blank=True, null=True)
    next_pm_counter_from = models.NullBooleanField()
    next_pm_counter_from_pcent = models.IntegerField(blank=True, null=True)
    next_pm_counter_from_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alert_redhand_settings'
        unique_together = (('p_profile', 'is_what'),)


class AllPictures(Model):
    id = models.BigIntegerField(primary_key=True)
    picture = models.BinaryField(unique=True)
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'all_pictures'


class AllPicturesTmp(Model):
    id = models.BigIntegerField(blank=True, null=True)
    picture = models.BinaryField(blank=True, null=True)
    description = models.TextField(primary_key=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'all_pictures_tmp'


class Applications(Model):
    nom_appli = models.TextField(primary_key=True)  # This field type is a guess.
    chem_appli = models.TextField(blank=True, null=True)  # This field type is a guess.
    window_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    descrip = models.TextField(blank=True, null=True)  # This field type is a guess.
    parameter = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'applications'


class AptimerLog(Model):
    type = models.CharField(primary_key=True, max_length=1)
    feature = models.TextField(blank=True, null=True)  # This field type is a guess.
    success = models.CharField(max_length=1, blank=True, null=True)
    log_date = models.TextField(unique=True)  # This field type is a guess.
    ip_address = models.TextField(unique=True)  # This field type is a guess.
    host_name = models.TextField(unique=True)  # This field type is a guess.
    nt_user_name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'aptimer_log'


class AssetContractHistoric(Model):
    historic_date = models.TextField(primary_key=True)  # This field type is a guess.
    historic_time = models.TextField(unique=True)  # This field type is a guess.
    user_login = models.TextField(unique=True)  # This field type is a guess.
    n_contrat = models.TextField(unique=True)  # This field type is a guess.
    n_imma = models.TextField(unique=True)  # This field type is a guess.
    financial_period_from = models.TextField(unique=True)  # This field type is a guess.
    what_changes = models.TextField(blank=True, null=True)
    generic_seq = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_contract_historic'


class AssetHistoricCounter(Model):
    n_imma = models.TextField(primary_key=True)  # This field type is a guess.
    counter_value = models.IntegerField(blank=True, null=True)
    historic_user_login = models.TextField(blank=True, null=True)  # This field type is a guess.
    module = models.TextField(blank=True, null=True)  # This field type is a guess.
    feature = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_hour = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'asset_historic_counter'


class AssetSupplierHistoric(Model):
    ash_id = models.IntegerField(primary_key=True)
    ash_date = models.TextField(unique=True)  # This field type is a guess.
    ash_time = models.TextField(unique=True)  # This field type is a guess.
    ash_asset_number = models.TextField(unique=True)  # This field type is a guess.
    ash_supplier_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asset_supplier_historic'


class AssetplusSchemas(Model):
    pk_field = models.TextField(primary_key=True)  # This field type is a guess.
    ap_owner = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_position = models.IntegerField(blank=True, null=True)
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_lng = models.IntegerField(blank=True, null=True)
    field_dec = models.IntegerField(blank=True, null=True)
    field_nullable = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_is_pk = models.IntegerField(blank=True, null=True)
    field_is_index = models.IntegerField(blank=True, null=True)
    fk_group_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_group_value_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_is_identity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assetplus_schemas'


class AssetplusScripts(Model):
    aps_id = models.BigIntegerField(primary_key=True)
    aps_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    aps_heure = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'assetplus_scripts'


class Assetstatus(Model):
    asset_status = models.IntegerField(primary_key=True)
    lib_assetstatus = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'assetstatus'


class BCompA(Model):
    c_refer = models.TextField(primary_key=True)  # This field type is a guess.
    c_design = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(unique=True, max_length=10)
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_prix_uni = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_unite = models.CharField(max_length=10, blank=True, null=True)
    c_tva = models.CharField(max_length=1, blank=True, null=True)
    ind_maint = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_march_ie = models.CharField(max_length=10, blank=True, null=True)
    typ_maint = models.CharField(max_length=1, blank=True, null=True)
    c_stock_mi = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_stock = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_stock_va = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_stock_qm = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_stock_li = models.TextField(unique=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    l_q_cde = models.TextField(blank=True, null=True)  # This field type is a guess.
    l_refer = models.CharField(max_length=9, blank=True, null=True)
    l_refer_da = models.CharField(max_length=10, blank=True, null=True)
    l_refer_es = models.CharField(max_length=1, blank=True, null=True)
    c_stockabc = models.CharField(max_length=1, blank=True, null=True)
    stock1994 = models.TextField(blank=True, null=True)  # This field type is a guess.
    stock1993 = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    stock1995 = models.TextField(blank=True, null=True)  # This field type is a guess.
    piece = models.CharField(max_length=1, blank=True, null=True)
    fdg = models.CharField(max_length=10, blank=True, null=True)
    typ_mod_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    localis = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_reform = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_device_type = models.BigIntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_mpu = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_ref = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    d_update_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'b_comp_a'


class BEq1996(Model):
    n_imma = models.TextField(primary_key=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    ef_typ = models.CharField(max_length=25, blank=True, null=True)
    poste_w = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca = models.TextField(blank=True, null=True)  # This field type is a guess.
    mes1 = models.CharField(max_length=10, blank=True, null=True)
    dpo = models.CharField(max_length=10, blank=True, null=True)
    fdg = models.CharField(max_length=10, blank=True, null=True)
    mhs = models.CharField(max_length=10, blank=True, null=True)
    fdg_constr = models.CharField(max_length=10, blank=True, null=True)
    date_refor = models.CharField(max_length=10, blank=True, null=True)
    ind_maint = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_maint = models.CharField(max_length=10, blank=True, null=True)
    c_ind_main = models.CharField(max_length=10, blank=True, null=True)
    unit_st = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix_fau = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_m_an_bas = models.CharField(max_length=2, blank=True, null=True)
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    m_an_effet = models.CharField(max_length=2, blank=True, null=True)
    p_m_tempor = models.IntegerField(blank=True, null=True)
    p_m_vetust = models.IntegerField(blank=True, null=True)
    p_m_prix_n = models.TextField(blank=True, null=True)  # This field type is a guess.
    h_exploit = models.CharField(max_length=10, blank=True, null=True)
    vac_ht = models.CharField(max_length=6, blank=True, null=True)
    fre_mp = models.CharField(max_length=2, blank=True, null=True)
    pd_mp = models.CharField(max_length=1, blank=True, null=True)
    nb_vcm = models.CharField(max_length=2, blank=True, null=True)
    dmcd_b = models.IntegerField(blank=True, null=True)
    pd_mc = models.CharField(max_length=1, blank=True, null=True)
    pd_seuil = models.IntegerField(blank=True, null=True)
    nb_ar_bl = models.CharField(max_length=2, blank=True, null=True)
    dmi = models.IntegerField(blank=True, null=True)
    t_im = models.CharField(max_length=7, blank=True, null=True)
    crit_ac = models.CharField(max_length=20, blank=True, null=True)
    crit_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    dit_tc = models.CharField(max_length=20, blank=True, null=True)
    dit_disf = models.CharField(max_length=10, blank=True, null=True)
    nbt_ab_tc = models.IntegerField(blank=True, null=True)
    nbt_ab_dis = models.IntegerField(blank=True, null=True)
    nb_vp = models.IntegerField(blank=True, null=True)
    nbh_vp = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vc = models.IntegerField(blank=True, null=True)
    nb_vcu = models.IntegerField(blank=True, null=True)
    nbh_vc = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vat = models.IntegerField(blank=True, null=True)
    nb_vatu = models.IntegerField(blank=True, null=True)
    nbh_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    dm_di = models.IntegerField(blank=True, null=True)
    dm_cd = models.IntegerField(blank=True, null=True)
    mt_co_en = models.IntegerField(blank=True, null=True)
    mt_pd = models.IntegerField(blank=True, null=True)
    mt_mo = models.IntegerField(blank=True, null=True)
    mt_dep = models.IntegerField(blank=True, null=True)
    dit_tci = models.CharField(max_length=20, blank=True, null=True)
    dit_disfi = models.CharField(max_length=10, blank=True, null=True)
    nbt_ab_tci = models.IntegerField(blank=True, null=True)
    nbt_b_disi = models.IntegerField(blank=True, null=True)
    nb_vpi = models.IntegerField(blank=True, null=True)
    nbh_vpi = models.IntegerField(blank=True, null=True)
    nb_vci = models.IntegerField(blank=True, null=True)
    nb_vcui = models.IntegerField(blank=True, null=True)
    nbh_vci = models.IntegerField(blank=True, null=True)
    nb_vati = models.IntegerField(blank=True, null=True)
    nb_vatui = models.IntegerField(blank=True, null=True)
    nbh_vati = models.IntegerField(blank=True, null=True)
    dm_dii = models.IntegerField(blank=True, null=True)
    dm_cdi = models.IntegerField(blank=True, null=True)
    mt_co_eni = models.IntegerField(blank=True, null=True)
    mt_pdi = models.IntegerField(blank=True, null=True)
    mt_moi = models.IntegerField(blank=True, null=True)
    mt_depi = models.IntegerField(blank=True, null=True)
    d_dern_int = models.CharField(max_length=10, blank=True, null=True)
    d_der_i_c = models.CharField(max_length=10, blank=True, null=True)
    d_der_i_p = models.CharField(max_length=10, blank=True, null=True)
    nbh_fonc = models.IntegerField(blank=True, null=True)
    date_syst = models.CharField(max_length=10, blank=True, null=True)
    be1numseco = models.TextField(blank=True, null=True)  # This field type is a guess.
    be2implant = models.TextField(blank=True, null=True)  # This field type is a guess.
    equal_lib1 = models.CharField(max_length=20, blank=True, null=True)
    equal_lib2 = models.CharField(max_length=20, blank=True, null=True)
    equal_lib3 = models.CharField(max_length=20, blank=True, null=True)
    equal_lib4 = models.CharField(max_length=20, blank=True, null=True)
    lib1_min = models.CharField(max_length=10, blank=True, null=True)
    lib1_max = models.CharField(max_length=10, blank=True, null=True)
    lib1_param = models.CharField(max_length=10, blank=True, null=True)
    lib2_min = models.CharField(max_length=10, blank=True, null=True)
    lib2_max = models.CharField(max_length=10, blank=True, null=True)
    lib2_param = models.CharField(max_length=10, blank=True, null=True)
    lib3_min = models.CharField(max_length=10, blank=True, null=True)
    lib3_max = models.CharField(max_length=10, blank=True, null=True)
    lib3_param = models.CharField(max_length=10, blank=True, null=True)
    lib4_min = models.CharField(max_length=10, blank=True, null=True)
    lib4_max = models.CharField(max_length=10, blank=True, null=True)
    lib4_param = models.CharField(max_length=10, blank=True, null=True)
    qual_r_p = models.CharField(max_length=20, blank=True, null=True)
    qual_r_m = models.CharField(max_length=20, blank=True, null=True)
    qual_i_e = models.CharField(max_length=20, blank=True, null=True)
    secu_indus = models.CharField(max_length=50, blank=True, null=True)
    secu_nbvis = models.IntegerField(blank=True, null=True)
    secu_act = models.CharField(max_length=20, blank=True, null=True)
    secu_cpt = models.CharField(max_length=10, blank=True, null=True)
    ex_n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    remp_prix = models.TextField(blank=True, null=True)  # This field type is a guess.
    remp_obs = models.TextField(blank=True, null=True)  # This field type is a guess.
    etiquetage = models.CharField(max_length=1, blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)
    id_usertable3 = models.BigIntegerField(blank=True, null=True)
    id_usertable4 = models.BigIntegerField(blank=True, null=True)
    id_usertable5 = models.BigIntegerField(blank=True, null=True)
    workgroup = models.TextField(blank=True, null=True)  # This field type is a guess.
    ip_address = models.TextField(blank=True, null=True)  # This field type is a guess.
    mat_address = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_plug = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_port = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_it_user = models.BigIntegerField(blank=True, null=True)
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    number_in_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    eq_amt_com = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_eqp = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_produit_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_client_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    from_module = models.TextField(blank=True, null=True)  # This field type is a guess.
    d_pro_i_p = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_request_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_request_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_recept_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_request_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    n_imma_replace = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler_eco_1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler_eco_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler_eco_3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_eco_1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_eco_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_eco_3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    tagid = models.TextField(blank=True, null=True)  # This field type is a guess.
    zoneid = models.TextField(blank=True, null=True)  # This field type is a guess.
    zonegroupid = models.TextField(blank=True, null=True)  # This field type is a guess.
    zoneowning_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    dwell_time = models.BigIntegerField(blank=True, null=True)
    x_ft = models.IntegerField(blank=True, null=True)
    y_ft = models.IntegerField(blank=True, null=True)
    is_tester = models.IntegerField(blank=True, null=True)
    el_fix_generic_quantity = models.IntegerField(blank=True, null=True)
    asset_status = models.IntegerField(blank=True, null=True)
    asset_sub_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    mac_address = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_rfid_tag = models.NullBooleanField()
    nb_vcq = models.CharField(max_length=2, blank=True, null=True)
    interface = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd_mp_int = models.NullBooleanField()
    pd_mc_int = models.NullBooleanField()
    id_usertable6 = models.BigIntegerField(blank=True, null=True)
    id_usertable7 = models.BigIntegerField(blank=True, null=True)
    id_usertable8 = models.BigIntegerField(blank=True, null=True)
    fk_all_pictures_id = models.BigIntegerField(blank=True, null=True)
    udi = models.TextField(blank=True, null=True)  # This field type is a guess.
    eqp_secondary_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)
    fabriquant = models.TextField(blank=True, null=True)  # This field type is a guess.
    centrale_achat = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_asset_status = models.IntegerField(blank=True, null=True)
    lib_assetstatus = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_dgos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'b_eq1996'


class BFt1996(Model):
    nu_int = models.TextField(primary_key=True)  # This field type is a guess.
    nu_bon_c = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_imm = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_ap = models.CharField(max_length=10, blank=True, null=True)
    he_ap = models.CharField(max_length=8, blank=True, null=True)
    da_int = models.CharField(max_length=10, blank=True, null=True)
    he_int = models.CharField(max_length=8, blank=True, null=True)
    da_hs = models.CharField(max_length=10, blank=True, null=True)
    he_hs = models.CharField(max_length=8, blank=True, null=True)
    da_dis = models.CharField(max_length=10, blank=True, null=True)
    he_dis = models.CharField(max_length=8, blank=True, null=True)
    da_fin = models.CharField(max_length=10, blank=True, null=True)
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
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    date_syst = models.CharField(max_length=10, blank=True, null=True)
    da_rec = models.CharField(max_length=10, blank=True, null=True)
    he_rec = models.CharField(max_length=8, blank=True, null=True)
    delai = models.IntegerField(blank=True, null=True)
    code_delai = models.CharField(max_length=1, blank=True, null=True)
    da_hdelai = models.CharField(max_length=10, blank=True, null=True)
    n_devis = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_facture = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_engag = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_recp = models.CharField(max_length=10, blank=True, null=True)
    div_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_cadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_statut = models.TextField(blank=True, null=True)  # This field type is a guess.
    par1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_contact_person_id = models.BigIntegerField(blank=True, null=True)
    fk_address_id = models.BigIntegerField(blank=True, null=True)
    date_of_nu_bon_c = models.CharField(max_length=10, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    is_digital_sign = models.NullBooleanField()
    is_wo_sign_mandatory = models.NullBooleanField()
    competency_is_activated = models.NullBooleanField()
    id_usertable6 = models.BigIntegerField(blank=True, null=True)
    id_usertable7 = models.BigIntegerField(blank=True, null=True)
    id_usertable8 = models.BigIntegerField(blank=True, null=True)
    wo_forward_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_decontaminated = models.TextField(blank=True, null=True)  # This field type is a guess.
    response_time_calcul_mode = models.NullBooleanField()
    udi = models.TextField(blank=True, null=True)  # This field type is a guess.
    call_creator = models.TextField(blank=True, null=True)  # This field type is a guess.
    autodispatch_notif_status = models.NullBooleanField()
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


class BSf1996(Model):
    n_ufef = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_compl = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_servi = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_cent_res = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_centre = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specc = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl = models.CharField(max_length=10, blank=True, null=True)
    f_specl2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    mes1 = models.CharField(max_length=10, blank=True, null=True)
    dpo = models.CharField(max_length=10, blank=True, null=True)
    prix_glob = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_ind_main = models.CharField(max_length=10, blank=True, null=True)
    ind_maint = models.TextField(blank=True, null=True)  # This field type is a guess.
    unit_st = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix_fau = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_m_an_bas = models.CharField(max_length=2, blank=True, null=True)
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_m_tempor = models.IntegerField(blank=True, null=True)
    p_m_vetust = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_m_prix_n = models.TextField(blank=True, null=True)  # This field type is a guess.
    m_an_effet = models.CharField(max_length=2, blank=True, null=True)
    h_exploit = models.CharField(max_length=10, blank=True, null=True)
    e_equip = models.IntegerField(blank=True, null=True)
    crit_ac = models.CharField(max_length=20, blank=True, null=True)
    crit_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_cons = models.CharField(max_length=20, blank=True, null=True)
    crit_const = models.IntegerField(blank=True, null=True)
    dit_tc = models.CharField(max_length=7, blank=True, null=True)
    dit_disf = models.CharField(max_length=7, blank=True, null=True)
    nbt_ab_tc = models.IntegerField(blank=True, null=True)
    nbt_ab_dis = models.IntegerField(blank=True, null=True)
    dit_tci = models.CharField(max_length=7, blank=True, null=True)
    dit_disfi = models.CharField(max_length=7, blank=True, null=True)
    nbt_ab_tci = models.IntegerField(blank=True, null=True)
    nbt_b_disi = models.IntegerField(blank=True, null=True)
    d_d_d_bl = models.CharField(max_length=10, blank=True, null=True)
    nbh_fonc = models.IntegerField(blank=True, null=True)
    mt_co_eni = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_co_en = models.TextField(blank=True, null=True)  # This field type is a guess.
    ef_typ = models.CharField(max_length=25, blank=True, null=True)
    ef_salle = models.CharField(max_length=25, blank=True, null=True)
    ef_etage = models.CharField(max_length=3, blank=True, null=True)
    ef_superf = models.CharField(max_length=8, blank=True, null=True)
    ef_vol = models.CharField(max_length=8, blank=True, null=True)
    ef_elec = models.CharField(max_length=20, blank=True, null=True)
    ef_menuis = models.CharField(max_length=20, blank=True, null=True)
    ef_plb = models.CharField(max_length=20, blank=True, null=True)
    ef_chauf = models.CharField(max_length=20, blank=True, null=True)
    ef_clim = models.CharField(max_length=20, blank=True, null=True)
    ef_etat = models.CharField(max_length=15, blank=True, null=True)
    ef_action = models.CharField(max_length=15, blank=True, null=True)
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fg_status = models.IntegerField(blank=True, null=True)
    fg_sub_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    udi = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'b_sf1996'


class BarcodeDetailSettings(Model):
    fk_id_header_label = models.IntegerField(primary_key=True)
    order_id_field = models.IntegerField(unique=True)
    name_table_view = models.TextField(blank=True, null=True)  # This field type is a guess.
    category_field = models.BooleanField(unique=True)
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_lng = models.IntegerField(blank=True, null=True)
    is_linked = models.NullBooleanField()
    is_prefixe = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_contain = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_suffixe = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_width = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_height = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_alignment = models.NullBooleanField()
    is_font = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_size = models.IntegerField(blank=True, null=True)
    is_color = models.IntegerField(blank=True, null=True)
    is_bold = models.NullBooleanField()
    is_italic = models.NullBooleanField()
    is_underline = models.NullBooleanField()
    is_strikethrough = models.NullBooleanField()
    is_barcode_type_id = models.IntegerField(blank=True, null=True)
    is_border = models.NullBooleanField()
    is_user_dimension = models.NullBooleanField()
    is_picture = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'barcode_detail_settings'
        unique_together = (('fk_id_header_label', 'order_id_field'),)


class BarcodeHeaderSettings(Model):
    id_barcode_header = models.IntegerField(primary_key=True)
    description_header = models.TextField(unique=True)  # This field type is a guess.
    category_label = models.IntegerField(unique=True)
    name_table_view = models.TextField(unique=True)  # This field type is a guess.
    width = models.TextField(blank=True, null=True)  # This field type is a guess.
    height = models.TextField(blank=True, null=True)  # This field type is a guess.
    upper_edge = models.IntegerField(blank=True, null=True)
    inter_label_h = models.IntegerField(blank=True, null=True)
    left_edge = models.IntegerField(blank=True, null=True)
    inter_label_v = models.IntegerField(blank=True, null=True)
    nbr_horizontal_label = models.IntegerField(blank=True, null=True)
    nbr_vertical_label = models.IntegerField(blank=True, null=True)
    margin_inside_left = models.IntegerField(blank=True, null=True)
    margin_inside_right = models.IntegerField(blank=True, null=True)
    margin_inside_up = models.IntegerField(blank=True, null=True)
    margin_inside_down = models.IntegerField(blank=True, null=True)
    border_label = models.NullBooleanField()
    date_format = models.IntegerField(blank=True, null=True)
    number_format = models.IntegerField(blank=True, null=True)
    fk_profile = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_vocation = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_site_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    display_translated_fields = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'barcode_header_settings'


class Batim(Model):
    n_bati = models.CharField(primary_key=True, max_length=10)
    n_etab = models.CharField(max_length=10, blank=True, null=True)
    bat_nom = models.CharField(max_length=25, blank=True, null=True)
    bat_nom2 = models.CharField(max_length=25, blank=True, null=True)
    bat_situ = models.CharField(max_length=25, blank=True, null=True)
    bat_birth = models.CharField(max_length=10, blank=True, null=True)
    bat_etat = models.CharField(max_length=20, blank=True, null=True)
    bat_stru = models.CharField(max_length=20, blank=True, null=True)
    bat_spec = models.CharField(max_length=35, blank=True, null=True)
    bat_resp = models.CharField(max_length=20, blank=True, null=True)
    bat_obs = models.CharField(max_length=80, blank=True, null=True)
    bat_maj = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batim'


class BoDictionary(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    field_name = models.TextField(unique=True)  # This field type is a guess.
    field_value = models.IntegerField(unique=True)
    bo_label = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'bo_dictionary'


class Bonpre(Model):
    nummag = models.TextField(blank=True, null=True)  # This field type is a guess.
    nommag = models.TextField(blank=True, null=True)  # This field type is a guess.
    numbp = models.TextField(primary_key=True)  # This field type is a guess.
    numcomm = models.TextField(blank=True, null=True)  # This field type is a guess.
    commentbp = models.TextField(blank=True, null=True)  # This field type is a guess.
    reqsql_con = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_bp = models.TextField(blank=True, null=True)  # This field type is a guess.
    nummagf = models.TextField(blank=True, null=True)  # This field type is a guess.
    nommagf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uff = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bonpre'


class BonpreDetails(Model):
    no_bonpre_detail = models.IntegerField(blank=True, null=True)
    no_bonpre = models.TextField(primary_key=True)  # This field type is a guess.
    code_supp_store = models.TextField()  # This field type is a guess.
    c_refer = models.TextField()  # This field type is a guess.
    code_dest_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    model = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity_requested = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity_stock = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_without_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_include_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_public_market = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_internal = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10)
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'bonpre_details'
        unique_together = (('no_bonpre', 'code_supp_store', 'c_refer', 'code_four'),)


class Budget(Model):
    nu_compte = models.TextField(primary_key=True)  # This field type is a guess.
    lib_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_cumul = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_an = models.IntegerField(blank=True, null=True)
    an_exo = models.CharField(max_length=4)
    mt_annuel = models.TextField(blank=True, null=True)  # This field type is a guess.
    obs_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    financial_period_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    financial_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_expenses_calculated = models.NullBooleanField()
    total_expenses_input = models.TextField(blank=True, null=True)  # This field type is a guess.
    latest_expenses_input_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    latest_expenses_input_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'budget'
        unique_together = (('nu_compte', 'an_exo'),)


class Catpiece(Model):
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'catpiece'


class Causes(Model):
    num = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    woestimatedduration = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_type_option = models.NullBooleanField()
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'causes'


class Chantiers(Model):
    nom_chant = models.CharField(primary_key=True, max_length=50)
    commentair = models.CharField(max_length=255, blank=True, null=True)
    retired_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    retired_type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'chantiers'


class ChecklistResDetails(Model):
    crd_id = models.BigIntegerField(primary_key=True)
    crd_idcrh = models.BigIntegerField(unique=True)
    crd_idctd = models.BigIntegerField(unique=True)
    crd_valeur = models.TextField(blank=True, null=True)  # This field type is a guess.
    crd_optionnum = models.BigIntegerField(blank=True, null=True)
    crd_optionlib = models.TextField(blank=True, null=True)  # This field type is a guess.
    crd_commentsuser = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'checklist_res_details'


class ChecklistResHeader(Model):
    crh_id = models.BigIntegerField(primary_key=True)
    crh_idctv = models.BigIntegerField(unique=True)
    crh_nu_int = models.TextField(unique=True)  # This field type is a guess.
    crh_file = models.TextField(blank=True, null=True)
    crh_result = models.TextField(blank=True, null=True)  # This field type is a guess.
    crh_commentsuser = models.TextField(blank=True, null=True)  # This field type is a guess.
    crh_completed = models.BooleanField(unique=True)
    crh_creationdate = models.TextField(unique=True)  # This field type is a guess.
    crh_creationheure = models.TextField(unique=True)  # This field type is a guess.
    crh_updatedate = models.TextField(blank=True, null=True)  # This field type is a guess.
    crh_updateheure = models.TextField(blank=True, null=True)  # This field type is a guess.
    crh_resultprgext = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'checklist_res_header'


class ChecklistTplDetails(Model):
    ctd_id = models.BigIntegerField(primary_key=True)
    ctd_idctv = models.BigIntegerField(blank=True, null=True)
    ctd_numordre = models.BigIntegerField(blank=True, null=True)
    ctd_idctdparent = models.BigIntegerField(blank=True, null=True)
    ctd_idinternal = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_idsubinternal = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_item = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_gras = models.NullBooleanField()
    ctd_italique = models.NullBooleanField()
    ctd_souligne = models.NullBooleanField()
    ctd_champsaisie = models.NullBooleanField()
    ctd_valeurtype = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_valeurmini = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_valeurmaxi = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_valeurunite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_options = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_comments = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_commentsuser = models.NullBooleanField()
    ctd_all_pictures_id = models.BigIntegerField(blank=True, null=True)
    ctd_optionstype = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctd_valeurminiyn = models.BooleanField(unique=True)
    ctd_valeurmaxiyn = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'checklist_tpl_details'


class ChecklistTplHeader(Model):
    cth_id = models.BigIntegerField(primary_key=True)
    cth_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    cth_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    cth_idctt = models.BigIntegerField(blank=True, null=True)
    cth_reforme = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'checklist_tpl_header'


class ChecklistTplType(Model):
    ctt_id = models.BigIntegerField(primary_key=True)
    ctt_manufacturer = models.TextField(unique=True)  # This field type is a guess.
    ctt_software = models.TextField(unique=True)  # This field type is a guess.
    ctt_filetype = models.TextField(unique=True)  # This field type is a guess.
    ctt_mode = models.TextField(unique=True)  # This field type is a guess.
    ctt_process = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'checklist_tpl_type'


class ChecklistTplVersion(Model):
    ctv_id = models.BigIntegerField(primary_key=True)
    ctv_idcth = models.BigIntegerField(unique=True)
    ctv_date = models.TextField(unique=True)  # This field type is a guess.
    ctv_heure = models.TextField(unique=True)  # This field type is a guess.
    ctv_version = models.BigIntegerField(unique=True)
    ctv_mode = models.TextField(unique=True)  # This field type is a guess.
    ctv_file = models.TextField(blank=True, null=True)
    ctv_active = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'checklist_tpl_version'


class ChkContentType(Model):
    id = models.BigIntegerField(primary_key=True)
    format = models.TextField(blank=True, null=True)  # This field type is a guess.
    manufacturer = models.TextField(unique=True)  # This field type is a guess.
    software = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'chk_content_type'


class ChkResults(Model):
    id = models.BigIntegerField(primary_key=True)
    fk_chk_tpl_id = models.BigIntegerField(unique=True)
    fk_nu_int = models.TextField(unique=True)  # This field type is a guess.
    content = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)  # This field type is a guess.
    observation = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_chk_results_id = models.BigIntegerField(blank=True, null=True)
    completed = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_update_time = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'chk_results'


class ChkTpl(Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.TextField(unique=True)  # This field type is a guess.
    version = models.BigIntegerField(unique=True)
    title = models.TextField(blank=True, null=True)  # This field type is a guess.
    content = models.TextField(blank=True, null=True)
    fk_chk_content_type_id = models.BigIntegerField(blank=True, null=True)
    fk_customer_id = models.BigIntegerField(blank=True, null=True)
    sti_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    retired = models.TextField(blank=True, null=True)  # This field type is a guess.
    active = models.CharField(max_length=1, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'chk_tpl'


class Classe(Model):
    classecode = models.TextField(primary_key=True)  # This field type is a guess.
    classelabel = models.TextField(unique=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'classe'


class Codehora(Model):
    h_exploit = models.CharField(primary_key=True, max_length=10)
    nbh_fonc = models.IntegerField(blank=True, null=True)
    s_jdeb = models.CharField(max_length=8, blank=True, null=True)
    s_pdeb = models.CharField(max_length=8, blank=True, null=True)
    s_pfin = models.CharField(max_length=8, blank=True, null=True)
    s_jfin = models.CharField(max_length=8, blank=True, null=True)
    w_jdeb = models.CharField(max_length=8, blank=True, null=True)
    w_pdeb = models.CharField(max_length=8, blank=True, null=True)
    w_pfin = models.CharField(max_length=8, blank=True, null=True)
    w_jfin = models.CharField(max_length=8, blank=True, null=True)
    d_jdeb = models.CharField(max_length=8, blank=True, null=True)
    d_pdeb = models.CharField(max_length=8, blank=True, null=True)
    d_pfin = models.CharField(max_length=8, blank=True, null=True)
    d_jfin = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codehora'


class Codelai(Model):
    typedelai = models.CharField(primary_key=True, max_length=1)
    codedelai = models.TextField(unique=True)  # This field type is a guess.
    libdelai = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'codelai'
        unique_together = (('typedelai', 'codedelai'),)


class CommandStatus(Model):
    code_status = models.TextField(primary_key=True)  # This field type is a guess.
    label_status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'command_status'


class Commande(Model):
    numcomm = models.TextField(blank=True, null=True)  # This field type is a guess.
    datecomm = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magor = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magdest = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    numdemm = models.TextField(primary_key=True)  # This field type is a guess.
    datedemm = models.TextField(blank=True, null=True)  # This field type is a guess.
    uf_magor = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fon_or = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_cpte = models.TextField(blank=True, null=True)  # This field type is a guess.
    nbligcomm = models.IntegerField(blank=True, null=True)
    etatcomm = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_comm = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_uf_dem = models.TextField(blank=True, null=True)  # This field type is a guess.
    no_uf_dem = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    metier_tech = models.TextField(blank=True, null=True)  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.
    interloc = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    budget_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    tva1 = models.CharField(max_length=1, blank=True, null=True)
    tva2 = models.CharField(max_length=1, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    numbp = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_estimated_delivery = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    sent_order_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    expected_delivery_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_buyer_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.IntegerField(blank=True, null=True)
    id_usertable2 = models.IntegerField(blank=True, null=True)
    id_usertable3 = models.IntegerField(blank=True, null=True)
    id_usertable4 = models.IntegerField(blank=True, null=True)
    id_usertable5 = models.IntegerField(blank=True, null=True)
    finance_po_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler8 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler9 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable6 = models.IntegerField(blank=True, null=True)
    id_usertable7 = models.IntegerField(blank=True, null=True)
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    service_comment = models.TextField(blank=True, null=True)
    n_devis = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_devis = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_facture = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_facture = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_part_service = models.IntegerField(blank=True, null=True)
    date_devis_accepte = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_contact = models.CharField(max_length=10, blank=True, null=True)
    is_use_contact = models.IntegerField(blank=True, null=True)
    remise = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_dgos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'commande'


class Commlign(Model):
    numcomm = models.TextField(primary_key=True)  # This field type is a guess.
    numligne = models.IntegerField()
    datecomm = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_comm = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(unique=True)  # This field type is a guess.
    c_design = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(unique=True, max_length=10)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magfour = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magdem = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_fourni = models.CharField(max_length=10, blank=True, null=True)
    c_unite = models.CharField(max_length=10, blank=True, null=True)
    c_prix_uni = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_tva = models.CharField(max_length=1, blank=True, null=True)
    qte_comm = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    etat_lig = models.CharField(max_length=1, blank=True, null=True)
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_recep = models.TextField(blank=True, null=True)  # This field type is a guess.
    qte_recep = models.TextField(blank=True, null=True)  # This field type is a guess.
    qte_reste = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_cpte = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_uf_dem = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    t_tva = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_mpu = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_ref = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    remise = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_prix_uni_ref = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'commlign'
        unique_together = (('numcomm', 'numligne'),)


class ConnectionLogin(Model):
    profile_name = models.TextField(primary_key=True)  # This field type is a guess.
    id_login = models.TextField(unique=True)  # This field type is a guess.
    pw_login = models.TextField(unique=True)  # This field type is a guess.
    dbase_name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'connection_login'


class Constant(Model):
    n_marche = models.CharField(primary_key=True, max_length=20)
    m_an_effet = models.CharField(max_length=2, blank=True, null=True)
    m_k1 = models.IntegerField(blank=True, null=True)
    m_k2 = models.IntegerField(blank=True, null=True)
    m_k3 = models.IntegerField(blank=True, null=True)
    m_k4 = models.IntegerField(blank=True, null=True)
    m_k5 = models.IntegerField(blank=True, null=True)
    somme = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constant'


class Contact(Model):
    nu_contact = models.CharField(primary_key=True, max_length=10)
    nu_four = models.CharField(max_length=10, blank=True, null=True)
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
    description = models.IntegerField(blank=True, null=True)
    ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    state = models.TextField(blank=True, null=True)  # This field type is a guess.
    contact_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact'


class ContactDescription(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact_description'


class ContactPerson(Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fax = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_address_id = models.BigIntegerField(blank=True, null=True)
    fk_territory_id = models.BigIntegerField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact_person'


class ContractCoverageDetail(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    n_contrat = models.TextField(unique=True)  # This field type is a guess.
    is_corr_pm = models.TextField(unique=True)  # This field type is a guess.
    is_option_coverage = models.TextField(unique=True)  # This field type is a guess.
    c_refer = models.TextField(unique=True)  # This field type is a guess.
    code_four = models.CharField(unique=True, max_length=10)
    inactivation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contract_coverage_detail'


class ContractCoverageHeader(Model):
    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    is_option_corr = models.TextField(blank=True, null=True)  # This field type is a guess.
    comment_corr = models.TextField(blank=True, null=True)
    is_option_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    comment_pm = models.TextField(blank=True, null=True)
    changes_tracking = models.TextField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contract_coverage_header'


class ContractInvoice(Model):
    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    invoice_id = models.TextField()  # This field type is a guess.
    invoice_periodicity = models.IntegerField(blank=True, null=True)
    total = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_rx_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_tx_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    invoice_tx_status = models.IntegerField(blank=True, null=True)
    n_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contract_invoice'
        unique_together = (('n_contrat', 'invoice_id'),)


class ContractPurchaseOrder(Model):
    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    n_order = models.TextField(unique=True)  # This field type is a guess.
    total = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_order = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contract_purchase_order'
        unique_together = (('n_contrat', 'n_order'),)


class ContractServicesHistoric(Model):
    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    annee_exo = models.IntegerField()
    date_effet = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_echu = models.TextField(blank=True, null=True)  # This field type is a guess.
    coeff = models.TextField(blank=True, null=True)  # This field type is a guess.
    remise = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    prix2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    defaut = models.CharField(max_length=1, blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    nb_vcq = models.CharField(max_length=2, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contract_services_historic'
        unique_together = (('n_contrat', 'annee_exo'),)


class Contrat(Model):
    n_contrat = models.TextField(primary_key=True)  # This field type is a guess.
    code_type = models.CharField(max_length=10, blank=True, null=True)
    n_presta = models.CharField(max_length=10, blank=True, null=True)
    n_cont_p = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_client = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_cont_c = models.TextField(blank=True, null=True)  # This field type is a guess.
    datedeb = models.TextField(blank=True, null=True)  # This field type is a guess.
    datefin = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    pd_mp_int = models.NullBooleanField()
    pd_mc_int = models.NullBooleanField()
    response_time_calcul_mode = models.NullBooleanField()
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
    auto_id = models.BigIntegerField(unique=True)
    periodicity_contract_mode = models.IntegerField(blank=True, null=True)
    prorata_contract_mode = models.IntegerField(blank=True, null=True)
    is_contract_mode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contrat'


class ContratBkp108(Model):
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_type = models.CharField(max_length=10, blank=True, null=True)
    n_presta = models.CharField(max_length=10, blank=True, null=True)
    n_cont_p = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_client = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_cont_c = models.TextField(blank=True, null=True)  # This field type is a guess.
    datedeb = models.TextField(blank=True, null=True)  # This field type is a guess.
    datefin = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    pd_mp_int = models.NullBooleanField()
    pd_mc_int = models.NullBooleanField()
    response_time_calcul_mode = models.NullBooleanField()
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
    auto_id = models.BigIntegerField(primary_key=True)
    periodicity_contract_mode = models.IntegerField(blank=True, null=True)
    prorata_contract_mode = models.IntegerField(blank=True, null=True)
    is_contract_mode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contrat_bkp_108'


class Controls(Model):
    typ_mod = models.TextField(primary_key=True)  # This field type is a guess.
    ctrl1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl1unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl1min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl1max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl2unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl2min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl2max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl3unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl3min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl3max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl4unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl4min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl4max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl5unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl5min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl5max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl6unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl6min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl6max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl7unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl7min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl7max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl8 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl8unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl8min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl8max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl9 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl9unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl9min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl9max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl10unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl10min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl10max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl11 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl11unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl11min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl11max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl12 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl12unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl12min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl12max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl13 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl13unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl13min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl13max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl14 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl14unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl14min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl14max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl15 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl15unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl15min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl15max = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_syst = models.CharField(max_length=10, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl16 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl16unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl16min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl16max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl17 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl17unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl17min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl17max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl18 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl18unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl18min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl18max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl19 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl19unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl19min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl19max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl20 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl20unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl20min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl20max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl21 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl21unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl21min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl21max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl22 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl22unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl22min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl22max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl23 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl23unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl23min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl23max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl24 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl24unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl24min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl24max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl25 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl25unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl25min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl25max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl26 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl26unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl26min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl26max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl27 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl27unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl27min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl27max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl28 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl28unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl28min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl28max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl29 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl29unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl29min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl29max = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl30 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl30unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl30min = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl30max = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_deprecated = models.IntegerField(blank=True, null=True)
    ctrl_release_number = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'controls'
        unique_together = (('typ_mod', 'ctrl_release_number'),)


class Cr(Model):
    n_cent_res = models.TextField(primary_key=True)  # This field type is a guess.
    nom_centre = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_etab = models.TextField(unique=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cr'


class Criticite(Model):
    riskcode = models.TextField(primary_key=True)  # This field type is a guess.
    risklabel = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    riskvalue = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'criticite'


class Customer(Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(unique=True)  # This field type is a guess.
    fk_territory_id = models.BigIntegerField(blank=True, null=True)
    fk_address_id = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_license_service_area_id = models.BigIntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'customer'


class DashboardCached(Model):
    cache_key = models.TextField(primary_key=True)  # This field type is a guess.
    time_stamp = models.TextField(blank=True, null=True)  # This field type is a guess.
    xml = models.TextField(blank=True, null=True)
    image_file_name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'dashboard_cached'


class DashboardImages(Model):
    file_name = models.TextField(primary_key=True)  # This field type is a guess.
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dashboard_images'


class Dashboards(Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'dashboards'


class DeletedRecords(Model):
    delete_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    pk_fields = models.TextField(blank=True, null=True)  # This field type is a guess.
    pk_values = models.TextField(blank=True, null=True)  # This field type is a guess.
    action_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    who = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deleted_records'


class DeviceType(Model):
    id_device_type = models.BigIntegerField(primary_key=True)
    code_label = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'device_type'
        unique_together = (('id_device_type', 'code_label'),)


class Dgos(Model):
    n_dgos = models.TextField(primary_key=True)  # This field type is a guess.
    buying_family_n_0 = models.TextField(unique=True)  # This field type is a guess.
    purchase_area_n_1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    purchase_category_n_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    buying_segment_n_3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    sub_segment_n_4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    basic_product_n_5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    geographical_scope = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_code_mpu = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_nu_account = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'dgos'


class DicoItLabel(Model):
    code_label = models.TextField(primary_key=True)  # This field type is a guess.
    code_langue = models.TextField(unique=True)  # This field type is a guess.
    label = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'dico_it_label'
        unique_together = (('code_label', 'code_langue'),)


class Diffus(Model):
    ref_int = models.TextField(primary_key=True)  # This field type is a guess.
    n_uf_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    technicien = models.TextField(blank=True, null=True)  # This field type is a guess.
    action_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    result_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_valid = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod_di = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque_dif = models.TextField(blank=True, null=True)  # This field type is a guess.
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'diffus'


class Docliste(Model):
    nu_doc = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_doc = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_doc = models.IntegerField(blank=True, null=True)
    commentair = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    eqouint = models.IntegerField(blank=True, null=True)
    applicat = models.CharField(max_length=50, blank=True, null=True)
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    nu_contact = models.CharField(max_length=10, blank=True, null=True)
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
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


class DoclisteOld(Model):
    nu_doc = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_doc = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_doc = models.IntegerField(blank=True, null=True)
    commentair = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    eqouint = models.IntegerField(blank=True, null=True)
    applicat = models.CharField(max_length=50, blank=True, null=True)
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    nu_contact = models.CharField(max_length=10, blank=True, null=True)
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    visibility_by_web = models.IntegerField(blank=True, null=True)
    request_id = models.BigIntegerField(blank=True, null=True)
    request_item_id = models.BigIntegerField(blank=True, null=True)
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    numdemm = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_id_training = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docliste_old'


class DocsAppli(Model):
    app_id = models.TextField(primary_key=True)  # This field type is a guess.
    app_label = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'docs_appli'


class Doctype(Model):
    nom_doc = models.TextField(primary_key=True)  # This field type is a guess.
    eqouint = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctype'


class Droits(Model):
    u_password = models.TextField(primary_key=True)  # This field type is a guess.
    eqmt = models.CharField(max_length=1, blank=True, null=True)
    intv = models.CharField(max_length=1, blank=True, null=True)
    contr = models.CharField(max_length=1, blank=True, null=True)
    prev = models.CharField(max_length=1, blank=True, null=True)
    edit = models.CharField(max_length=1, blank=True, null=True)
    stock = models.CharField(max_length=1, blank=True, null=True)
    tabl = models.CharField(max_length=1, blank=True, null=True)
    cneh = models.CharField(max_length=1, blank=True, null=True)
    etab = models.CharField(max_length=1, blank=True, null=True)
    bat = models.CharField(max_length=1, blank=True, null=True)
    ufl = models.CharField(max_length=1, blank=True, null=True)
    efl = models.CharField(max_length=1, blank=True, null=True)
    equip = models.CharField(max_length=1, blank=True, null=True)
    impor = models.CharField(max_length=1, blank=True, null=True)
    feur = models.CharField(max_length=1, blank=True, null=True)
    calend = models.CharField(max_length=1, blank=True, null=True)
    sim = models.CharField(max_length=1, blank=True, null=True)
    inv = models.CharField(max_length=1, blank=True, null=True)
    conf = models.CharField(max_length=1, blank=True, null=True)
    utilis = models.CharField(max_length=1, blank=True, null=True)
    neweq = models.CharField(max_length=1, blank=True, null=True)
    newuf = models.CharField(max_length=1, blank=True, null=True)
    newef = models.CharField(max_length=1, blank=True, null=True)
    newpiece = models.CharField(max_length=1, blank=True, null=True)
    newfour = models.CharField(max_length=1, blank=True, null=True)
    newcneh = models.CharField(max_length=1, blank=True, null=True)
    newremed = models.CharField(max_length=1, blank=True, null=True)
    newcaus = models.CharField(max_length=1, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    ppc_quick_wo_status = models.IntegerField(blank=True, null=True)
    ppc_quick_wo_scan = models.IntegerField(blank=True, null=True)
    donotallowchange_org = models.IntegerField(blank=True, null=True)
    donotallowchange_site = models.IntegerField(blank=True, null=True)
    donotallowchange_md = models.IntegerField(blank=True, null=True)
    donotallowchange_td = models.IntegerField(blank=True, null=True)
    donotallowchange_fc = models.IntegerField(blank=True, null=True)
    donotallowchange_contract = models.IntegerField(blank=True, null=True)
    donotallowchange_pole = models.IntegerField(blank=True, null=True)
    loan_request_creation = models.CharField(max_length=1, blank=True, null=True)
    loan_request_check_out = models.CharField(max_length=1, blank=True, null=True)
    loan_request_check_in = models.CharField(max_length=1, blank=True, null=True)
    loan_request_monitoring = models.CharField(max_length=1, blank=True, null=True)
    server_file_path = models.TextField(blank=True, null=True)  # This field type is a guess.
    server_file_option = models.IntegerField(blank=True, null=True)
    document_management = models.CharField(max_length=1, blank=True, null=True)
    contract_finance_right = models.CharField(max_length=1, blank=True, null=True)
    part_finance_right = models.CharField(max_length=1, blank=True, null=True)
    po_finance_right = models.CharField(max_length=1, blank=True, null=True)
    wo_finance_right = models.CharField(max_length=1, blank=True, null=True)
    supplier_finance_right = models.CharField(max_length=1, blank=True, null=True)
    simplified = models.IntegerField(blank=True, null=True)
    operating_right = models.IntegerField(blank=True, null=True)
    finance_right = models.IntegerField(blank=True, null=True)
    hr_right = models.IntegerField(blank=True, null=True)
    nomenclature_right = models.IntegerField(blank=True, null=True)
    administrative_right = models.IntegerField(blank=True, null=True)
    service_order_right = models.IntegerField(blank=True, null=True)
    activate_db_menu = models.NullBooleanField()
    activate_db_time_refresh = models.NullBooleanField()
    db_time_refresh = models.IntegerField(blank=True, null=True)
    wo_archive_right = models.IntegerField(blank=True, null=True)
    override_sign_right = models.IntegerField(blank=True, null=True)
    cm_activation_competency = models.NullBooleanField()
    cm_competency_issue = models.NullBooleanField()
    cm_reply_issue = models.NullBooleanField()
    cm_max_time = models.IntegerField(blank=True, null=True)
    right_for_delete_document = models.NullBooleanField()
    ppc_quick_wo_allow = models.NullBooleanField()
    prefix_other_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_wo_forward_by_td = models.NullBooleanField()
    pi_scan_mandatory = models.NullBooleanField()
    tm_activation_competency = models.NullBooleanField()
    is_pw_limited = models.NullBooleanField()
    pw_valid_period = models.IntegerField(blank=True, null=True)
    mds_right = models.NullBooleanField()
    pr_asset_right = models.NullBooleanField()
    pr_part_right = models.NullBooleanField()
    pr_service_right = models.NullBooleanField()
    pr_validation_right = models.NullBooleanField()
    pr_stat_right = models.NullBooleanField()
    pr_settings_right = models.NullBooleanField()
    auto_id = models.BigIntegerField(unique=True)
    apm_quick_wo_status = models.NullBooleanField()
    location_right = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'droits'


class Ecri(Model):
    code_ecri = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(unique=True)  # This field type is a guess.
    nom2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specc = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ret = models.CharField(max_length=1, blank=True, null=True)
    eq_amt_com = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_ac = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_act = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ecri'


class ElRequest(Model):
    request_id = models.BigIntegerField(primary_key=True)
    fk_md_code = models.TextField(unique=True)  # This field type is a guess.
    fk_site_code = models.TextField(unique=True)  # This field type is a guess.
    fk_location_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    borrower_id = models.BigIntegerField(blank=True, null=True)
    borrower_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    borrower_phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    model_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    ecri_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    ecri_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    manufacturer = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_date = models.TextField(unique=True)  # This field type is a guess.
    request_time = models.TextField(unique=True)  # This field type is a guess.
    wished_start_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    wished_start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    wished_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    wished_end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    duration_hour = models.IntegerField(blank=True, null=True)
    duration_day = models.IntegerField(blank=True, null=True)
    duration_unit_number = models.IntegerField(blank=True, null=True)
    duration_unit = models.IntegerField(blank=True, null=True)
    request_status = models.IntegerField(blank=True, null=True)
    request_comment = models.TextField(blank=True, null=True)
    reject_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    reject_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    approved_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    approved_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    library_md_no = models.TextField(blank=True, null=True)  # This field type is a guess.
    library_site_no = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_status_historic = models.TextField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.IntegerField(blank=True, null=True)
    id_usertable2 = models.IntegerField(blank=True, null=True)
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'el_request'


class ElRequestItem(Model):
    request_item_id = models.BigIntegerField(primary_key=True)
    request_id = models.BigIntegerField(unique=True)
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    item_request_status = models.IntegerField(blank=True, null=True)
    wo_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    loan_start_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    loan_start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    expected_return_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    expected_return_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    loan_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    loan_end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    back2stock_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    back2stock_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_item_comment = models.TextField(blank=True, null=True)
    expected_duration_hour = models.IntegerField(blank=True, null=True)
    expected_duration_day = models.TextField(blank=True, null=True)  # This field type is a guess.
    effective_duration_hour = models.IntegerField(blank=True, null=True)
    effective_duration_day = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_damaged = models.IntegerField(blank=True, null=True)
    is_not_clean = models.IntegerField(blank=True, null=True)
    is_unrepareable = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    back2stock_duration_hour = models.IntegerField(blank=True, null=True)
    back2stock_duration_day = models.TextField(blank=True, null=True)  # This field type is a guess.
    items_availables_by_model = models.IntegerField(blank=True, null=True)
    items_in_loan_by_model = models.IntegerField(blank=True, null=True)
    items_availables_by_ecri = models.IntegerField(blank=True, null=True)
    items_in_loan_by_ecri = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'el_request_item'


class EmailNotificationEvents(Model):
    id_email = models.BigIntegerField(primary_key=True)
    notif_datetimestamp = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    in_venan_index = models.BigIntegerField(blank=True, null=True)
    caller_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    old_int_statut = models.CharField(max_length=20, blank=True, null=True)
    int_statut = models.CharField(max_length=20, blank=True, null=True)
    cadre = models.CharField(max_length=1, blank=True, null=True)
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    action_type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'email_notification_events'


class EnCours(Model):
    nu_int = models.TextField(primary_key=True)  # This field type is a guess.
    nu_bon_c = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_imm = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_ap = models.CharField(max_length=10, blank=True, null=True)
    he_ap = models.CharField(max_length=8, blank=True, null=True)
    da_int = models.CharField(max_length=10, blank=True, null=True)
    he_int = models.CharField(max_length=8, blank=True, null=True)
    da_hs = models.CharField(max_length=10, blank=True, null=True)
    he_hs = models.CharField(max_length=8, blank=True, null=True)
    da_dis = models.CharField(max_length=10, blank=True, null=True)
    he_dis = models.CharField(max_length=8, blank=True, null=True)
    da_fin = models.CharField(max_length=10, blank=True, null=True)
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
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    observ3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_syst = models.CharField(max_length=10, blank=True, null=True)
    da_rec = models.CharField(max_length=10, blank=True, null=True)
    he_rec = models.CharField(max_length=8, blank=True, null=True)
    delai = models.IntegerField(blank=True, null=True)
    code_delai = models.CharField(max_length=1, blank=True, null=True)
    da_hdelai = models.CharField(max_length=10, blank=True, null=True)
    n_devis = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_facture = models.TextField(blank=True, null=True)  # This field type is a guess.
    mt_engag = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_recp = models.CharField(max_length=10, blank=True, null=True)
    tot_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_cadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_statut = models.TextField(blank=True, null=True)  # This field type is a guess.
    par1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    par5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_contact_person_id = models.BigIntegerField(blank=True, null=True)
    fk_address_id = models.BigIntegerField(blank=True, null=True)
    date_of_nu_bon_c = models.CharField(max_length=10, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    is_digital_sign = models.NullBooleanField()
    is_wo_sign_mandatory = models.NullBooleanField()
    competency_is_activated = models.NullBooleanField()
    id_usertable6 = models.BigIntegerField(blank=True, null=True)
    id_usertable7 = models.BigIntegerField(blank=True, null=True)
    id_usertable8 = models.BigIntegerField(blank=True, null=True)
    wo_forward_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_decontaminated = models.TextField(blank=True, null=True)  # This field type is a guess.
    response_time_calcul_mode = models.NullBooleanField()
    udi = models.TextField(blank=True, null=True)  # This field type is a guess.
    call_creator = models.TextField(blank=True, null=True)  # This field type is a guess.
    autodispatch_notif_status = models.NullBooleanField()
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


class EnCoursTampon(Model):
    id = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    int_statut = models.CharField(max_length=20, blank=True, null=True)
    lib_statut = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_forward_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    disp_ap_at = models.CharField(max_length=1, blank=True, null=True)
    disp_ef_at = models.CharField(max_length=1, blank=True, null=True)
    process_status = models.NullBooleanField()
    is_inserted_updated = models.NullBooleanField()
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'en_cours_tampon'


class EqCneh(Model):
    n_nom_cneh = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specc = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_specl2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ret = models.CharField(max_length=1, blank=True, null=True)
    eq_amt_com = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_ac = models.TextField(blank=True, null=True)  # This field type is a guess.
    crit_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    remp_prix = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    ch5 = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    riskcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    ecr_modcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'eq_cneh'


class Etabli(Model):
    n_etab = models.TextField(primary_key=True)  # This field type is a guess.
    nom_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    adr_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    ville_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    cp_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_territory_id = models.BigIntegerField(blank=True, null=True)
    fk_license_service_area_id = models.BigIntegerField(blank=True, null=True)
    fk_customer_id = models.BigIntegerField(blank=True, null=True)
    fk_contact_person_id = models.BigIntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'etabli'


class EventAutodispatchAssignment(Model):
    id = models.BigIntegerField(primary_key=True)
    n_imma = models.TextField(unique=True)  # This field type is a guess.
    int_cm = models.TextField(unique=True)  # This field type is a guess.
    code_techn = models.TextField(unique=True)  # This field type is a guess.
    order_notification = models.IntegerField(unique=True)
    delay_notification = models.IntegerField(unique=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'event_autodispatch_assignment'


class EventAutodispatchAudit(Model):
    id = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    event_date = models.TextField(unique=True)  # This field type is a guess.
    event_time = models.TextField(unique=True)  # This field type is a guess.
    notification_type = models.BooleanField(unique=True)
    call_status = models.BooleanField(unique=True)
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    email_or_phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    result = models.NullBooleanField()
    detail = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_autodispatch_audit'


class EventAutodispatchWoid(Model):
    short_id = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'event_autodispatch_woid'


class EventAutodispatchWorkflow(Model):
    id = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_sent_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_sent_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_read_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_read_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    currenttrackingid = models.BigIntegerField(blank=True, null=True)
    acceptedtrackingid = models.BigIntegerField(blank=True, null=True)
    status = models.BooleanField(unique=True)
    useemail = models.NullBooleanField()
    usesms = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'event_autodispatch_workflow'


class EventContextFields(Model):
    event_context_id = models.IntegerField(primary_key=True)
    table_view_name = models.TextField()  # This field type is a guess.
    field_name = models.TextField()  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_pk = models.NullBooleanField()
    is_trigger = models.NullBooleanField()
    is_filter = models.NullBooleanField()
    is_body_field = models.NullBooleanField()
    id_msg_field = models.IntegerField(blank=True, null=True)
    ref_field_return_name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'event_context_fields'
        unique_together = (('event_context_id', 'table_view_name', 'field_name'),)


class EventContextHeaders(Model):
    event_context_id = models.IntegerField(primary_key=True)
    event_context_name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'event_context_headers'


class EventContextRecipients(Model):
    event_context_id = models.IntegerField(primary_key=True)
    event_recipient_group_id = models.IntegerField(unique=True)
    event_recipient_group_name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'event_context_recipients'
        unique_together = (('event_context_id', 'event_recipient_group_id'),)


class EventNotificationDetail(Model):
    event_detail_id = models.BigIntegerField(primary_key=True)
    fk_event_header_id = models.BigIntegerField(unique=True)
    event_context_id = models.IntegerField(blank=True, null=True)
    category_field = models.NullBooleanField()
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_operator = models.IntegerField(blank=True, null=True)
    string_value = models.TextField(blank=True, null=True)
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_option_date = models.IntegerField(blank=True, null=True)
    date_value = models.IntegerField(blank=True, null=True)
    id_msg_field = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_notification_detail'


class EventNotificationHeader(Model):
    event_header_id = models.BigIntegerField(primary_key=True)
    event_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_description = models.TextField(blank=True, null=True)
    event_retired_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_context_id = models.IntegerField(blank=True, null=True)
    event_is_autodispatch = models.NullBooleanField()
    event_notify_more_emails_to = models.TextField(blank=True, null=True)
    event_notify_more_sms_to = models.TextField(blank=True, null=True)
    event_notify_more_emails_cc = models.TextField(blank=True, null=True)
    event_notify_more_sms_cc = models.TextField(blank=True, null=True)
    event_user_query = models.TextField(blank=True, null=True)
    event_text_email_option = models.NullBooleanField()
    event_text_email_subject = models.TextField(blank=True, null=True)
    event_text_email_body = models.TextField(blank=True, null=True)
    event_text_sms_option = models.NullBooleanField()
    event_text_sms_body = models.TextField(blank=True, null=True)
    event_final_query = models.TextField(blank=True, null=True)
    id_msg_event_name = models.IntegerField(blank=True, null=True)
    id_msg_event_description = models.IntegerField(blank=True, null=True)
    id_msg_text_email_subject = models.IntegerField(blank=True, null=True)
    id_msg_text_email_body = models.IntegerField(blank=True, null=True)
    id_msg_text_sms_body = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_notification_header'


class EventNotificationRecipient(Model):
    event_recipient_id = models.BigIntegerField(primary_key=True)
    fk_event_header_id = models.BigIntegerField(unique=True)
    event_context_id = models.IntegerField(unique=True)
    event_recipient_group_id = models.IntegerField(unique=True)
    event_recipient_group_type = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'event_notification_recipient'


class EventNotificationTracking(Model):
    event_tracking_id = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    event_tracking_date = models.TextField(unique=True)  # This field type is a guess.
    event_tracking_time = models.TextField(unique=True)  # This field type is a guess.
    event_tracking_date_expire = models.TextField(unique=True)  # This field type is a guess.
    event_tracking_time_expire = models.TextField(unique=True)  # This field type is a guess.
    event_tracking_recipient_type = models.NullBooleanField()
    event_tracking_td = models.TextField(unique=True)  # This field type is a guess.
    event_tracking_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_tracking_phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_tracking_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_tracking_result = models.NullBooleanField()
    event_tracking_failure = models.TextField(blank=True, null=True)
    event_tracking_respone = models.TextField(blank=True, null=True)
    event_tracking_status = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'event_notification_tracking'


class Famimag(Model):
    magdef = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'famimag'


class Feature(Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'feature'


class FinanceExclusion(Model):
    table_name = models.TextField(primary_key=True)  # This field type is a guess.
    field_name = models.TextField(unique=True)  # This field type is a guess.
    keyword_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'finance_exclusion'
        unique_together = (('table_name', 'field_name'),)


class Fournis2(Model):
    code_four = models.CharField(primary_key=True, max_length=10)
    f_cle_comp = models.CharField(max_length=1, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_resp = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_adr = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_pays = models.CharField(max_length=3, blank=True, null=True)
    f_codp = models.CharField(max_length=10, blank=True, null=True)
    f_vill = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_mailing = models.CharField(max_length=1, blank=True, null=True)
    f_adr_1_2 = models.CharField(max_length=1, blank=True, null=True)
    f_tel = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_fax = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_resp2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_adr2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_pays2 = models.CharField(max_length=3, blank=True, null=True)
    f_codp2 = models.CharField(max_length=10, blank=True, null=True)
    f_vill2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_tel2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_fax2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    xx = models.CharField(max_length=1, blank=True, null=True)
    f_form_jur = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_rc = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_siret = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ape = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_adr_obs = models.TextField(blank=True, null=True)  # This field type is a guess.
    xxxx = models.CharField(max_length=1, blank=True, null=True)
    f_trav_ent = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_spec_ent = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_trav_equ = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_qualif = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_classif = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_opqcb = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_spec = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_qual_obs = models.TextField(blank=True, null=True)  # This field type is a guess.
    yyy = models.CharField(max_length=1, blank=True, null=True)
    f_ass_rc = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ass_cons = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_ca_kf = models.IntegerField(blank=True, null=True)
    f_jurid = models.CharField(max_length=2, blank=True, null=True)
    f_jurid_ob = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_rouge = models.CharField(max_length=1, blank=True, null=True)
    f_rouge_da = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_rouge_ob = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_obs_gen = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_marche_i = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_comm = models.TextField(blank=True, null=True)  # This field type is a guess.
    actif = models.CharField(max_length=1, blank=True, null=True)
    f_seuil = models.TextField(blank=True, null=True)  # This field type is a guess.
    ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_site = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_state = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_state2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    supplier_parent_number = models.CharField(max_length=10, blank=True, null=True)
    supplier_tree_path = models.TextField(blank=True, null=True)  # This field type is a guess.
    supplier_tree_level = models.IntegerField(blank=True, null=True)
    financial_account_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler8 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler9 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'fournis2'


class Grpeqp(Model):
    n_imma = models.TextField(unique=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    nimma_pere = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_pere = models.TextField(blank=True, null=True)  # This field type is a guess.
    niveau = models.TextField(primary_key=True)  # This field type is a guess.
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_by = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'grpeqp'


class Histctrl(Model):
    nu_ctrl = models.TextField(primary_key=True)  # This field type is a guess.
    typ_mod = models.TextField(unique=True)  # This field type is a guess.
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl1param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl2param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl3param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl4param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl5param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl6param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl7param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl8param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl9param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl10param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl11param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl12param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl13param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl14param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl15param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl1val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl2val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl3val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl4val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl5val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl6val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl7val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl8val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl9val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl10val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl11val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl12val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl13val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl14val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl15val = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl16param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl17param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl18param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl19param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl20param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl21param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl22param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl23param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl24param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl25param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl26param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl27param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl28param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl29param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl30param = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl16val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl17val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl18val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl19val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl20val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl21val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl22val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl23val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl24val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl25val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl26val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl27val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl28val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl29val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl30val = models.TextField(blank=True, null=True)  # This field type is a guess.
    ctrl1status = models.IntegerField(blank=True, null=True)
    ctrl2status = models.IntegerField(blank=True, null=True)
    ctrl3status = models.IntegerField(blank=True, null=True)
    ctrl4status = models.IntegerField(blank=True, null=True)
    ctrl5status = models.IntegerField(blank=True, null=True)
    ctrl6status = models.IntegerField(blank=True, null=True)
    ctrl7status = models.IntegerField(blank=True, null=True)
    ctrl8status = models.IntegerField(blank=True, null=True)
    ctrl9status = models.IntegerField(blank=True, null=True)
    ctrl10status = models.IntegerField(blank=True, null=True)
    ctrl11status = models.IntegerField(blank=True, null=True)
    ctrl12status = models.IntegerField(blank=True, null=True)
    ctrl13status = models.IntegerField(blank=True, null=True)
    ctrl14status = models.IntegerField(blank=True, null=True)
    ctrl15status = models.IntegerField(blank=True, null=True)
    ctrl16status = models.IntegerField(blank=True, null=True)
    ctrl17status = models.IntegerField(blank=True, null=True)
    ctrl18status = models.IntegerField(blank=True, null=True)
    ctrl19status = models.IntegerField(blank=True, null=True)
    ctrl20status = models.IntegerField(blank=True, null=True)
    ctrl21status = models.IntegerField(blank=True, null=True)
    ctrl22status = models.IntegerField(blank=True, null=True)
    ctrl23status = models.IntegerField(blank=True, null=True)
    ctrl24status = models.IntegerField(blank=True, null=True)
    ctrl25status = models.IntegerField(blank=True, null=True)
    ctrl26status = models.IntegerField(blank=True, null=True)
    ctrl27status = models.IntegerField(blank=True, null=True)
    ctrl28status = models.IntegerField(blank=True, null=True)
    ctrl29status = models.IntegerField(blank=True, null=True)
    ctrl30status = models.IntegerField(blank=True, null=True)
    hist_release_number = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'histctrl'


class HistoEq(Model):
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
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    asset_annual_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_net_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vcq = models.CharField(max_length=2, blank=True, null=True)
    financial_period_from = models.TextField()  # This field type is a guess.
    financial_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    inactive_contract_asset_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    contract_asset_status = models.IntegerField(blank=True, null=True)
    pd_mp_int = models.NullBooleanField()
    pd_mc_int = models.NullBooleanField()
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
    auto_id = models.BigIntegerField(unique=True)
    is_user_change_cost = models.IntegerField(blank=True, null=True)
    ht_net = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'histo_eq'
        unique_together = (('n_contrat', 'n_imma', 'generic_seq', 'financial_period_from'),)


class HistoEqBkp108(Model):
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_type = models.CharField(max_length=10, blank=True, null=True)
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    generic_seq = models.IntegerField(blank=True, null=True)
    fk_lieu_n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_nu_compte = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    asset_annual_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_annual_net_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_vcq = models.CharField(max_length=2, blank=True, null=True)
    financial_period_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    financial_period_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    inactive_contract_asset_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    contract_asset_status = models.IntegerField(blank=True, null=True)
    pd_mp_int = models.NullBooleanField()
    pd_mc_int = models.NullBooleanField()
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
    auto_id = models.BigIntegerField(primary_key=True)
    is_user_change_cost = models.IntegerField(blank=True, null=True)
    ht_net = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'histo_eq_bkp_108'


class Idepiece(Model):
    c_refer = models.TextField(primary_key=True)  # This field type is a guess.
    c_design = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10)
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    piece = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_prix_uni = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_unite = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_tva = models.CharField(max_length=1, blank=True, null=True)
    stock1995 = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_stock_qm = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_march_ie = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_cre = models.TextField(blank=True, null=True)  # This field type is a guess.
    qte_stock = models.TextField(blank=True, null=True)  # This field type is a guess.
    stock_val = models.TextField(blank=True, null=True)  # This field type is a guess.
    cum_entree = models.TextField(blank=True, null=True)  # This field type is a guess.
    cum_sortie = models.TextField(blank=True, null=True)  # This field type is a guess.
    fdg = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_ref = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_reform = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_device_type = models.BigIntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_mpu = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    d_update_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler8 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler9 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler10 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.IntegerField(blank=True, null=True)
    id_usertable2 = models.IntegerField(blank=True, null=True)
    id_usertable3 = models.IntegerField(blank=True, null=True)
    id_usertable4 = models.IntegerField(blank=True, null=True)
    id_usertable5 = models.IntegerField(blank=True, null=True)
    ipi_date_peremption = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_dgos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'idepiece'
        unique_together = (('c_refer', 'code_four'),)


class InVenan(Model):
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ordre = models.IntegerField(blank=True, null=True)
    da_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    he_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    da_fin = models.TextField(blank=True, null=True)  # This field type is a guess.
    he_fin = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_int = models.CharField(max_length=1, blank=True, null=True)
    code_four = models.CharField(max_length=10, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    nhee = models.TextField(blank=True, null=True)  # This field type is a guess.
    mo_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    dep_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd1_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    pd2_ht = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    nhe = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_nhe = models.TextField(blank=True, null=True)  # This field type is a guess.
    hint = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_dep = models.TextField(blank=True, null=True)  # This field type is a guess.
    piec = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    chint = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    div_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_tva1 = models.CharField(max_length=1, blank=True, null=True)
    t_tva1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_tva2 = models.CharField(max_length=1, blank=True, null=True)
    t_tva2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    cmnt = models.TextField(blank=True, null=True)  # This field type is a guess.
    plannedstartdate = models.TextField(blank=True, null=True)  # This field type is a guess.
    plannedstarttime = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimatedduration = models.TextField(blank=True, null=True)  # This field type is a guess.
    in_venan_index = models.BigIntegerField(primary_key=True)
    udf_1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    inc_transp_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    inc_transp_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    inc_transp_code_four = models.CharField(max_length=10, blank=True, null=True)
    out_transp_number = models.TextField(blank=True, null=True)  # This field type is a guess.
    out_transp_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    out_transp_code_four = models.CharField(max_length=10, blank=True, null=True)
    external_labor_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_travel_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_part1_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_part2_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_misc_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_total_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_labor_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_extra_travel_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_travel_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_misc_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_total_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.IntegerField(blank=True, null=True)
    id_usertable2 = models.IntegerField(blank=True, null=True)
    id_usertable3 = models.IntegerField(blank=True, null=True)
    id_usertable4 = models.IntegerField(blank=True, null=True)
    id_usertable5 = models.IntegerField(blank=True, null=True)
    cost_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_techn_notified = models.IntegerField(blank=True, null=True)
    working_hour_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    travel_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_service_provider_notified = models.IntegerField(blank=True, null=True)
    is_hourcost_applied = models.IntegerField(blank=True, null=True)
    is_travelcost_applied = models.IntegerField(blank=True, null=True)
    inv_ge_taskcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'in_venan'


class InVenanTampon(Model):
    id = models.BigIntegerField(primary_key=True)
    in_venan_index = models.BigIntegerField(unique=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    code_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    techn_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    process_status = models.NullBooleanField()
    is_inserted_updated = models.NullBooleanField()
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'in_venan_tampon'


class Inciden(Model):
    ref_int = models.TextField(primary_key=True)  # This field type is a guess.
    num_seq = models.IntegerField(blank=True, null=True)
    date_inc = models.TextField(blank=True, null=True)  # This field type is a guess.
    des_inc = models.TextField(blank=True, null=True)  # This field type is a guess.
    lieu_inc = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_emis = models.CharField(max_length=1, blank=True, null=True)
    ref_minis = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_minis = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_envoi = models.CharField(max_length=1, blank=True, null=True)
    date_envoi = models.TextField(blank=True, null=True)  # This field type is a guess.
    arch_inc = models.CharField(max_length=1, blank=True, null=True)
    arch_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_mes = models.TextField(blank=True, null=True)  # This field type is a guess.
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    des_con = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod_co = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque_co = models.TextField(blank=True, null=True)  # This field type is a guess.
    dm_steril = models.CharField(max_length=1, blank=True, null=True)
    date_steri = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_perem = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_emet = models.CharField(max_length=1, blank=True, null=True)
    n_uf_eme = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf_eme = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_eme = models.TextField(blank=True, null=True)  # This field type is a guess.
    qua_eme = models.TextField(blank=True, null=True)  # This field type is a guess.
    tel_eme = models.TextField(blank=True, null=True)  # This field type is a guess.
    fax_eme = models.TextField(blank=True, null=True)  # This field type is a guess.
    info_four = models.CharField(max_length=1, blank=True, null=True)
    etat_inc = models.CharField(max_length=1, blank=True, null=True)
    n_uf_ana = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf_ana = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_ana = models.TextField(blank=True, null=True)  # This field type is a guess.
    qua_ana = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_ana = models.TextField(blank=True, null=True)  # This field type is a guess.
    analyse_t = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    qua_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    action_t = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf_dec = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf_dec = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_dec = models.TextField(blank=True, null=True)  # This field type is a guess.
    qua_dec = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_dec = models.TextField(blank=True, null=True)  # This field type is a guess.
    decision_t = models.TextField(blank=True, null=True)  # This field type is a guess.
    titre_cir = models.TextField(blank=True, null=True)  # This field type is a guess.
    resum_cir = models.TextField(blank=True, null=True)  # This field type is a guess.
    action_d = models.TextField(blank=True, null=True)  # This field type is a guess.
    orga_nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    orga_tel = models.TextField(blank=True, null=True)  # This field type is a guess.
    orga_fax = models.TextField(blank=True, null=True)  # This field type is a guess.
    orga_ad = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    inc_soft_release = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'inciden'


class Insertuf(Model):
    id = models.TextField(primary_key=True)  # This field type is a guess.
    username = models.TextField(blank=True, null=True)  # This field type is a guess.
    password = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_profile_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    context = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'insertuf'


class ItUsers(Model):
    id_it_user = models.BigIntegerField(primary_key=True)
    n_util = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_util = models.TextField(unique=True)  # This field type is a guess.
    prenom = models.TextField(blank=True, null=True)  # This field type is a guess.
    tel = models.TextField(blank=True, null=True)  # This field type is a guess.
    fax = models.TextField(blank=True, null=True)  # This field type is a guess.
    portable = models.TextField(blank=True, null=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    login_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_profes = models.BigIntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'it_users'


class Jferies(Model):
    datefete = models.CharField(primary_key=True, max_length=10)
    texte = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'jferies'


class KpiDashboard(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    id_dashboard = models.IntegerField(unique=True)
    dashboard_sql = models.TextField(blank=True, null=True)
    dashboard_table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    dashboard_sql_user_input = models.IntegerField(blank=True, null=True)
    dashboard_graph_type = models.IntegerField(blank=True, null=True)
    dashboard_title_x = models.TextField(blank=True, null=True)  # This field type is a guess.
    dashboard_title_y = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'kpi_dashboard'
        unique_together = (('fk_id_kpi_ref', 'id_dashboard'),)


class KpiDashboardX(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    fk_id_dashboard = models.IntegerField(unique=True)
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_dashboard_x'
        unique_together = (('fk_id_kpi_ref', 'fk_id_dashboard'),)


class KpiDashboardY(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    fk_id_dashboard = models.IntegerField(unique=True)
    order_seq = models.IntegerField(unique=True)
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    dashboard_calcul_mode = models.IntegerField(blank=True, null=True)
    dashboard_count_distinct = models.IntegerField(blank=True, null=True)
    dashboard_top_n_number = models.IntegerField(blank=True, null=True)
    dashboard_sorted_desc_asc = models.IntegerField(blank=True, null=True)
    dashboard_id_color = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_dashboard_y'
        unique_together = (('fk_id_kpi_ref', 'fk_id_dashboard', 'order_seq'),)


class KpiFieldsFilter(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    order_seq = models.IntegerField(unique=True)
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_fields_filter'
        unique_together = (('fk_id_kpi_ref', 'order_seq'),)


class KpiFieldsFilterValues(Model):
    id_kpi_user = models.IntegerField(primary_key=True)
    fk_id_kpi_ref = models.IntegerField(unique=True)
    order_seq = models.IntegerField(unique=True)
    fk_profile_user = models.TextField(unique=True)  # This field type is a guess.
    fk_login_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    id_operator = models.IntegerField(blank=True, null=True)
    string_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_option_date = models.IntegerField(blank=True, null=True)
    date_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_fields_filter_values'
        unique_together = (('id_kpi_user', 'fk_id_kpi_ref', 'fk_profile_user', 'order_seq'),)


class KpiFieldsSelect(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    order_seq = models.IntegerField(unique=True)
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    is_id_ui_associated = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_fields_select'
        unique_together = (('fk_id_kpi_ref', 'order_seq'),)


class KpiMandatoryFilter(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    order_seq = models.IntegerField(unique=True)
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    id_operator = models.IntegerField(blank=True, null=True)
    string_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_option_date = models.IntegerField(blank=True, null=True)
    date_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_mandatory_filter'
        unique_together = (('fk_id_kpi_ref', 'order_seq'),)


class KpiMandatoryFilterValues(Model):
    id_kpi_user = models.IntegerField(primary_key=True)
    fk_id_kpi_ref = models.IntegerField(unique=True)
    order_seq = models.IntegerField(unique=True)
    fk_profile_user = models.TextField(unique=True)  # This field type is a guess.
    fk_login_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    id_operator = models.IntegerField(blank=True, null=True)
    string_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_option_date = models.IntegerField(blank=True, null=True)
    date_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_mandatory_filter_values'
        unique_together = (('id_kpi_user', 'fk_id_kpi_ref', 'fk_profile_user', 'order_seq'),)


class KpiProfileSelection(Model):
    id_kpi_user = models.IntegerField(primary_key=True)
    fk_id_kpi_ref = models.IntegerField(unique=True)
    fk_profile_user = models.TextField(unique=True)  # This field type is a guess.
    dashboard_in_use = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_profile_selection'
        unique_together = (('id_kpi_user', 'fk_id_kpi_ref', 'fk_profile_user'),)


class KpiReference(Model):
    id_kpi = models.IntegerField(primary_key=True)
    title_kpi = models.TextField(unique=True)  # This field type is a guess.
    description_kpi = models.TextField(unique=True)  # This field type is a guess.
    query_kpi = models.TextField(unique=True)
    table_view_name_kpi = models.TextField(unique=True)  # This field type is a guess.
    query_select_use_kpi = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_ui_associated_kpi = models.IntegerField(blank=True, null=True)
    dashboard_type_kpi = models.IntegerField(blank=True, null=True)
    fk_id_msg_title_kpi = models.IntegerField(blank=True, null=True)
    fk_id_msg_description_kpi = models.IntegerField(blank=True, null=True)
    fk_vocation = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_profile = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_site_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_assetplus = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'kpi_reference'


class KpiSqlFilter(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    order_seq = models.IntegerField(unique=True)
    sql_filter = models.TextField(blank=True, null=True)
    sql_filter_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    sql_filter_is_mandatory = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_sql_filter'
        unique_together = (('fk_id_kpi_ref', 'order_seq'),)


class KpiSqlFilterValues(Model):
    id_kpi_user = models.IntegerField(primary_key=True)
    fk_id_kpi_ref = models.IntegerField(unique=True)
    order_seq = models.IntegerField(unique=True)
    fk_profile_user = models.TextField(unique=True)  # This field type is a guess.
    fk_login_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    sql_filter = models.TextField(blank=True, null=True)
    sql_filter_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_sql_filter_values'
        unique_together = (('id_kpi_user', 'fk_id_kpi_ref', 'fk_profile_user', 'order_seq'),)


class KpiTdbUserSetting(Model):
    id_tdb_user = models.IntegerField(primary_key=True)
    id_kpi_user = models.IntegerField(unique=True)
    fk_id_kpi_ref = models.IntegerField(unique=True)
    fk_profile_user = models.TextField(unique=True)  # This field type is a guess.
    fk_login_user = models.TextField(unique=True)  # This field type is a guess.
    dashboard_in_use = models.IntegerField(blank=True, null=True)
    pos_x = models.IntegerField(blank=True, null=True)
    pos_y = models.IntegerField(blank=True, null=True)
    pos_l = models.IntegerField(blank=True, null=True)
    pos_h = models.IntegerField(blank=True, null=True)
    tdb_x = models.IntegerField(blank=True, null=True)
    tdb_y = models.IntegerField(blank=True, null=True)
    tdb_l = models.IntegerField(blank=True, null=True)
    tdb_h = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_tdb_user_setting'


class KpiUserFilter(Model):
    fk_id_kpi_ref = models.IntegerField(primary_key=True)
    order_seq = models.IntegerField(unique=True)
    user_filter_type = models.IntegerField(unique=True)
    fk_pk_field = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_view_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_name_alias = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_filter_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_msg_field = models.IntegerField(blank=True, null=True)
    user_sql_filter = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_user_filter'
        unique_together = (('fk_id_kpi_ref', 'order_seq'),)


class KpiUserSetting(Model):
    id_kpi_user = models.IntegerField(primary_key=True)
    fk_id_kpi_ref = models.IntegerField(unique=True)
    fk_profile_user = models.TextField(unique=True)  # This field type is a guess.
    fk_login_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    dashboard_in_use = models.IntegerField(blank=True, null=True)
    title_kpi_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    dashboard_graph_type_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_user_setting'
        unique_together = (('id_kpi_user', 'fk_id_kpi_ref', 'fk_profile_user'),)


class Kpilog(Model):
    kpiname = models.TextField(primary_key=True)  # This field type is a guess.
    value = models.TextField(unique=True)  # This field type is a guess.
    logdate = models.TextField(unique=True)  # This field type is a guess.
    username = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'kpilog'


class LibChampsTechnique(Model):
    name = models.TextField(primary_key=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_lib_unites_technique_name = models.TextField(unique=True)  # This field type is a guess.
    with_value_list = models.IntegerField(blank=True, null=True)
    with_free_input_allowed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lib_champs_technique'
        unique_together = (('name', 'fk_lib_unites_technique_name'),)


class LibUnitesTechnique(Model):
    name = models.TextField(primary_key=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lib_unites_technique'


class LicenseServiceArea(Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(unique=True)  # This field type is a guess.
    fk_territory_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'license_service_area'


class Lieu(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)
    fk_all_pictures_id = models.BigIntegerField(blank=True, null=True)
    full_path = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_dgos = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lieu'


class LieuRecup20140630(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_recup_20140630'


class LieuSav20140507(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_sav_20140507'


class LieuSav20140523(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_sav_20140523'


class LieuSav20140613(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_sav_20140613'


class LieuSav20140702(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_sav_20140702'


class LieuSav20140704(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_sav_20140704'


class LieuTest(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_test'


class LieuTestSav20140630(Model):
    n_lieu = models.TextField(primary_key=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.CharField(max_length=7, blank=True, null=True)
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieu_test_sav_20140630'


class Lieusauve(Model):
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    reforme = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_loc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.BigIntegerField(blank=True, null=True)
    id_usertable2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lieusauve'


class LinkPropertiesPart(Model):
    id_lk_property_part = models.BigIntegerField(primary_key=True)
    flag_part_eqp = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    n_mag = models.TextField(blank=True, null=True)  # This field type is a guess.
    serie_lot = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_device_type = models.BigIntegerField(blank=True, null=True)
    id_property = models.BigIntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)  # This field type is a guess.
    unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'link_properties_part'


class LkAssetTd(Model):
    fk_asset = models.TextField(primary_key=True)  # This field type is a guess.
    fk_td = models.TextField(unique=True)  # This field type is a guess.
    is_master_td = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'lk_asset_td'
        unique_together = (('fk_asset', 'fk_td'),)


class LkBCompAPrevent2(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    nu_prevent = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_consumption = models.CharField(max_length=1, blank=True, null=True)
    n_mag = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_ref = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_design = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    qte_tbe_used = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_b_comp_a_prevent2'


class LkBEq1996Lieu(Model):
    fk_b_eq1996_n_imma = models.TextField(primary_key=True)  # This field type is a guess.
    fk_lieu_n_lieu = models.TextField(unique=True)  # This field type is a guess.
    nb_imma = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_b_eq1996_lieu'
        unique_together = (('fk_b_eq1996_n_imma', 'fk_lieu_n_lieu'),)


class LkBEq1996PrLines(Model):
    no_request = models.TextField(primary_key=True)  # This field type is a guess.
    no_line = models.IntegerField(unique=True)
    n_imma = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_b_eq1996_pr_lines'


class LkBEq1996Unites(Model):
    fk_b_eq1996_n_imma = models.TextField(primary_key=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField()  # This field type is a guess.
    nb_imma = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lk_b_eq1996_unites'
        unique_together = (('fk_b_eq1996_n_imma', 'fk_unites_n_uf'),)


class LkCalendarPrevent2(Model):
    nu_prevent = models.TextField(primary_key=True)  # This field type is a guess.
    date_planned = models.TextField(unique=True)  # This field type is a guess.
    date_execute = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_asset_done = models.IntegerField(blank=True, null=True)
    nb_asset_due = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_calendar_prevent2'
        unique_together = (('nu_prevent', 'date_planned'),)


class LkChecklistEqCneh(Model):
    fk_cth_id = models.BigIntegerField(primary_key=True)
    fk_n_nom_cneh = models.TextField()  # This field type is a guess.
    lce_mandatory = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'lk_checklist_eq_cneh'
        unique_together = (('fk_cth_id', 'fk_n_nom_cneh'),)


class LkChecklistPrevent2(Model):
    fk_cth_id = models.BigIntegerField(primary_key=True)
    fk_nu_prevent = models.TextField()  # This field type is a guess.
    lcp_mandatory = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'lk_checklist_prevent2'
        unique_together = (('fk_cth_id', 'fk_nu_prevent'),)


class LkChecklistTypes(Model):
    fk_cth_id = models.BigIntegerField(primary_key=True)
    fk_tp_type = models.TextField()  # This field type is a guess.
    fk_marque = models.TextField()  # This field type is a guess.
    lct_mandatory = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'lk_checklist_types'
        unique_together = (('fk_cth_id', 'fk_tp_type', 'fk_marque'),)


class LkChkTplEqCneh(Model):
    fk_chk_tpl_code = models.TextField(primary_key=True)  # This field type is a guess.
    fk_eq_cneh_n_nom_cneh = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_chk_tpl_eq_cneh'
        unique_together = (('fk_chk_tpl_code', 'fk_eq_cneh_n_nom_cneh'),)


class LkChkTplPrevent2(Model):
    fk_chk_tpl_code = models.TextField(primary_key=True)  # This field type is a guess.
    fk_prevent2_nu_prevent = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_chk_tpl_prevent2'
        unique_together = (('fk_chk_tpl_code', 'fk_prevent2_nu_prevent'),)


class LkChkTplTypes(Model):
    fk_chk_tpl_code = models.TextField(primary_key=True)  # This field type is a guess.
    fk_types_tp_type = models.TextField(unique=True)  # This field type is a guess.
    fk_types_marque = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_chk_tpl_types'
        unique_together = (('fk_chk_tpl_code', 'fk_types_tp_type', 'fk_types_marque'),)


class LkContactSite(Model):
    nu_contact = models.CharField(primary_key=True, max_length=10)
    n_etab = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_contact_site'
        unique_together = (('nu_contact', 'n_etab'),)


class LkCounterPrevent2(Model):
    nu_prevent = models.TextField(primary_key=True)  # This field type is a guess.
    counter_planned = models.IntegerField(unique=True)
    nb_asset_done = models.IntegerField(blank=True, null=True)
    nb_asset_due = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_counter_prevent2'
        unique_together = (('nu_prevent', 'counter_planned'),)


class LkDashboardProfile(Model):
    fk_profile_id = models.BigIntegerField(primary_key=True)
    fk_dashboard_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'lk_dashboard_profile'
        unique_together = (('fk_profile_id', 'fk_dashboard_id'),)


class LkPicture(Model):
    fk_all_pictures_id = models.BigIntegerField(blank=True, null=True)
    fk_b_eq1996_n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_idepiece_c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_idepiece_code_four = models.CharField(max_length=10, blank=True, null=True)
    fk_types_tp_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_types_marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_picture'


class LkPropFieldLocation(Model):
    auto_id = models.BigIntegerField(unique=True)
    fk_pfs_auto_id = models.BigIntegerField(primary_key=True)
    fk_n_lieu = models.TextField(unique=True)  # This field type is a guess.
    string_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_pvs_auto_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lk_prop_field_location'
        unique_together = (('fk_pfs_auto_id', 'fk_n_lieu'),)


class LkPropFieldTechfamily(Model):
    auto_id = models.BigIntegerField(unique=True)
    fk_pfs_auto_id = models.BigIntegerField(primary_key=True)
    fk_code_fam = models.TextField(unique=True)  # This field type is a guess.
    string_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_pvs_auto_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lk_prop_field_techfamily'
        unique_together = (('fk_pfs_auto_id', 'fk_code_fam'),)


class LkTechfield(Model):
    fk_lib_champs_technique_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_lib_unites_technique_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_b_eq1996_n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_idepiece_c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_idepiece_code_four = models.CharField(max_length=10, blank=True, null=True)
    value = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_lieu_n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_types_tp_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_types_marque = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_techfield'


class LkTrainingModels(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    fk_id_training = models.IntegerField(unique=True)
    fk_model_type = models.TextField(unique=True)  # This field type is a guess.
    fk_manufacturer = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_training_models'


class LkTrainingUsers(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    fk_id_training = models.IntegerField(unique=True)
    category_user = models.IntegerField(unique=True)
    fk_intern_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_intern_technician = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_md_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_site_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    usual_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_training_users'


class LkUniteStBEq1996(Model):
    fk_unite_st_code_techn = models.TextField(primary_key=True)  # This field type is a guess.
    fk_b_eq1996_n_imma = models.TextField(unique=True)  # This field type is a guess.
    c_metier = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_unite_st_b_eq1996'
        unique_together = (('fk_unite_st_code_techn', 'fk_b_eq1996_n_imma', 'c_metier'),)


class LkUniteStTypes(Model):
    fk_unite_st_code_techn = models.TextField(primary_key=True)  # This field type is a guess.
    fk_types_tp_type = models.TextField(unique=True)  # This field type is a guess.
    fk_types_marque = models.TextField(unique=True)  # This field type is a guess.
    rank = models.BigIntegerField(blank=True, null=True)
    c_metier = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_unite_st_types'
        unique_together = (('fk_unite_st_code_techn', 'fk_types_tp_type', 'fk_types_marque', 'c_metier'),)


class LkUserCsEtabli(Model):
    fk_user_cs_id = models.TextField(primary_key=True)  # This field type is a guess.
    fk_etabli_n_etab = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_cs_etabli'
        unique_together = (('fk_user_cs_id', 'fk_etabli_n_etab'),)


class LkUserCsTd(Model):
    fk_usercslogin = models.TextField(primary_key=True)  # This field type is a guess.
    fk_td = models.TextField(unique=True)  # This field type is a guess.
    is_master_td = models.BooleanField(unique=True)
    auto_id = models.BigIntegerField(unique=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_cs_td'
        unique_together = (('fk_usercslogin', 'fk_td'),)


class LkUserCsUnites(Model):
    fk_user_cs_id = models.TextField(primary_key=True)  # This field type is a guess.
    fk_unites_n_uf = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_cs_unites'
        unique_together = (('fk_user_cs_id', 'fk_unites_n_uf'),)


class LkUserCustomer(Model):
    fk_user_id = models.BigIntegerField(primary_key=True)
    fk_customer_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'lk_user_customer'
        unique_together = (('fk_user_id', 'fk_customer_id'),)


class LkUserEtabli(Model):
    fk_user_id = models.BigIntegerField(primary_key=True)
    fk_etabli_n_etab = models.TextField()  # This field type is a guess.
    lutieta_insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    lutieta_update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_etabli'
        unique_together = (('fk_user_id', 'fk_etabli_n_etab'),)


class LkUserLieu(Model):
    fk_user_id = models.BigIntegerField(primary_key=True)
    fk_lieu_n_lieu = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_lieu'
        unique_together = (('fk_user_id', 'fk_lieu_n_lieu'),)


class LkUserMetiers(Model):
    fk_user_id = models.BigIntegerField(primary_key=True)
    fk_metiers_c_metier = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_metiers'
        unique_together = (('fk_user_id', 'fk_metiers_c_metier'),)


class LkUserUnites(Model):
    fk_user_id = models.BigIntegerField(primary_key=True)
    fk_unites_n_uf = models.TextField()  # This field type is a guess.
    lutiuf_insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    lutiuf_update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'lk_user_unites'
        unique_together = (('fk_user_id', 'fk_unites_n_uf'),)


class LkUserUnitesSav20141031(Model):
    fk_user_id = models.BigIntegerField(unique=True)
    fk_unites_n_uf = models.CharField(primary_key=True, max_length=7)

    class Meta:
        managed = False
        db_table = 'lk_user_unites_sav_20141031'


class LocaHistoAsset(Model):
    loca_histo_date = models.TextField(unique=True)  # This field type is a guess.
    loca_histo_time = models.TextField(primary_key=True)  # This field type is a guess.
    loca_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_asset = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_ind_main = models.CharField(max_length=10, blank=True, null=True)
    ind_maint = models.TextField(blank=True, null=True)  # This field type is a guess.
    poste_w = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca_histo_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_id = models.BigIntegerField(blank=True, null=True)
    loca_histo_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca_histo_end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca_histo_duration = models.BigIntegerField(blank=True, null=True)
    event_type_rfid = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'loca_histo_asset'


class LocaHistoSets(Model):
    date_time = models.TextField(primary_key=True)  # This field type is a guess.
    who_update = models.TextField(blank=True, null=True)  # This field type is a guess.
    loca_histo_manage = models.TextField(blank=True, null=True)  # This field type is a guess.
    move_asset_of_fg = models.TextField(blank=True, null=True)  # This field type is a guess.
    move_child_asset = models.TextField(blank=True, null=True)  # This field type is a guess.
    move_wo_asset = models.TextField(blank=True, null=True)  # This field type is a guess.
    move_asset_md = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    change_date_location = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'loca_histo_sets'


class Magasin(Model):
    magnum = models.TextField(primary_key=True)  # This field type is a guess.
    magnom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    magdef = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mag = models.CharField(max_length=1, blank=True, null=True)
    commentm = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_comme = models.CharField(max_length=1, blank=True, null=True)
    tel_mag = models.TextField(blank=True, null=True)  # This field type is a guess.
    res_mag = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    livr1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    livr2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    livr3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    livr4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    livr5 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'magasin'


class Marques(Model):
    ma_nom = models.TextField(primary_key=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'marques'


class MdsEventSetting(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    event_description = models.TextField(unique=True)  # This field type is a guess.
    event_comments = models.TextField(blank=True, null=True)
    event_sql_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_sql_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_id_signatory = models.IntegerField(unique=True)
    event_wo_status = models.IntegerField(blank=True, null=True)
    event_multiples_sign = models.IntegerField(blank=True, null=True)
    event_linked_table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_linked_field_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_inactive_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mds_event_setting'


class MdsSignatoryHistoric(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    fk_nu_int = models.TextField(unique=True)  # This field type is a guess.
    fk_id_wf_event_sign = models.IntegerField(unique=True)
    fk_id_wf = models.IntegerField(unique=True)
    fk_id_event = models.IntegerField(unique=True)
    fk_id_signatory = models.IntegerField(unique=True)
    wf_sql_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_sql_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_multiples_sign = models.IntegerField(blank=True, null=True)
    sign_creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_creation_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_user_login = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_user_pw = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_user_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_picture = models.BinaryField(blank=True, null=True)
    sign_tracking_status = models.IntegerField(blank=True, null=True)
    sign_tracking_user_comment = models.TextField(blank=True, null=True)
    in_venan_index = models.IntegerField(blank=True, null=True)
    numdemm = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magfour = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_removed = models.IntegerField(blank=True, null=True)
    sign_tracking_overriden = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mds_signatory_historic'


class MdsSignatorySetting(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    signatory_description = models.TextField(unique=True)  # This field type is a guess.
    signatory_comments = models.TextField(blank=True, null=True)
    signatory_identification = models.IntegerField(blank=True, null=True)
    fk_signatory_profile_cs = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_signatory_user_cs = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_signatory_profile_web = models.BigIntegerField(blank=True, null=True)
    fk_signatory_user_web = models.BigIntegerField(blank=True, null=True)
    signatory_sql_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_signatory_end_user = models.IntegerField(blank=True, null=True)
    signatory_inactive_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mds_signatory_setting'


class MdsSignatoryTracking(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    fk_nu_int = models.TextField(unique=True)  # This field type is a guess.
    fk_id_wf_event_sign = models.IntegerField(unique=True)
    fk_id_wf = models.IntegerField(unique=True)
    fk_id_event = models.IntegerField(unique=True)
    fk_id_signatory = models.IntegerField(unique=True)
    wf_sql_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_sql_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_multiples_sign = models.IntegerField(blank=True, null=True)
    sign_creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_creation_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_user_login = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_user_pw = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_user_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_picture = models.BinaryField(blank=True, null=True)
    sign_tracking_status = models.IntegerField(blank=True, null=True)
    sign_tracking_user_comment = models.TextField(blank=True, null=True)
    in_venan_index = models.IntegerField(blank=True, null=True)
    numdemm = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magfour = models.TextField(blank=True, null=True)  # This field type is a guess.
    sign_tracking_removed = models.IntegerField(blank=True, null=True)
    sign_tracking_overriden = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mds_signatory_tracking'


class MdsWfEventSignSetting(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    fk_id_wf = models.IntegerField(unique=True)
    fk_id_event = models.IntegerField(unique=True)
    fk_id_signatory = models.IntegerField(unique=True)
    inactive_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mds_wf_event_sign_setting'


class MdsWfSetting(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    wf_description = models.TextField(unique=True)  # This field type is a guess.
    wf_comments = models.TextField(blank=True, null=True)
    wf_sql_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    wf_sql_query = models.TextField(unique=True)  # This field type is a guess.
    wf_inactive_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mds_wf_setting'


class Metiers(Model):
    c_metier = models.TextField(primary_key=True)  # This field type is a guess.
    resp = models.TextField(blank=True, null=True)  # This field type is a guess.
    cmnt = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_department_category = models.TextField(blank=True, null=True)  # This field type is a guess.
    ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    parent = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_operat_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    dispatch_parent_flag = models.TextField(blank=True, null=True)  # This field type is a guess.
    call_select_flag = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    dispatch_brother_flag = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_digital_sign = models.NullBooleanField()
    competency_is_activated = models.NullBooleanField()
    phone_fixe = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'metiers'


class MobilityTechnicalUse(Model):
    mtu_id = models.TextField(unique=True)  # This field type is a guess.
    mtu_value = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'mobility_technical_use'


class Modality(Model):
    mod_code = models.TextField(primary_key=True)  # This field type is a guess.
    mod_name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'modality'


class Numcom(Model):
    numco = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'numcom'


class Numintv(Model):
    numintv = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'numintv'


class Numpieces(Model):
    numco = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'numpieces'


class Numprev(Model):
    numprev = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'numprev'


class OperatSchedule(Model):
    operat_id = models.TextField(primary_key=True)  # This field type is a guess.
    operat_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    operat_day7 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'operat_schedule'


class ParaIni(Model):
    secname = models.TextField(primary_key=True)  # This field type is a guess.
    kwname = models.TextField(unique=True)  # This field type is a guess.
    kwvalue = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'para_ini'
        unique_together = (('secname', 'kwname'),)


class Parafen(Model):
    p_profil = models.TextField(primary_key=True)  # This field type is a guess.
    p_fenetre = models.TextField(unique=True)  # This field type is a guess.
    p_nom_chp = models.TextField(unique=True)  # This field type is a guess.
    p_lib_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_type_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_genre_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_visible = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_lib_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_saisie = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_valcar = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_valnum = models.IntegerField(blank=True, null=True)
    u_curseur = models.IntegerField(blank=True, null=True)
    u_ind_ongl = models.IntegerField(blank=True, null=True)
    u_num_mnu = models.IntegerField(blank=True, null=True)
    u_para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_mode = models.IntegerField(blank=True, null=True)
    p_fenetre_extension = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'parafen'


class Param(Model):
    rep = models.CharField(unique=True, max_length=20)
    datemaj = models.CharField(max_length=10, blank=True, null=True)
    cmnt = models.TextField(blank=True, null=True)  # This field type is a guess.
    tva1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    tva2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    dbtype = models.CharField(primary_key=True, max_length=1)
    printdef = models.CharField(max_length=1, blank=True, null=True)
    institut = models.CharField(max_length=45, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'param'


class Paramets(Model):
    para_type = models.CharField(max_length=1, blank=True, null=True)
    so_lib_fen = models.TextField(blank=True, null=True)  # This field type is a guess.
    para_fen = models.TextField(blank=True, null=True)  # This field type is a guess.
    so_lib_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    para_val = models.TextField(blank=True, null=True)  # This field type is a guess.
    para_lib = models.TextField(blank=True, null=True)  # This field type is a guess.
    para_vis = models.CharField(max_length=1, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'paramets'


class Paranum(Model):
    nomtab = models.TextField(primary_key=True)  # This field type is a guess.
    numero = models.BigIntegerField(blank=True, null=True)
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.IntegerField(blank=True, null=True)
    para4 = models.IntegerField(blank=True, null=True)
    flag_update = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    digitnumber = models.IntegerField(blank=True, null=True)
    prefix_type = models.IntegerField(blank=True, null=True)
    prefix_date_format = models.TextField(blank=True, null=True)  # This field type is a guess.
    prefix_other = models.TextField(blank=True, null=True)  # This field type is a guess.
    prefix_separator = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_used_prefix_numero = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paranum'


class Paraplanning(Model):
    plandesc = models.TextField(blank=True, null=True)  # This field type is a guess.
    plandefault = models.TextField(blank=True, null=True)  # This field type is a guess.
    wocolor = models.IntegerField(blank=True, null=True)
    pmcolor = models.IntegerField(blank=True, null=True)
    abscolor = models.IntegerField(blank=True, null=True)
    conflcolor = models.IntegerField(blank=True, null=True)
    charge1 = models.IntegerField(blank=True, null=True)
    charge2 = models.IntegerField(blank=True, null=True)
    charge3 = models.IntegerField(blank=True, null=True)
    charge4 = models.IntegerField(blank=True, null=True)
    overcharge = models.IntegerField(blank=True, null=True)
    woestimatedduration = models.TextField(blank=True, null=True)  # This field type is a guess.
    conflwarning = models.TextField(blank=True, null=True)  # This field type is a guess.
    abswarning = models.TextField(blank=True, null=True)  # This field type is a guess.
    overcwarning = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    pmestimatedduration = models.TextField(blank=True, null=True)  # This field type is a guess.
    closewarning = models.TextField(blank=True, null=True)  # This field type is a guess.
    details_dispmode = models.TextField(blank=True, null=True)  # This field type is a guess.
    cm_pmcolor = models.IntegerField(blank=True, null=True)
    training_color = models.IntegerField(blank=True, null=True)
    dayoff_color = models.IntegerField(blank=True, null=True)
    weekend_color = models.IntegerField(blank=True, null=True)
    is_unrolled_all = models.NullBooleanField()
    mode_display = models.NullBooleanField()
    view_display = models.NullBooleanField()
    unit_display_day = models.NullBooleanField()
    unit_display_week = models.NullBooleanField()
    fk_operat_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_profile_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    archivedcolor = models.IntegerField(blank=True, null=True)
    closedcolor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paraplanning'


class Paraprno(Model):
    prnobject = models.TextField(primary_key=True)  # This field type is a guess.
    prntheme = models.TextField(unique=True)  # This field type is a guess.
    prndescription = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'paraprno'
        unique_together = (('prnobject', 'prntheme'),)


class Paraprnt(Model):
    prnlanguage = models.CharField(primary_key=True, max_length=10)
    prnkey = models.TextField(unique=True)  # This field type is a guess.
    prnlabel = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'paraprnt'
        unique_together = (('prnlanguage', 'prnkey'),)


class Parasoph(Model):
    so_lib_fen = models.TextField(primary_key=True)  # This field type is a guess.
    so_lib_chp = models.TextField(unique=True)  # This field type is a guess.
    so_lib = models.TextField(unique=True)  # This field type is a guess.
    para_fen = models.TextField(unique=True)  # This field type is a guess.
    para_val = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'parasoph'


class Paratbls(Model):
    pname = models.TextField(primary_key=True)  # This field type is a guess.
    wname = models.TextField(unique=True)  # This field type is a guess.
    tname = models.TextField(unique=True)  # This field type is a guess.
    tpos = models.TextField(blank=True, null=True)  # This field type is a guess.
    tfix = models.TextField(blank=True, null=True)  # This field type is a guess.
    tsize = models.TextField(blank=True, null=True)  # This field type is a guess.
    tcol = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'paratbls'
        unique_together = (('pname', 'wname', 'tname'),)


class PasswordHistoric(Model):
    u_id = models.TextField(primary_key=True)  # This field type is a guess.
    user_pw_creationdate = models.TextField(unique=True)  # This field type is a guess.
    user_old_password = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'password_historic'
        unique_together = (('u_id', 'user_pw_creationdate'),)


class PermanentInventory(Model):
    pi_index = models.BigIntegerField(primary_key=True)
    pi_ppc_date = models.TextField(unique=True)  # This field type is a guess.
    u_id = models.TextField(unique=True)  # This field type is a guess.
    pi_last_synchronization_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_etab = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    ma_nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    tp_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    pi_found_asset = models.IntegerField(blank=True, null=True)
    pi_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    pi_validated = models.IntegerField(blank=True, null=True)
    pi_newasset = models.IntegerField(blank=True, null=True)
    pi_quantity = models.IntegerField(blank=True, null=True)
    pi_taken_action = models.IntegerField(blank=True, null=True)
    pi_movedasset = models.IntegerField(blank=True, null=True)
    pi_taken_action_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fonc = models.CharField(max_length=4, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    pi_assetname = models.TextField(blank=True, null=True)  # This field type is a guess.
    pi_asset_status = models.IntegerField(blank=True, null=True)
    pi_retired_asset = models.TextField(blank=True, null=True)  # This field type is a guess.
    pi_area_validated = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permanent_inventory'


class PieLEq(Model):
    ref_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'pie_l_eq'


class Pieces(Model):
    nu_piece = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    qte = models.TextField(blank=True, null=True)  # This field type is a guess.
    tot_ttc = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ef = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque_ap = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    c_prix_uni = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_tva = models.CharField(max_length=1, blank=True, null=True)
    n_seri_p = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magdem = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_magfour = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_sorti = models.CharField(max_length=1, blank=True, null=True)
    date_sorti = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    external_consumption = models.CharField(max_length=1, blank=True, null=True)
    voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_design = models.TextField(blank=True, null=True)  # This field type is a guess.
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    t_tva = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_mpu = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_ref = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_id_piece_reception = models.BigIntegerField(blank=True, null=True)
    generic = models.IntegerField(blank=True, null=True)
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    udf_5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_usertable1 = models.IntegerField(blank=True, null=True)
    id_usertable2 = models.IntegerField(blank=True, null=True)
    id_usertable3 = models.IntegerField(blank=True, null=True)
    id_usertable4 = models.IntegerField(blank=True, null=True)
    id_usertable5 = models.IntegerField(blank=True, null=True)
    piece = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_serialpart = models.TextField(blank=True, null=True)  # This field type is a guess.
    pie_ge_fromge = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'pieces'


class PiecesReception(Model):
    id = models.BigIntegerField(primary_key=True)
    n_mag = models.TextField(unique=True)  # This field type is a guess.
    c_refer = models.TextField(unique=True)  # This field type is a guess.
    c_design = models.TextField(blank=True, null=True)  # This field type is a guess.
    internal_ref = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(unique=True, max_length=10)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_seri = models.TextField(blank=True, null=True)  # This field type is a guess.
    numcomm = models.TextField(blank=True, null=True)  # This field type is a guess.
    numligne = models.IntegerField(blank=True, null=True)
    date_recep = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_unite = models.CharField(max_length=10, blank=True, null=True)
    qte_recep = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_prix_uni = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_tva = models.CharField(max_length=1, blank=True, null=True)
    t_tva = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_uf_dem = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_cpte = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_mpu = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_marche_publique = models.TextField(blank=True, null=True)  # This field type is a guess.
    qte_utilise = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_budget_an_exo = models.CharField(max_length=4, blank=True, null=True)
    transfert_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_unit_price = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'pieces_reception'


class PlanningEvent(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    plne_fk_category = models.CharField(unique=True, max_length=2)
    plne_event_title = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_event_note = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_event_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_start_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_end_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_duration_in_minutes = models.BigIntegerField(blank=True, null=True)
    plne_technician_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_supplier_code = models.CharField(max_length=10, blank=True, null=True)
    plne_supplier_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_location_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    plne_location_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planning_event'


class PlanningEventGuests(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    plng_fk_plne_auto_id = models.BigIntegerField(unique=True)
    plng_technician_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    plng_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    plng_supplier_code = models.CharField(max_length=10, blank=True, null=True)
    plng_supplier_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'planning_event_guests'


class Ppcsettings(Model):
    webserverurl = models.TextField(primary_key=True)  # This field type is a guess.
    webserverport = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ppcsettings'
        unique_together = (('webserverurl', 'webserverport'),)


class PrefixAutonumbering(Model):
    prefix_other_id = models.TextField(primary_key=True)  # This field type is a guess.
    prefix_numero = models.BigIntegerField(blank=True, null=True)
    is_used_prefix_numero = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prefix_autonumbering'


class PrevEqp(Model):
    nu_prevent = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    p1_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p2_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p3_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p4_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p5_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    statue = models.CharField(max_length=1, blank=True, null=True)
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    old_date_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    generic_seq = models.IntegerField(blank=True, null=True)
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_imma = models.IntegerField(blank=True, null=True)
    heure_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor_unit_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_refor_unit_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    prev_eqp_pk = models.BigIntegerField(primary_key=True)
    next_counter = models.IntegerField(blank=True, null=True)
    old_counter = models.IntegerField(blank=True, null=True)
    last_wo_done = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_pm_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_prep_id = models.BigIntegerField(blank=True, null=True)
    auto_id = models.BigIntegerField(unique=True)
    is_task_calculated = models.IntegerField(blank=True, null=True)
    trg_event = models.TextField(blank=True, null=True)  # This field type is a guess.
    trg_wo_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    trg_wo_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    trg_pmunit_id = models.BigIntegerField(blank=True, null=True)
    trg_pmocc_id = models.BigIntegerField(blank=True, null=True)
    init_pm_date_before = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prev_eqp'


class PrevEqpBkp105(Model):
    nu_prevent = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    p1_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p2_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p3_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p4_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    p5_num = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    statue = models.CharField(max_length=1, blank=True, null=True)
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    modification_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    old_date_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    generic = models.IntegerField(blank=True, null=True)
    generic_seq = models.IntegerField(blank=True, null=True)
    n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    nb_imma = models.IntegerField(blank=True, null=True)
    heure_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    estimated_duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor_unit_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_refor_unit_pm = models.TextField(blank=True, null=True)  # This field type is a guess.
    prev_eqp_pk = models.BigIntegerField(blank=True, null=True)
    next_counter = models.IntegerField(blank=True, null=True)
    old_counter = models.IntegerField(blank=True, null=True)
    last_wo_done = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_pm_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_prep_id = models.BigIntegerField(blank=True, null=True)
    auto_id = models.BigIntegerField(primary_key=True)
    is_task_calculated = models.IntegerField(blank=True, null=True)
    trg_event = models.TextField(blank=True, null=True)  # This field type is a guess.
    trg_wo_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    trg_wo_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    trg_pmunit_id = models.BigIntegerField(blank=True, null=True)
    trg_pmocc_id = models.BigIntegerField(blank=True, null=True)
    init_pm_date_before = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prev_eqp_bkp_105'


class PrevEqpPlanned(Model):
    prep_id = models.BigIntegerField(primary_key=True)
    prep_fk_nu_prevent = models.TextField(unique=True)  # This field type is a guess.
    prep_fk_prev_eqp_pk = models.BigIntegerField(unique=True)
    prep_date_planned = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_date_planned_out_wk = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_fk_nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_tolerance_in_days = models.IntegerField(blank=True, null=True)
    prep_date_planned_tolerance = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_date_changed_by_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_who = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_when = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_is_done = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_code_four = models.CharField(max_length=10, blank=True, null=True)
    prep_assigned_days = models.BigIntegerField(blank=True, null=True)
    prep_assigned_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_assigned_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_assigned_duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_n_imma = models.TextField(blank=True, null=True)  # This field type is a guess.
    prep_generic = models.IntegerField(blank=True, null=True)
    prep_generic_seq = models.IntegerField(blank=True, null=True)
    prep_n_lieu = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prev_eqp_planned'


class Prevent2(Model):
    nu_prevent = models.TextField(primary_key=True)  # This field type is a guess.
    nature = models.TextField(blank=True, null=True)  # This field type is a guess.
    titre = models.TextField(blank=True, null=True)  # This field type is a guess.
    periode = models.CharField(max_length=1, blank=True, null=True)
    datedeb = models.CharField(max_length=10, blank=True, null=True)
    heuredeb = models.CharField(max_length=8, blank=True, null=True)
    datefin = models.CharField(max_length=10, blank=True, null=True)
    heurefin = models.CharField(max_length=8, blank=True, null=True)
    dateorig = models.CharField(max_length=10, blank=True, null=True)
    datesaisi = models.CharField(max_length=10, blank=True, null=True)
    comporig = models.IntegerField(blank=True, null=True)
    compsaisi = models.IntegerField(blank=True, null=True)
    periodela = models.IntegerField(blank=True, null=True)
    periocomp = models.IntegerField(blank=True, null=True)
    int_ext = models.CharField(max_length=1, blank=True, null=True)
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    nom_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_nom = models.CharField(max_length=1, blank=True, null=True)
    statue = models.CharField(max_length=1, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    tolerance = models.IntegerField(blank=True, null=True)
    estimated_duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodicity_occurrence = models.IntegerField(blank=True, null=True)
    periodicity_dmy = models.IntegerField(blank=True, null=True)
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    tools = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_convert_wo = models.IntegerField(blank=True, null=True)
    auto_print_out = models.IntegerField(blank=True, null=True)
    docs_print_out = models.IntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    tolerance_dmy = models.IntegerField(blank=True, null=True)
    alerte = models.IntegerField(blank=True, null=True)
    alerte_dmy = models.IntegerField(blank=True, null=True)
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    pm_cadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    tolerance_days = models.IntegerField(blank=True, null=True)
    auto_convert_wo_days = models.IntegerField(blank=True, null=True)
    id_usertable1_pm = models.BigIntegerField(blank=True, null=True)
    id_usertable2_pm = models.BigIntegerField(blank=True, null=True)
    id_usertable3_pm = models.BigIntegerField(blank=True, null=True)
    already_converted = models.IntegerField(blank=True, null=True)
    is_caller_notified = models.IntegerField(blank=True, null=True)
    is_techn_notified = models.IntegerField(blank=True, null=True)
    wo_status_conversion = models.IntegerField(blank=True, null=True)
    lock_quick_conversion = models.CharField(max_length=1, blank=True, null=True)
    is_service_provider_notified = models.IntegerField(blank=True, null=True)
    call_status = models.IntegerField(blank=True, null=True)
    is_exclude_weekend = models.IntegerField(blank=True, null=True)
    planned_occurrence = models.IntegerField(blank=True, null=True)
    planned_occurrence_dmy = models.IntegerField(blank=True, null=True)
    date_occurrence_end_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_next_pm_after_wo = models.IntegerField(blank=True, null=True)
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'prevent2'


class Prevent2Bkp105(Model):
    nu_prevent = models.TextField(blank=True, null=True)  # This field type is a guess.
    nature = models.TextField(blank=True, null=True)  # This field type is a guess.
    titre = models.TextField(blank=True, null=True)  # This field type is a guess.
    periode = models.CharField(max_length=1, blank=True, null=True)
    datedeb = models.CharField(max_length=10, blank=True, null=True)
    heuredeb = models.CharField(max_length=8, blank=True, null=True)
    datefin = models.CharField(max_length=10, blank=True, null=True)
    heurefin = models.CharField(max_length=8, blank=True, null=True)
    dateorig = models.CharField(max_length=10, blank=True, null=True)
    datesaisi = models.CharField(max_length=10, blank=True, null=True)
    comporig = models.IntegerField(blank=True, null=True)
    compsaisi = models.IntegerField(blank=True, null=True)
    periodela = models.IntegerField(blank=True, null=True)
    periocomp = models.IntegerField(blank=True, null=True)
    int_ext = models.CharField(max_length=1, blank=True, null=True)
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    nom_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn_four = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    observ = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_prev = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_nom = models.CharField(max_length=1, blank=True, null=True)
    statue = models.CharField(max_length=1, blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    tolerance = models.IntegerField(blank=True, null=True)
    estimated_duration = models.TextField(blank=True, null=True)  # This field type is a guess.
    periodicity_occurrence = models.IntegerField(blank=True, null=True)
    periodicity_dmy = models.IntegerField(blank=True, null=True)
    ri_suivi_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    ri_suivi_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    tools = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_convert_wo = models.IntegerField(blank=True, null=True)
    auto_print_out = models.IntegerField(blank=True, null=True)
    docs_print_out = models.IntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    tolerance_dmy = models.IntegerField(blank=True, null=True)
    alerte = models.IntegerField(blank=True, null=True)
    alerte_dmy = models.IntegerField(blank=True, null=True)
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    pm_cadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    tolerance_days = models.IntegerField(blank=True, null=True)
    auto_convert_wo_days = models.IntegerField(blank=True, null=True)
    id_usertable1_pm = models.BigIntegerField(blank=True, null=True)
    id_usertable2_pm = models.BigIntegerField(blank=True, null=True)
    id_usertable3_pm = models.BigIntegerField(blank=True, null=True)
    already_converted = models.IntegerField(blank=True, null=True)
    is_caller_notified = models.IntegerField(blank=True, null=True)
    is_techn_notified = models.IntegerField(blank=True, null=True)
    wo_status_conversion = models.IntegerField(blank=True, null=True)
    lock_quick_conversion = models.CharField(max_length=1, blank=True, null=True)
    is_service_provider_notified = models.IntegerField(blank=True, null=True)
    call_status = models.IntegerField(blank=True, null=True)
    is_exclude_weekend = models.IntegerField(blank=True, null=True)
    planned_occurrence = models.IntegerField(blank=True, null=True)
    planned_occurrence_dmy = models.IntegerField(blank=True, null=True)
    date_occurrence_end_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_next_pm_after_wo = models.IntegerField(blank=True, null=True)
    auto_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'prevent2_bkp_105'


class Preventif(Model):
    num_prev = models.CharField(max_length=10, blank=True, null=True)
    date_prev = models.CharField(max_length=10, blank=True, null=True)
    user_connected = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'preventif'


class PrimarykeyChanges(Model):
    pkchange_id = models.BigIntegerField(primary_key=True)
    pkchange_update_datetime = models.TextField(unique=True)  # This field type is a guess.
    pkchange_table_name = models.TextField(unique=True)  # This field type is a guess.
    pkchange_column_name = models.TextField(unique=True)  # This field type is a guess.
    pkchange_old_value = models.TextField(unique=True)  # This field type is a guess.
    pkchange_new_value = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'primarykey_changes'


class PrioritizationAge(Model):
    range = models.TextField(primary_key=True)  # This field type is a guess.
    value1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    criteria_value = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prioritization_age'


class PrioritizationAssetValues(Model):
    n_imma = models.TextField(primary_key=True)  # This field type is a guess.
    value_formula1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula6 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prioritization_asset_values'


class PrioritizationFormula(Model):
    formula_code = models.TextField(primary_key=True)  # This field type is a guess.
    formula_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula_is_active = models.CharField(unique=True, max_length=1)

    class Meta:
        managed = False
        db_table = 'prioritization_formula'


class PrioritizationPmValues(Model):
    prev_eqp_pk = models.BigIntegerField(primary_key=True)
    value_formula1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula6 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prioritization_pm_values'


class PrioritizationPrice(Model):
    range = models.TextField(primary_key=True)  # This field type is a guess.
    value1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    criteria_value = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prioritization_price'


class PrioritizationUserTable(Model):
    user_table_type = models.TextField(primary_key=True)  # This field type is a guess.
    user_table_name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prioritization_user_table'


class PrioritizationWoValues(Model):
    nu_int = models.TextField(primary_key=True)  # This field type is a guess.
    value_formula1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    value_formula6 = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula1_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula2_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula3_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula4_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula5_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula6_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    formula6 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'prioritization_wo_values'


class Profes(Model):
    id_profes = models.BigIntegerField(primary_key=True)
    pocode = models.TextField(blank=True, null=True)  # This field type is a guess.
    ponom = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'profes'


class Profile(Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    fk_dashboard_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'


class Properties(Model):
    id_property = models.BigIntegerField(primary_key=True)
    code_label = models.TextField(unique=True)  # This field type is a guess.
    id_device_type = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'properties'
        unique_together = (('id_property', 'code_label'),)


class PropertyFieldSetting(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    fk_pgs_auto_id = models.BigIntegerField(unique=True)
    pfs_code = models.TextField(unique=True)  # This field type is a guess.
    pfs_name = models.TextField(unique=True)  # This field type is a guess.
    pfs_type = models.TextField(unique=True)  # This field type is a guess.
    pfs_enable_deseable = models.NullBooleanField()
    string_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    numeric_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    pfs_fk_vocation = models.TextField(blank=True, null=True)  # This field type is a guess.
    pfs_is_date_nowday = models.NullBooleanField()
    fk_pvs_auto_id = models.BigIntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'property_field_setting'


class PropertyGroupSetting(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    pgs_code = models.TextField(unique=True)  # This field type is a guess.
    pgs_name = models.TextField(unique=True)  # This field type is a guess.
    pgs_fk_vocation = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'property_group_setting'


class PropertyValueSetting(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    pvs_value = models.TextField(unique=True)  # This field type is a guess.
    pvs_category = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'property_value_setting'


class Proven(Model):
    pv_nom = models.TextField(primary_key=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'proven'


class PublicTenderCode(Model):
    code_mpu = models.TextField(primary_key=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    commentaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_reform = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'public_tender_code'


class PublicTenderContract(Model):
    n_marche_publique = models.TextField(primary_key=True)  # This field type is a guess.
    designation = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    montant_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    actif_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    commentaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'public_tender_contract'
        unique_together = (('n_marche_publique', 'code_four'),)


class PurchaseRequestLines(Model):
    no_line = models.IntegerField(primary_key=True)
    no_request = models.TextField()  # This field type is a guess.
    code_supp_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_supp_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_dest_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_dest_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    model = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity_stock = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity_requested = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity_received = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity_remaining = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_unit = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    rate_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_without_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_include_vat = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_public_market = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_internal = models.TextField(blank=True, null=True)  # This field type is a guess.
    c_refer = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'purchase_request_lines'
        unique_together = (('no_line', 'no_request'),)


class PurchaseRequests(Model):
    no_request = models.TextField(primary_key=True)  # This field type is a guess.
    date_creation = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_sent = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_estimated_delivery = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    code_supp_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_supp_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_supp_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_supp_store_resp = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_dest_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_dest_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_dest_store = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_dest_store_resp = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_requester = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_requester = models.IntegerField(blank=True, null=True)
    code_med_dept = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_med_dept = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_med_dept_resp = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_med_dept = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    purchase_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    priority = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.
    year_budget = models.TextField(blank=True, null=True)  # This field type is a guess.
    account_budget = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_requester_technician = models.TextField(blank=True, null=True)  # This field type is a guess.
    name_requester_technician = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    corps_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    hidden_no_request = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_requester = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'purchase_requests'


class RdsUserConnection(Model):
    ip_address = models.TextField(primary_key=True)  # This field type is a guess.
    computer_name = models.TextField(unique=True)  # This field type is a guess.
    domain_name = models.TextField(unique=True)  # This field type is a guess.
    nt_user_name = models.TextField(unique=True)  # This field type is a guess.
    last_connection_date = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'rds_user_connection'
        unique_together = (('ip_address', 'computer_name', 'domain_name', 'nt_user_name'),)


class Remedes(Model):
    num = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_type_option = models.NullBooleanField()
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'remedes'


class ReportTemplate(Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    theme = models.TextField(blank=True, null=True)  # This field type is a guess.
    available_view = models.TextField(blank=True, null=True)  # This field type is a guess.
    content = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_profile_id = models.BigIntegerField(blank=True, null=True)
    fk_user_id = models.BigIntegerField(blank=True, null=True)
    report_type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'report_template'


class RfidLog(Model):
    rfid_log_id = models.TextField(primary_key=True)  # This field type is a guess.
    rfid_log_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    rfid_log_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    rfid_log_category = models.TextField(blank=True, null=True)  # This field type is a guess.
    rfid_log_error_level = models.TextField(blank=True, null=True)  # This field type is a guess.
    rfid_log_error_key = models.TextField(blank=True, null=True)  # This field type is a guess.
    rfid_log_error_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    rfid_log_error_msg = models.TextField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'rfid_log'


class RightManagement(Model):
    fk_profile_id = models.BigIntegerField(primary_key=True)
    fk_feature_id = models.BigIntegerField(unique=True)
    access_right = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'right_management'
        unique_together = (('fk_profile_id', 'fk_feature_id'),)


class SchemaVersion(Model):
    schema_version = models.TextField(primary_key=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'schema_version'


class ScriptResults(Model):
    line_id = models.BigIntegerField(primary_key=True)
    script_version = models.TextField(blank=True, null=True)  # This field type is a guess.
    table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_result = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'script_results'


class Services(Model):
    n_servi2 = models.TextField(unique=True)  # This field type is a guess.
    n_chef_s = models.TextField(blank=True, null=True)  # This field type is a guess.
    s_tel1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_etab = models.TextField(unique=True)  # This field type is a guess.
    num_servi = models.TextField(primary_key=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'services'


class Settings(Model):
    stg_global = models.TextField(primary_key=True)  # This field type is a guess.
    stg_fkprofil = models.TextField(blank=True, null=True)  # This field type is a guess.
    stg_fkuser = models.TextField(blank=True, null=True)  # This field type is a guess.
    stg_fklocal = models.TextField(blank=True, null=True)  # This field type is a guess.
    stg_secname = models.TextField(unique=True)  # This field type is a guess.
    stg_kwname = models.TextField(unique=True)  # This field type is a guess.
    stg_kwvalue = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'settings'


class Strfen(Model):
    p_fenetre = models.TextField(primary_key=True)  # This field type is a guess.
    p_nom_chp = models.TextField(unique=True)  # This field type is a guess.
    p_lib_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_type_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_genre_chp = models.TextField(blank=True, null=True)  # This field type is a guess.
    p_num_mnu = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strfen'
        unique_together = (('p_fenetre', 'p_nom_chp'),)


class SupplierHistoricForLink(Model):
    shfl_id = models.BigIntegerField(primary_key=True)
    shfl_date = models.TextField(unique=True)  # This field type is a guess.
    shfl_time = models.TextField(unique=True)  # This field type is a guess.
    shfl_old_supplier_code = models.CharField(max_length=10, blank=True, null=True)
    shfl_new_supplier_code = models.CharField(max_length=10, blank=True, null=True)
    shfl_table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    shfl_pk_fields = models.TextField(blank=True, null=True)  # This field type is a guess.
    shfl_pk_values = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'supplier_historic_for_link'


class SupplierOwnerHistoric(Model):
    soh_id = models.IntegerField(primary_key=True)
    soh_date = models.TextField(unique=True)  # This field type is a guess.
    soh_time = models.TextField(unique=True)  # This field type is a guess.
    soh_supplier_code = models.CharField(unique=True, max_length=10)
    soh_supplier_father_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier_owner_historic'


class SynchAnomaly(Model):
    sa_index = models.BigIntegerField(primary_key=True)
    sah_index = models.BigIntegerField(blank=True, null=True)
    sa_type = models.IntegerField(blank=True, null=True)
    sa_level = models.TextField(blank=True, null=True)  # This field type is a guess.
    sa_source = models.TextField(blank=True, null=True)  # This field type is a guess.
    sa_object = models.TextField(blank=True, null=True)  # This field type is a guess.
    sa_contents = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'synch_anomaly'


class SynchAnomalyHeader(Model):
    sah_index = models.BigIntegerField(primary_key=True)
    u_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    sah_datehour = models.TextField(blank=True, null=True)  # This field type is a guess.
    sah_setting_priority_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    sah_setting_allow_dup_wo = models.IntegerField(blank=True, null=True)
    sah_setting_allow_dup_pm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'synch_anomaly_header'


class TdbDef(Model):
    db_id = models.BigIntegerField(primary_key=True)
    db_type = models.NullBooleanField()
    db_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_titlex = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_titley = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_list_column_title = models.TextField(blank=True, null=True)
    db_list_column_anchor = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_graph_column_title = models.TextField(blank=True, null=True)
    db_graph_column_category = models.TextField(blank=True, null=True)
    db_graph_color_serie = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_explanation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tdb_def'


class TdbDefMandfilter(Model):
    db_id = models.BigIntegerField(primary_key=True)
    db_mand_filter_id = models.BigIntegerField(unique=True)
    db_mand_filter_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_mand_filter_default_type = models.BigIntegerField(blank=True, null=True)
    db_mand_filter_default_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tdb_def_mandfilter'
        unique_together = (('db_id', 'db_mand_filter_id'),)


class TdbDefMandfilterSql(Model):
    db_id = models.BigIntegerField(primary_key=True)
    db_mand_filter_id = models.BigIntegerField(unique=True)
    db_mand_filter_sqltype = models.BooleanField(unique=True)
    db_mand_filter_where = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tdb_def_mandfilter_sql'
        unique_together = (('db_id', 'db_mand_filter_id', 'db_mand_filter_sqltype'),)


class TdbDefOptfilter(Model):
    db_id = models.BigIntegerField(primary_key=True)
    db_opt_filter_id = models.BigIntegerField(unique=True)
    db_opt_filter_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_opt_filter_col_title = models.TextField(blank=True, null=True)
    db_opt_filter_col_list_anchor = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_opt_filter_col_to_select = models.BigIntegerField(blank=True, null=True)
    db_opt_filter_col_notvisible = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_opt_filter_col_linked = models.BigIntegerField(blank=True, null=True)
    db_opt_filter_col_linked_exp = models.TextField(blank=True, null=True)  # This field type is a guess.
    db_opt_filter_linked_to_user = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tdb_def_optfilter'
        unique_together = (('db_id', 'db_opt_filter_id'),)


class TdbDefOptfilterSql(Model):
    db_id = models.BigIntegerField(primary_key=True)
    db_opt_filter_id = models.BigIntegerField(unique=True)
    db_opt_filter_sqltype = models.BooleanField(unique=True)
    db_opt_filter_where = models.TextField(blank=True, null=True)
    db_opt_filter_sql_selec = models.TextField(blank=True, null=True)
    db_opt_filter_sql_selec_where = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tdb_def_optfilter_sql'
        unique_together = (('db_id', 'db_opt_filter_id', 'db_opt_filter_sqltype'),)


class TdbDefSql(Model):
    db_id = models.BigIntegerField(primary_key=True)
    db_sqltype = models.BooleanField(unique=True)
    db_sqlqueryforgraph = models.TextField(blank=True, null=True)
    db_sqlqueryforlist = models.TextField(blank=True, null=True)
    db_filter_organisation = models.TextField(blank=True, null=True)
    db_filter_pole = models.TextField(blank=True, null=True)
    db_filter_site = models.TextField(blank=True, null=True)
    db_filter_md = models.TextField(blank=True, null=True)
    db_filter_contract = models.TextField(blank=True, null=True)
    db_filter_tech_dept = models.TextField(blank=True, null=True)
    db_filter_technician = models.TextField(blank=True, null=True)
    db_filter_vocation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tdb_def_sql'
        unique_together = (('db_id', 'db_sqltype'),)


class TdbValueFilterMandatory(Model):
    db_id = models.BigIntegerField(primary_key=True)
    u_password = models.TextField(unique=True)  # This field type is a guess.
    db_mand_filter_id = models.BigIntegerField(unique=True)
    db_position = models.BooleanField(unique=True)
    db_mand_filter_value = models.BigIntegerField(unique=True)
    db_mand_filter_data = models.BigIntegerField(unique=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tdb_value_filter_mandatory'
        unique_together = (('db_id', 'u_password', 'db_mand_filter_id', 'db_position'),)


class TdbValueFilterOptional(Model):
    db_id = models.BigIntegerField(primary_key=True)
    u_password = models.TextField(unique=True)  # This field type is a guess.
    db_opt_filter_id = models.BigIntegerField(unique=True)
    db_position = models.BooleanField(unique=True)
    db_opt_filter_value = models.TextField(unique=True)
    db_opt_nb_data_selected = models.BigIntegerField(unique=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tdb_value_filter_optional'
        unique_together = (('db_id', 'u_password', 'db_opt_filter_id', 'db_position'),)


class TdbValueProfileAssociation(Model):
    db_id = models.BigIntegerField(primary_key=True)
    u_password = models.TextField(unique=True)  # This field type is a guess.
    db_position = models.BooleanField(unique=True)
    db_title_customised = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tdb_value_profile_association'
        unique_together = (('db_id', 'u_password', 'db_position'),)


class Techfamily(Model):
    code_fam = models.TextField(primary_key=True)  # This field type is a guess.
    nom_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    niveau = models.TextField(blank=True, null=True)  # This field type is a guess.
    branche = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'techfamily'


class TechnicalFieldValues(Model):
    value_index = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    technicalunitname = models.TextField(unique=True)  # This field type is a guess.
    value = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'technical_field_values'


class Territory(Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'territory'


class Theme(Model):
    codecouleur = models.TextField(primary_key=True)  # This field type is a guess.
    element = models.TextField(unique=True)  # This field type is a guess.
    libelle = models.TextField(unique=True)  # This field type is a guess.
    cprimaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    csecondaire = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'theme'


class Tracker(Model):
    item_type = models.CharField(primary_key=True, max_length=1)
    track_item = models.TextField(unique=True)  # This field type is a guess.
    high_response_time = models.IntegerField(blank=True, null=True)
    avg_response_time = models.IntegerField(blank=True, null=True)
    usl_response_time = models.IntegerField(blank=True, null=True)
    usage_count = models.IntegerField(blank=True, null=True)
    pass_count = models.IntegerField(blank=True, null=True)
    throw_count = models.IntegerField(blank=True, null=True)
    error_count = models.IntegerField(blank=True, null=True)
    last_error_msg = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_error_track_item = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_event_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_error_event_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    last_event_timestamp = models.IntegerField(blank=True, null=True)
    last_error_timestamp = models.IntegerField(blank=True, null=True)
    log_mode = models.IntegerField(blank=True, null=True)
    report_mode = models.IntegerField(blank=True, null=True)
    high_response_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracker'
        unique_together = (('item_type', 'track_item'),)


class TrackerLog(Model):
    event_id = models.TextField(primary_key=True)  # This field type is a guess.
    process_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    event_item = models.TextField(blank=True, null=True)  # This field type is a guess.
    item_type = models.CharField(max_length=1, blank=True, null=True)
    process_item = models.TextField(blank=True, null=True)  # This field type is a guess.
    action_level = models.IntegerField(blank=True, null=True)
    error_msg = models.TextField(blank=True, null=True)  # This field type is a guess.
    error_status = models.IntegerField(blank=True, null=True)
    response_time = models.IntegerField(blank=True, null=True)
    begin_timestamp = models.IntegerField(blank=True, null=True)
    end_timestamp = models.IntegerField(blank=True, null=True)
    caller_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tracker_log'


class TrackerProp(Model):
    prop_name = models.TextField(primary_key=True)  # This field type is a guess.
    prop_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    prop_desc = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tracker_prop'


class TrainingHeader(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    code_training = models.TextField(unique=True)  # This field type is a guess.
    title = models.TextField(unique=True)  # This field type is a guess.
    description_training = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_type_training = models.IntegerField(blank=True, null=True)
    issued_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    issued_by_fc = models.TextField(blank=True, null=True)  # This field type is a guess.
    issuer_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    trained_by_supplier = models.CharField(max_length=10, blank=True, null=True)
    trainer_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    expired_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    competency_level = models.IntegerField(blank=True, null=True)
    competency_level_desc = models.TextField(blank=True, null=True)  # This field type is a guess.
    competency_confirmed = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    id_training_parent = models.IntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    start_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    end_time = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'training_header'


class TrainingType(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    description_training_type = models.TextField(unique=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'training_type'


class Tva(Model):
    c_tva = models.CharField(primary_key=True, max_length=1)
    t_tva = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tva'


class TwoHistoric(Model):
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_statut = models.CharField(max_length=20, blank=True, null=True)
    cadre = models.CharField(max_length=1, blank=True, null=True)
    lib_statut = models.TextField(blank=True, null=True)  # This field type is a guess.
    lib_cadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    woh_comment = models.TextField(blank=True, null=True)
    woh_signature_status = models.NullBooleanField()
    woh_signature_digital = models.BinaryField(blank=True, null=True)
    woh_signature_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    woh_signature_login = models.TextField(blank=True, null=True)  # This field type is a guess.
    woh_signature_password = models.TextField(blank=True, null=True)  # This field type is a guess.
    woh_signature_is_override = models.NullBooleanField()
    woh_module = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    wo_forward_by_td = models.TextField(blank=True, null=True)  # This field type is a guess.
    signatory_tracking_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'two_historic'


class TwoHistoricInVenan(Model):
    nu_int = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_ordre = models.IntegerField(blank=True, null=True)
    type_int = models.CharField(max_length=1, blank=True, null=True)
    code_four = models.CharField(max_length=10, blank=True, null=True)
    fourni = models.TextField(blank=True, null=True)  # This field type is a guess.
    techn_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_cm = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_act = models.TextField(blank=True, null=True)  # This field type is a guess.
    woh_module = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_imm = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_mod = models.TextField(blank=True, null=True)  # This field type is a guess.
    marque = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_nom_cneh = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_eqp = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    competency_is_activated = models.NullBooleanField()
    cm_activation_competency = models.NullBooleanField()
    cm_competency_issue = models.NullBooleanField()
    cm_reply_issue = models.NullBooleanField()
    woh_ext_soft_response = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'two_historic_in_venan'


class TwoHistoricLogin(Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    username = models.TextField(unique=True)  # This field type is a guess.
    fk_profile_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.IntegerField(blank=True, null=True)
    pw_update = models.TextField(blank=True, null=True)  # This field type is a guess.
    loginstatus = models.TextField(blank=True, null=True)  # This field type is a guess.
    createdate = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'two_historic_login'


class TwoQuotation(Model):
    id_quotation = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    status_quotation = models.BooleanField(unique=True)
    ref_quotation = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_quotation = models.NullBooleanField()
    amount = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    ref_fourniss = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_contact = models.CharField(max_length=10, blank=True, null=True)
    ref_contact = models.TextField(blank=True, null=True)  # This field type is a guess.
    descript = models.TextField(blank=True, null=True)  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_on = models.TextField(blank=True, null=True)  # This field type is a guess.
    reception_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    expiration_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_by = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    reason = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_change = models.TextField(unique=True)  # This field type is a guess.
    time_change = models.TextField(unique=True)  # This field type is a guess.
    user_change = models.TextField(unique=True)  # This field type is a guess.
    type_change = models.BooleanField(unique=True)
    order_amount = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'two_quotation'


class TypCont(Model):
    code_type = models.CharField(primary_key=True, max_length=10)
    lib_type = models.TextField(unique=True)  # This field type is a guess.
    calcul_ext = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'typ_cont'


class TypeAbs(Model):
    typ_abs = models.CharField(primary_key=True, max_length=2)
    motif = models.TextField(blank=True, null=True)  # This field type is a guess.
    color = models.IntegerField(blank=True, null=True)
    shortcut = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_abs'


class TypeEf(Model):
    ef_typ = models.CharField(primary_key=True, max_length=25)
    famille = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_ef'


class Types(Model):
    tp_type = models.TextField(primary_key=True)  # This field type is a guess.
    marque = models.TextField()  # This field type is a guess.
    four_type = models.CharField(max_length=10, blank=True, null=True)
    cneh_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_ecri = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom2_ecri = models.TextField(blank=True, null=True)  # This field type is a guess.
    para1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    para5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    criticite = models.TextField(blank=True, null=True)  # This field type is a guess.
    classe_eqp = models.TextField(blank=True, null=True)  # This field type is a guess.
    asset_part_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_techfamily_code_fam = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_rfid_tag = models.NullBooleanField()
    remp_prix = models.TextField(blank=True, null=True)  # This field type is a guess.
    typ_obsolescence_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'types'
        unique_together = (('tp_type', 'marque'),)


class UniteSt(Model):
    unit_st = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_techn = models.TextField(primary_key=True)  # This field type is a guess.
    pren_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    tel_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    grade = models.TextField(blank=True, null=True)  # This field type is a guess.
    metier = models.TextField()  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    heures_trav = models.TextField(blank=True, null=True)  # This field type is a guess.
    ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    hr_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    hourly_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    contract_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    cost_hour = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_affichage = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_master_td = models.NullBooleanField()
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'unite_st'
        unique_together = (('nom_techn', 'metier'),)


class UniteStHeader(Model):
    tech_code_techn = models.TextField(primary_key=True)  # This field type is a guess.
    tech_inside_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_hr_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_last_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_first_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_telephone = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_grade = models.TextField(blank=True, null=True)  # This field type is a guess.
    tech_tds = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'unite_st_header'


class Unites(Model):
    n_uf = models.TextField(primary_key=True)  # This field type is a guess.
    n_servi = models.TextField(unique=True)  # This field type is a guess.
    n_servi2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_cent_res = models.TextField(blank=True, null=True)  # This field type is a guess.
    nom_centre = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_plan = models.TextField(unique=True)  # This field type is a guess.
    n_chef_s = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_bati = models.TextField(blank=True, null=True)  # This field type is a guess.
    n_niv = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_l1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_l2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_n1 = models.IntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    ad_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_refor = models.TextField(blank=True, null=True)  # This field type is a guess.
    multi_marc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_activity_pole_id = models.BigIntegerField(blank=True, null=True)
    is_library = models.IntegerField(blank=True, null=True)
    is_digital_sign = models.NullBooleanField()
    riskcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)
    n_lieu_uf = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'unites'


class UrgencyLevel(Model):
    ul_id = models.IntegerField(primary_key=True)
    ul_color = models.IntegerField(unique=True)
    ul_max_response_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'urgency_level'


class UserInterfaceAssociated(Model):
    id_ui_associated_kpi = models.IntegerField(primary_key=True)
    screen_name = models.TextField(unique=True)  # This field type is a guess.
    pk_ui_field_name = models.TextField(unique=True)  # This field type is a guess.
    screen_name_list = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user_interface_associated'


class UserInterfaceList(Model):
    ui_screen_name = models.TextField(primary_key=True)  # This field type is a guess.
    field_name = models.TextField(unique=True)  # This field type is a guess.
    field_type = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user_interface_list'
        unique_together = (('ui_screen_name', 'field_name'),)


class Usershortcuts(Model):
    usershortcuts_username = models.TextField(primary_key=True)  # This field type is a guess.
    usershortcuts_ordre = models.IntegerField(unique=True)
    usershortcuts_type = models.IntegerField(unique=True)
    usershortcuts_description = models.TextField(unique=True)  # This field type is a guess.
    usershortcuts_file = models.TextField(blank=True, null=True)  # This field type is a guess.
    usershortcuts_letter = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usershortcuts'
        unique_together = (('usershortcuts_username', 'usershortcuts_ordre', 'usershortcuts_type', 'usershortcuts_description'),)


class Usertable1(Model):
    id_usertable1 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable1'


class Usertable1Contract(Model):
    id_usertable1 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_contract'


class Usertable1Loan(Model):
    id_usertable1 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_loan'


class Usertable1Location(Model):
    id_usertable1 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_location'


class Usertable1Part(Model):
    id_usertable1 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_part'


class Usertable1PartWo(Model):
    id_usertable1 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_part_wo'


class Usertable1Pm(Model):
    id_usertable1_pm = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_pm'


class Usertable1Po(Model):
    id_usertable1 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_po'


class Usertable1Ri(Model):
    id_usertable1 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_ri'


class Usertable1Tech(Model):
    id_usertable1 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_tech'


class Usertable1Wo(Model):
    id_usertable1_wo = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable1_wo'


class Usertable2(Model):
    id_usertable2 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable2'


class Usertable2Contract(Model):
    id_usertable2 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_contract'


class Usertable2Loan(Model):
    id_usertable2 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_loan'


class Usertable2Location(Model):
    id_usertable2 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_location'


class Usertable2Part(Model):
    id_usertable2 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_part'


class Usertable2PartWo(Model):
    id_usertable2 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_part_wo'


class Usertable2Pm(Model):
    id_usertable2_pm = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_pm'


class Usertable2Po(Model):
    id_usertable2 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_po'


class Usertable2Ri(Model):
    id_usertable2 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_ri'


class Usertable2Tech(Model):
    id_usertable2 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_tech'


class Usertable2Wo(Model):
    id_usertable2_wo = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable2_wo'


class Usertable3(Model):
    id_usertable3 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable3'


class Usertable3Contract(Model):
    id_usertable3 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_contract'


class Usertable3Part(Model):
    id_usertable3 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_part'


class Usertable3PartWo(Model):
    id_usertable3 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_part_wo'


class Usertable3Pm(Model):
    id_usertable3_pm = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_pm'


class Usertable3Po(Model):
    id_usertable3 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_po'


class Usertable3Ri(Model):
    id_usertable3 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_ri'


class Usertable3Tech(Model):
    id_usertable3 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_tech'


class Usertable3Wo(Model):
    id_usertable3_wo = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable3_wo'


class Usertable4(Model):
    id_usertable4 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable4'


class Usertable4Contract(Model):
    id_usertable4 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_contract'


class Usertable4Part(Model):
    id_usertable4 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_part'


class Usertable4PartWo(Model):
    id_usertable4 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_part_wo'


class Usertable4Po(Model):
    id_usertable4 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_po'


class Usertable4Ri(Model):
    id_usertable4 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_ri'


class Usertable4Tech(Model):
    id_usertable4 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_tech'


class Usertable4Wo(Model):
    id_usertable4_wo = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable4_wo'


class Usertable5(Model):
    id_usertable5 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable5'


class Usertable5Contract(Model):
    id_usertable5 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_contract'


class Usertable5Part(Model):
    id_usertable5 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_part'


class Usertable5PartWo(Model):
    id_usertable5 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_part_wo'


class Usertable5Po(Model):
    id_usertable5 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_po'


class Usertable5Ri(Model):
    id_usertable5 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_ri'


class Usertable5Tech(Model):
    id_usertable5 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_tech'


class Usertable5Wo(Model):
    id_usertable5_wo = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable5_wo'


class Usertable6(Model):
    id_usertable6 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable6'


class Usertable6Po(Model):
    id_usertable6 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable6_po'


class Usertable7(Model):
    id_usertable7 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable7'


class Usertable7Po(Model):
    id_usertable7 = models.IntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'usertable7_po'


class Usertable8(Model):
    id_usertable8 = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    field5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'usertable8'


class Utilisat(Model):
    u_password = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_uf = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_marche = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_ens_hosp = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_id = models.TextField(primary_key=True)  # This field type is a guess.
    u_db = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_dbtyp = models.TextField(blank=True, null=True)  # This field type is a guess.
    u_prn = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    ref_plan = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_customer_id = models.BigIntegerField(blank=True, null=True)
    code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    rightclick = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_pole_id = models.BigIntegerField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    pw_limited = models.IntegerField(blank=True, null=True)
    pw_end_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_email = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_buyer_code = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_pw_encrypted = models.CharField(max_length=1, blank=True, null=True)
    use_wifi_network = models.CharField(max_length=1, blank=True, null=True)
    pw_update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    pr_less_greater_amount = models.NullBooleanField()
    pr_approval_amount = models.TextField(blank=True, null=True)  # This field type is a guess.
    int_champrequete = models.TextField(blank=True, null=True)  # This field type is a guess.
    use_quick_debrief_wo = models.TextField(blank=True, null=True)  # This field type is a guess.
    pswd_change_nextcnx = models.NullBooleanField()
    login_attempts = models.BigIntegerField(blank=True, null=True)
    login_locked = models.NullBooleanField()
    uti_secondary_td = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'utilisat'


class Version(Model):
    script_run_on = models.TextField(blank=True, null=True)  # This field type is a guess.
    module_impacted = models.TextField(blank=True, null=True)  # This field type is a guess.
    software_version = models.TextField(blank=True, null=True)  # This field type is a guess.
    script_version = models.TextField(blank=True, null=True)  # This field type is a guess.
    schema_version = models.TextField(blank=True, null=True)  # This field type is a guess.
    descriptions = models.TextField(blank=True, null=True)  # This field type is a guess.
    used_login = models.TextField(blank=True, null=True)  # This field type is a guess.
    result_error = models.TextField(blank=True, null=True)  # This field type is a guess.
    log_file_error = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_comment = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'version'


class Vocfonc(Model):
    voc_fonc = models.TextField(primary_key=True)  # This field type is a guess.
    lib = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    auto_id = models.BigIntegerField(blank=True, null=True)
    technical_id = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'vocfonc'


class WebStats(Model):
    web_stats_name = models.TextField(unique=True)  # This field type is a guess.
    web_stats_count = models.IntegerField(primary_key=True)
    web_stats_min = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_stats_max = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_stats_total = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_stats_access = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_stats_lower = models.IntegerField(blank=True, null=True)
    web_stats_ok = models.IntegerField(blank=True, null=True)
    web_stats_greater = models.IntegerField(blank=True, null=True)
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    web_stats_failure = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_stats'


class WebUser(Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.TextField(blank=True, null=True)  # This field type is a guess.
    password = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_profile_id = models.BigIntegerField(blank=True, null=True)
    fk_metiers_c_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_vocfonc_voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_contrat_n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unite_st_code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    context = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    config = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    calls_filter_by_user = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    pw_update = models.TextField(blank=True, null=True)  # This field type is a guess.
    phone_mobile = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_fourni_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_user'


class WebUserSav20141030(Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.TextField(unique=True)  # This field type is a guess.
    password = models.TextField(unique=True)  # This field type is a guess.
    fk_profile_id = models.BigIntegerField(unique=True)
    fk_metiers_c_metier = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_vocfonc_voc_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_contrat_n_contrat = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_unite_st_code_techn = models.TextField(blank=True, null=True)  # This field type is a guess.
    context = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    config = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler3 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler4 = models.TextField(blank=True, null=True)  # This field type is a guess.
    filler5 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'web_user_sav_20141030'


class WfDomains(Model):
    domain_id = models.TextField(unique=True)  # This field type is a guess.
    domain_label = models.TextField(primary_key=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wf_domains'


class WfItems(Model):
    item_id = models.TextField(primary_key=True)  # This field type is a guess.
    item_label = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wf_items'


class WfLinks(Model):
    item_id = models.TextField(primary_key=True)  # This field type is a guess.
    pre_item = models.TextField(blank=True, null=True)  # This field type is a guess.
    post_item = models.TextField(blank=True, null=True)  # This field type is a guess.
    archived = models.BigIntegerField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)  # This field type is a guess.
    wf_domain = models.TextField(blank=True, null=True)  # This field type is a guess.
    audience = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wf_links'


class WhoDoWhat(Model):
    www_who = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_when = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_mode = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_table_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_query = models.TextField(blank=True, null=True)
    www_pk = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_module = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_where = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_ip = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_host_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_user_login_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_track_changes = models.TextField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'who_do_what'


class Wksserver(Model):
    wks_id = models.TextField(primary_key=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wksserver'


class WoQuotation(Model):
    id_quotation = models.BigIntegerField(primary_key=True)
    nu_int = models.TextField(unique=True)  # This field type is a guess.
    status_quotation = models.BooleanField(unique=True)
    ref_quotation = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_quotation = models.NullBooleanField()
    amount = models.TextField(blank=True, null=True)  # This field type is a guess.
    code_four = models.CharField(max_length=10, blank=True, null=True)
    ref_fourniss = models.TextField(blank=True, null=True)  # This field type is a guess.
    nu_contact = models.CharField(max_length=10, blank=True, null=True)
    ref_contact = models.TextField(blank=True, null=True)  # This field type is a guess.
    descript = models.TextField(blank=True, null=True)  # This field type is a guess.
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.
    request_on = models.TextField(blank=True, null=True)  # This field type is a guess.
    reception_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    expiration_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_by = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    reason = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    order_amount = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wo_quotation'


class WoSubStatus(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    wo_status_option = models.NullBooleanField()
    sub_status_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wo_sub_status'


class WoSubType(Model):
    auto_id = models.BigIntegerField(primary_key=True)
    wo_type_option = models.NullBooleanField()
    sub_type_description = models.TextField(blank=True, null=True)  # This field type is a guess.
    v_fonc = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wo_sub_type'


class WoTester(Model):
    wot_id = models.IntegerField(primary_key=True)
    wot_wo_number = models.TextField(unique=True)  # This field type is a guess.
    wot_assetnumber = models.TextField(unique=True)  # This field type is a guess.
    wot_usage_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    wot_usage_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    wot_tech_dept = models.TextField(blank=True, null=True)  # This field type is a guess.
    wot_technician = models.TextField(blank=True, null=True)  # This field type is a guess.
    wot_code_four = models.CharField(max_length=10, blank=True, null=True)
    wot_external_tech = models.TextField(blank=True, null=True)  # This field type is a guess.
    insert_date = models.TextField(blank=True, null=True)  # This field type is a guess.
    update_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wo_tester'


class WwwOnLocation(Model):
    www_who = models.TextField(primary_key=True)  # This field type is a guess.
    www_when = models.TextField(unique=True)  # This field type is a guess.
    www_mode = models.TextField(unique=True)  # This field type is a guess.
    www_table_name = models.TextField(unique=True)  # This field type is a guess.
    www_query = models.TextField(blank=True, null=True)
    www_pk = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_module = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_where = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_ip = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_host_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_user_login_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_comment = models.TextField(blank=True, null=True)  # This field type is a guess.
    www_track_changes = models.TextField(blank=True, null=True)
    filler1 = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'www_on_location'
