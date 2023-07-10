from django.db.models import Q
from django.utils.timezone import now
from pandas import DataFrame, Int32Dtype, StringDtype

from analytics.apps import AnalyticsEngine
from common import config


class DemandesFullStatus(AnalyticsEngine):
    """
    Un moteur analytics primordial (sans data en entrée) qui donne, pour un utilisateur donné, une vision globale des demandes qui le concernent :

    Il retourne deux tableaux à deux dimensions (deux DataFrame pandas) de structures identiques :

    **Lignes :**

    - Les demandes dont je suis le rédacteur
    - Les demandes dans mon secteur fonctionnel (sur les UF pour lesquelles je peux faire une demande)
    - Les demandes pour lesquelles je suis cadre supérieur : demandes sur lesquelles j'ai (eu) un avis à donner
    - Les demandes pour lesquelles je suis directeur / chef de pôle : demandes que je peux approuver / que j'ai approuvé
    - Les demandes pour lesquelle je suis dispatcher
    - Les demandes pour lesquelles je suis expert
    - Les demandes pour lesquelles je suis arbitre

    **Colonnes:**

    - Demandes en cours (total)
    - Demandes à évaluer (avis CS à donner)
    - Demande à approuver
    - Demandes à dispatcher
    - Demandes à expertiser
    - Demandes 'refusables' : Qui peuvent être refusées
    - Demandes 'validables' : Qui peuvent être acceptées
    - Demandes à arbitrer (en attente d'arbitrage)
    - Demandes arbitrées mais non définitives

    **Retour :**

    Deux tableaux avec des données de natures différentes
    - `nb` : Nombre de demandes pour chaque cas
    - `filter` : filtre (chaîne JSON) à utiliser pour aller sur les demandes concernées

    **Paramètres du moteur :**

    - L'id de utilisateur concerné (-1, valeur par défaut, pour tous les utilisateurs)
    - L'id de la campagne concernée (-1, valeur par défaut, pour toutes les campagnes)
    - L'id du programme concerné (-1, valeur par défaut, pour tous les programmes)
    """

    def __init__(self, *args, user_id=-1, campaign_id=-1, program_id=-1):
        super().__init__()
        self.user_id = user_id
        self.campaign_id = campaign_id
        self.program_id = program_id
        # Initializing output values (even to None) is not an option !
        self._values = {'count': None, 'filters': None}

    def run(self):
        columns_filters = {}
        rows_filters = {}
        for cf in columns_filters.keys():
            for rf in rows_filters.keys():
                pass
        self._values['count'] = DataFrame(dtype=Int32Dtype())
        self._values['filters'] = DataFrame(dtype=StringDtype())


class DemandesADispatcher(AnalyticsEngine):
    def __init__(self, *args, user=-1, requester=-1, dispatcher=-1, the_campaign=-1):
        super().__init__()
        # General user : all requests on UF this user can make demand for are accounted
        self.user = user
        # Requester : Account only for resquests this user wrote
        self.requester = requester
        # Campaign : Accout only requests in that campaign
        self.campaign = the_campaign
        # Dispatcher : Account only requests this user has to dispatch
        self.dispatcher = dispatcher
        self._values = {'count': None, 'requests': None}

    def run(self, verbosity=0):
        from common.models import UserUfRole
        from dem.models import Demande

        q_filters = [Q(gel=False), Q(programme__isnull=True) | Q(domaine__isnull=True) | Q(expert_metier__isnull=True)]
        filters = {}

        if self.user >= 0:
            tmp_scope = UserUfRole.objects.filter(
                user__pk=self.user,
                role_code__in=config.settings.DEM_DEMANDE_CREATION_ROLES,
            )
            q_filters.append(
                Q(uf__in=tmp_scope.values('uf'))
                | Q(uf__service__in=tmp_scope.values('service'))
                | Q(uf__centre_responsabilite__in=tmp_scope.values('centre_responsabilite'))
                | Q(uf__pole__in=tmp_scope.values('pole'))
                | Q(uf__site__in=tmp_scope.values('site'))
                | Q(uf__etablissement__in=tmp_scope.values('etablissement'))
            )
        if self.requester >= 0:
            filters['redacteur__pk'] = self.requester
        if self.campaign >= 0:
            filters['calendrier__pk'] = self.campaign
        if self.dispatcher >= 0:
            filters['calendrier__dispatcher__pk'] = self.dispatcher

        self._last_run_ts = now()
        self._values['requests'] = Demande.objects.filter(*q_filters, **filters)
        self._values['count'] = self._values['requests'].count()

    # @property
    # def requests(self):
    #     self.run()
    #     return self.values['requests']

    # @property
    # def count(self):
    #     self.run()
    #     return self.values['count']
