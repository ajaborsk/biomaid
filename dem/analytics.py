from django.db.models import Q
from django.utils.timezone import now

from analytics.apps import AnalyticsEngine
from common import config


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
