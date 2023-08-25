from django.db.models import (
    JSONField,
    DateTimeField,
    CharField,
    TextField,
    ForeignKey,
    PROTECT,
    UniqueConstraint,
)
from django.utils.translation import gettext as _

from overoly.base import OverolyModel as Model


class DataSource(Model):
    class Meta:
        constraints = [UniqueConstraint(name='data_source_code_is_unique', fields=['code'])]

    code = CharField(max_length=256, verbose_name=_("code de la source de données"))
    label = CharField(max_length=1024, verbose_name=_("nom de la source de données"))
    auto = JSONField(
        verbose_name=_("Calcul automatique"),
        help_text=_(
            "Calcule la donnée dès que toutes les dépendances sont disponibles."
            " Liste des jeux de paramètres à calculer automatiquement."
        ),
        default=list,
    )
    inputs = JSONField(
        null=True,
        blank=True,
        verbose_name=_("Données d'entrée"),
        help_text=_(
            "Dictionnaire JSON qui donne les données d'entrée de la DataSource."
            " Utilisées dans le calcul des dépendances et comme entrées du moteur."
        ),
    )
    processor_name = CharField(
        max_length=1024,
        verbose_name=_("nom du processeur de données"),
        null=True,
        blank=True,
    )
    description = TextField(
        null=True,
        blank=True,
        verbose_name=_("description longue de la source de données"),
    )
    definition = JSONField(
        null=True,
        blank=True,
        verbose_name=_("définition de la source et notamment méthode de calcul"),
    )
    parameters = JSONField(null=True, blank=True, verbose_name=_("paramètres possibles (avec définitions)"))
    schedule = JSONField(null=True, blank=True, verbose_name=_("programmation temporelle"))
    storage_policy = JSONField(null=True, blank=True, verbose_name=_("politique de stockage/archivage"))
    date_creation = DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = DateTimeField(auto_now=True, verbose_name=_("date de modification"))
    cloture = DateTimeField(verbose_name=_("date de clôture"), null=True, blank=True)

    def __str__(self):
        return f'Datasource {self.code}: {self.label}'


class Data(Model):
    class Meta:
        pass

    source = ForeignKey(DataSource, on_delete=PROTECT)
    parameters = JSONField(
        null=True,
        blank=True,
        verbose_name=_("valeurs des paramètres utilisés pour calculer ces données"),
    )
    timestamp = DateTimeField(verbose_name=_("date de référence des données (à laquelle les calculs se réfèrent)"))
    link = JSONField(
        null=True,
        blank=True,
        verbose_name=_("lien vers la page expliquant ces données analytiques"),
    )
    data = JSONField(null=True, blank=True, verbose_name=_("données analytiques"))
    context = JSONField(null=True, blank=True, verbose_name=_("informations sur le contextes du calcul"))
    date_creation = DateTimeField(auto_now_add=True, verbose_name=_("date de création"))
    date_modification = DateTimeField(auto_now=True, verbose_name=_("date de modification"))
