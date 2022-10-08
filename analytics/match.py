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
Ensemble de classes et de fonction pour faire de l'appairage, généralement entre deux listes d'enregistrements.

Le principe est de fournir à un objet, le 'RecordMatcher', deux listes et cet objet tente de rapprocher ces deux listes
 (c'est à dire trouver des correpondances entre les enregistrements de chaque liste),
 en se basant sur un certain nombre de critères.

Exemples :
- Fiches d'immobilisation et fiches d'inventaire Asset+
- Commandes et factures
- Lignes de commande et interventions Asset+

Idées :
- Sorties possibles :
    - Liste appairée 'dure' (1 record <--> 1 record) = best match
    - Liste appairée 'soft' (1 record <--> 1 liste de records) = best matches
    - Listes des records non appairés (de l'une et l'autre listes)
- Fonction de calcul de distance globale (différentes façons d'aggréger les distances pondérées de chaque critère) :
    manhattan, euclidienne, max... ==> Non, ce n'est pas une distance !!
- Valeur cut-off : A partir d'une certaine distance, considérer que l'appairage a échoué
- Fonction d'apprentissage :
    - Calcul des meilleurs poids de critères, de la distance, du cut-off...
    - Soit à partir de listes de référence
    - Soit uniquement pour les critères 'mous' (dates, montant, ...) à partir d'un appairage (éventuellement partiel) réalisé par
       les critères 'durs' (n° d'enregistrement coincidants...)
- Détection des anomalies : trouver les enregistrements/critères pour lesquel on a bon 'match' global mais pour lesquel ces critères
    devient significativement de la distance moyenne pour ce critère en cas de 'match'
    (exemple : Détecter une date farfelue liée à une faute de frappe)
- Voir s'il est possible d'avoir un processus en 'batch' pour les grandes listes car le calcul peut être long...

"""
from functools import partial
from math import fabs

from django.apps import apps
from django.db.models import Model, Q
from django.utils.translation import gettext as _


class RecordFetcher:
    """
    Class to get record from one or more models.
    Very similar to Queryset but can also get record with built keys and/or union of models
    Try to get as much fields as possible.
    """

    def __init__(self, models, using=None, key_builder=None):
        self.using = using or 'default'

        # self.key_builder = key_builder
        if isinstance(key_builder, str):
            # The key is a single field name
            self.key_filter = partial(self.simple_key_filter, key_builder)
        elif callable(key_builder):
            self.key_filter = key_builder

        if isinstance(models, list) or isinstance(models, tuple):
            models = list(models)
        else:
            models = [models]

        self.models = []
        self.fieldnames = None
        for model_ref in models:
            if isinstance(model_ref, Model):
                model = model_ref
            elif isinstance(model_ref, str):
                model = apps.get_model(*model_ref.split('.', maxsplit=1))
            else:
                raise ValueError(_("Unexpected value for model reference: {}").format(repr(model_ref)))

            self.models.append(model)
            if self.fieldnames is None:
                self.fieldnames = set(f.attname for f in model._meta.get_fields())
            else:
                self.fieldnames = self.fieldnames.intersection(set(f.attname for f in model._meta.get_fields()))

        print(self.fieldnames)

        self.qs = []

    @staticmethod
    def simple_key_filter(fieldname, key):
        return Q(**{fieldname: key})

    def get(self, key):
        results = []
        for model in self.models:
            qs = model.objects.using(self.using).filter(self.key_filter(key)).values(*list(self.fieldnames))
            qs._fetch_all()
            results += list(qs)
        if len(results) == 1:
            return results[0]
        else:
            raise ValueError(
                _("RecordFetch.get(key={}) returns {} records (should returns exactly ONE record)").format(key, len(results))
            )

    def get_candidates(self, *args, **kwargs):
        pass


# -----------------------------------------------------------------------------------------------------------------------------------


class Criterion:
    def __init__(self, left_field, right_field):
        self.left_field = left_field
        self.right_field = right_field

    def __call__(self, left, right):
        return 0.0


class Equal(Criterion):
    def __call__(self, left, right):
        return 1.0 if left[self.left_field] == right[self.right_field] else 0.0


class Contains(Criterion):
    def __call__(self, left, right):
        return 1.0 if right[self.right_field] in left[self.left_field] else 0.0


class IsContained(Criterion):
    def __call__(self, left, right):
        return 1.0 if left[self.left_field] in right[self.right_field] else 0.0


class FloatDifference(Criterion):
    def __call__(self, left, right):
        return fabs(left[self.left_field] - right[self.right_field])


class DateDayDifference(Criterion):
    def __call__(self, left, right):
        return abs((left[self.left_field] - right[self.right_field]).days)


class RecordMatcher:
    criteria = tuple()
    cutoff_value = 0.0

    def __init__(self, left: dict = None, right: dict = None, **options):
        self.left: dict = left or {}
        self.right: dict = right or {}
        self.options: dict = options or {}
        self.match_done = False
        self.batch_size = None  # Unused
        self.left_matches = {}
        self.left_unmatched = []
        self.right_matches = {}
        self.right_unmatched = []
        self.weights, self.criteria_obj = zip(*self.criteria)

    def records_distance(self, left: dict, right: dict) -> float:
        coords = []
        for i in range(len(self.criteria_obj)):
            coords.append(self.weights[i] * self.criteria_obj[i](left, right))
        return sum(coords) / sum(self.weights)

    def do_match(self):
        for l_k, l_v in self.left.items():
            self.left_matches[l_k] = []
            for r_k, r_v in self.right.items():
                self.right_matches[r_k] = self.right_matches.get(r_k, [])
                strength = self.records_distance(l_v, r_v)
                if strength > self.cutoff_value:
                    self.left_matches[l_k].append((r_k, strength))
                    self.right_matches[r_k].append((l_k, strength))
            if len(self.left_matches[l_k]):
                self.left_matches[l_k].sort(key=lambda a: -a[1])
            else:
                del self.left_matches[l_k]
        for r_k in self.right.keys():
            if len(self.right_matches[r_k]):
                self.right_matches[r_k].sort(key=lambda a: -a[1])
            else:
                del self.right_matches[r_k]
        self.left_unmatched = list(set(self.left.keys()) - set(self.left_matches.keys()))
        self.right_unmatched = list(set(self.right.keys()) - set(self.right_matches.keys()))
        self.match_done = True

    def get_all_results(self):
        if not self.match_done:
            self.do_match()
        return (
            self.left_matches,
            self.left_unmatched,
            self.right_matches,
            self.right_unmatched,
        )


# -----------------------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------------
