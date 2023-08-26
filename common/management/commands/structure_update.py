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
import datetime

import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Count

from django.conf import settings
from common.models import (
    ExtensionUser,
    Uf,
    UserUfRole,
    Pole,
    Service,
    CentreResponsabilite,
    Site,
    Etablissement,
)
from common.db_utils import get_uf_list


# TODO: Reste à faire :
#  - rouvrir une UF qui avait été fermée
#  - fermer les structures dont toutes les UF sont fermées (est-ce vraiment utile ?)
#  - Faire plus de retour sur ce qui est effectivement fait dans la base (comptages, modifications...)
#  - Gérer des configurations d'import pour chaque fichier structure

# Ces constantes devraient sans doute être à part, dans un dossier qui regroupe tout ce qui concerne notre portail GÉQIP
# (et non l'application générale)
CHUAP_FILE_STRUCTURE = {
    'format': 'excel',
    # 'sheet': '',
    'fields': {
        'code_uf': {'column': 'Code UF'},
        'nom_uf': {'column': 'Libellé long uf'},
        'debut_uf': {'column': 'Date début UF'},
        'fin_uf': {'column': 'Date fin UF'},
        'lettre_budget': {'column': 'Lettre Budgétaire'},
        'code_service': {'column': 'Code Service'},
        'nom_service': {'column': 'Libellé long service'},
        'code_centre_responsabilite': {'column': 'Code CR'},
        'nom_centre_responsabilite': {'column': 'Libellé long CR'},
        'code_pole': {'column': 'Code Pôle'},
        'nom_pole': {'column': 'Libellé long Pôle'},
        'code_site': {'column': 'Code EG'},
        'nom_site': {'column': 'Libellé long EG'},
    },
}

CHIMR_FILE_STRUCTURE = {
    'format': 'excel',
    'fields': {
        'code_uf': {'column': 'UF'},
        'nom_uf': {'column': "libéllé d'UF"},
        'debut_uf': {'constant': datetime.datetime(2018, 1, 1, tzinfo=timezone.pytz.timezone(settings.TIME_ZONE))},
        'fin_uf': {'constant': datetime.datetime(2118, 1, 1, tzinfo=timezone.pytz.timezone(settings.TIME_ZONE))},
        'lettre_budget': {'column': 'budget'},
        'code_service': {'column': 'CR'},
        'nom_service': {'column': 'libéllé des centres de responsabilité'},
        'code_centre_responsabilite': {'column': 'CR'},
        'nom_centre_responsabilite': {'column': 'libéllé des centres de responsabilité'},
        'code_pole': {'column': 'pole'},
        'nom_pole': {'column': "libéllé de pole d'activité"},
        'code_site': {'constant': 1},
        'nom_site': {'constant': 'Montdidier'},
    },
}


STRUCTURE_LEVELS = {
    'site': Site,
    'pole': Pole,
    'centre_responsabilite': CentreResponsabilite,
    'service': Service,
}


class Command(BaseCommand):
    help = _("Mise à jour de la structure d'un établissement")

    def add_arguments(self, parser):
        parser.add_argument('code_etablissement', type=int)
        parser.add_argument('filename', type=str)

    def format_guess(self, filename):
        """Version très basique de divination du format..."""
        if 'CHIMR' in filename:
            return CHIMR_FILE_STRUCTURE
        else:
            return CHUAP_FILE_STRUCTURE

    def file_read(self, filename, **kwargs):
        """Lit un fichier structure "filenename"
        et renvoie une liste de dict avec les clés 'code_'+level et 'nom_'+level ou level est dans
        ['uf', 'service', 'centre_responsabilite', 'pole', 'site']
        La structure du fichier est donnée par la méthode format_guess()
        """
        file_structure = self.format_guess(filename)
        if file_structure['format'] == 'excel':
            df = pd.read_excel(filename)
            for col in df:
                # Si la colonne est une date/time, la ramener dans l'intervalle que peut comprendre pandas
                #  et la convertir en heure locale (aware vs naive)
                if hasattr(df[col], 'dt'):
                    df[col] = (
                        df[col]
                        .clip(lower=pd.Timestamp.min, upper=pd.Timestamp.max)
                        .dt.tz_localize(tz=timezone.pytz.timezone(settings.TIME_ZONE))
                    )
            uf_list = []
            for index, row in df.iterrows():
                dst_row = {}
                for field, desc in file_structure['fields'].items():
                    if 'column' in desc:
                        value = row[desc['column']]
                    elif 'constant' in desc:
                        value = desc['constant']
                    else:
                        value = None
                    dst_row[field] = value
                uf_list.append(dst_row)
            return uf_list
        else:
            self.stdout.write(
                self.style.ERROR(_("Erreur : ")) + _("Type de fichier structure non supporté : {}").format(file_structure['format'])
            )
            raise CommandError(_("Type de fichier structure non supporté : {}").format(file_structure['format']))

    def structure_update(self, code_etablissement, uf_list):
        today = datetime.datetime.now(tz=timezone.pytz.timezone(settings.TIME_ZONE))
        etablissement = Etablissement.records.get(code=code_etablissement)
        self.stdout.write(_("Mise à jour de la structure de l'établissement : {:s}...").format(str(etablissement)))

        # Etape 1 : On ajoute les structures (hors UF) nécessaires, si besoin

        for level, klass in STRUCTURE_LEVELS.items():
            self.stdout.write(_("  Ajout/mise à jour des structures de niveau : {}...").format(level))
            structures = dict({(uf['code_' + level], uf['nom_' + level]) for uf in uf_list})
            for code, nom in structures.items():
                qs = klass.records.filter(code=etablissement.prefix + "{:04d}".format(code)).union(
                    klass.records.filter(code=etablissement.prefix + "{:d}".format(code))
                )
                if qs.exists():
                    # Bizarrement, la mise à jour directe par qs.update(...)
                    #  ne fonctionne pas du tout (ne fait rien mais ne dit rien)
                    for item in qs:
                        item.code = etablissement.prefix + "{:04d}".format(code)
                        item.nom = nom
                        item.save()
                else:
                    structure = klass(code=etablissement.prefix + "{:04d}".format(code), nom=nom)
                    structure.save()

        # Etape 2 : Ajouter ou mettre à jour les UF (liens vers les structures)

        self.stdout.write(_("  Ajout/mise à jour des Uf..."))
        for uf in uf_list:
            if uf['fin_uf'] and uf['fin_uf'] <= today:
                cloture_uf = uf['fin_uf']
            elif uf['nom_uf'].startswith('XX'):
                cloture_uf = today
            else:
                cloture_uf = None

            qs = (
                Uf.records.filter(code=etablissement.prefix + "{:04d}".format(uf['code_uf']))
                .order_by()
                .union(Uf.records.filter(code=etablissement.prefix + "{:d}".format(uf['code_uf'])).order_by())
            )
            structs = {}
            for level, klass in STRUCTURE_LEVELS.items():
                structs[level] = klass.records.get(code=etablissement.prefix + "{:04d}".format(uf['code_' + level]))
            if qs.exists():
                structs['code'] = etablissement.prefix + "{:04d}".format(uf['code_uf'])
                structs['nom'] = uf['nom_uf']
                structs['etablissement'] = etablissement
                structs['lettre_budget'] = uf['lettre_budget']
                # qs.update(**structs)
                # Bizarrement, la mise à jour directe par qs.update(...) ne fonctionne pas du tout (ne fait rien mais ne dit rien)
                for item in qs:
                    # Si l'UF (qui est toujours dans le fichier structure) n'était pas fermée et qu'elle doit l'être maintenant...
                    if not item.cloture and cloture_uf:
                        item.cloture = cloture_uf
                    # Mise à jour effective
                    for property_name, property_value in structs.items():
                        setattr(item, property_name, property_value)
                    item.save()
            else:
                if not cloture_uf:
                    self.stdout.write(
                        _("    Ajout de l'Uf {} - {}").format(
                            etablissement.prefix + "{:04d}".format(uf['code_uf']),
                            uf['nom_uf'],
                        )
                    )

                # L'UF n'existe pas dans la base
                # Etape 2.1 : déterminer les droits à partir des autres UF qui sont dans les mêmes structures
                roles = set()
                if not cloture_uf:
                    for level, klass in STRUCTURE_LEVELS.items():
                        structure = klass.records.get(code='{}{:04d}'.format(etablissement.prefix, uf['code_' + level]))
                        ufs = get_uf_list(structure)
                        responsabilites = (
                            UserUfRole.records.select_related('extension_user')
                            .filter(uf__in=ufs, uf__cloture__isnull=True)
                            .values('role_code', 'extension_user')
                            .annotate(c=Count('uf'))
                            .filter(c=len(ufs))
                        )
                        for responsabilite in responsabilites:
                            role = frozenset(
                                {
                                    'extension_user': ExtensionUser.records.get(id=responsabilite['extension_user']),
                                    'role_code': responsabilite['role_code'],
                                }.items()
                            )
                            roles.add(role)
                    # self.stdout.write(_("      Roles: {}").format(repr(roles)))

                # Etape 2.2 : Ajouter l'UF dans la base
                structs['code'] = etablissement.prefix + "{:04d}".format(uf['code_uf'])
                structs['nom'] = uf['nom_uf']
                structs['etablissement'] = etablissement
                structs['lettre_budget'] = uf['lettre_budget']
                if cloture_uf:
                    structs['cloture'] = cloture_uf
                uf_instance = Uf(**structs)
                uf_instance.save()

                # Etape 2.3 : Ajouter à l'UF créée les droits déterminés à l'étape 2.1
                if not cloture_uf:
                    for role in roles:
                        role_instance = UserUfRole(
                            uf=uf_instance,
                            role_code=dict(role)['role_code'],
                            extension_user=dict(role)['extension_user'],
                        )
                        role_instance.save()

        # Etape 3 : Fermer les UF devenues inutiles (si nécessaire)

        self.stdout.write(_("  Fermeture des Uf..."))

        file_uf_codes = set(['{}{:04d}'.format(etablissement.prefix, uf['code_uf']) for uf in uf_list])
        db_uf_list = set(Uf.records.filter(code__regex=r"^" + etablissement.prefix + r"\d+$").values_list('code', flat=True))

        uf_to_close = db_uf_list - file_uf_codes
        for code_uf in uf_to_close:
            db_uf = Uf.records.filter(code=code_uf)
            if db_uf.exists():
                db_uf.update(cloture=today)

        # Etape 4 : Fermer les structures (hors UF) devenues inutiles, si besoin

        # Etape 4.1 : Fermeture des structures qui n'apparaissent plus dans le fichier structure
        for level, klass in STRUCTURE_LEVELS.items():
            self.stdout.write(_("  Fermeture des structures de niveau : {}...").format(level))
            structures = dict({(uf['code_' + level], uf['nom_' + level]) for uf in uf_list})
            # Liste de tous les codes de la base qui ont la forme du préfixe suivi de chiffres ensuite :
            codes = set(klass.records.filter(code__regex=r"^" + etablissement.prefix + r"\d+$").values_list('code', flat=True))
            # codes qui sont dans la base mais pas dans le tableau :
            unused_codes = set(codes) - set({etablissement.prefix + "{:04d}".format(code) for code in structures.keys()})
            klass.records.filter(code__in=list(unused_codes)).update(cloture=today)

        # Etape 4.2 : Fermeture des structures dont toutes les UF sont fermées
        # TODO
        pass

        self.stdout.write(_("Mise à jour de la structure de l'établissement {:s} terminée").format(str(etablissement)))

    def handle(self, *args, **options):
        self.stdout.write(
            _("Mise à jour structure établissement code={} avec le fichier {}...").format(
                options['code_etablissement'], options['filename']
            )
        )

        uf_list = self.file_read(options['filename'])
        if uf_list:
            self.structure_update(options['code_etablissement'], uf_list)
