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
from django.views.generic import TemplateView

import geprete

from django.utils.translation import gettext_lazy as _

# from common.views import BiomAidView
from common.base_views import BiomAidViewMixin
from smart_view.smart_page import SmartPage
from geprete.smart_views import GepreteSmartView, GessayeSmartView


# def geprete_context(request, context={}, **kwargs):
#     """Complète un contexte avec des informations fréquemment utilisées
#
#     Retourne un contexte mis à jour avec :
#     - les titres et les liens des tabs
#     - la date de fin de recensement
#     - phase du recensement ('fini', 'bientot_fini' ou 'en_cours')
#     Cette fonction peut etre appelée avec un contexte existant et/ou des arguments nommés
#     Les éléments de contexte fournis sont prioritaires sur les données calculées par défaut dans cette fonction
#
#     Returns:
#         Le contexte mis à jour
#
#     Todo:
#         Cela pourrait être fait avec un middleware
#     """
#
#     if 'url_prefix' in kwargs and kwargs['url_prefix']:
#         reverse_base = {'url_prefix': kwargs['url_prefix']}
#         context['url_prefix'] = kwargs['url_prefix']
#     else:
#         reverse_base = {}
#
#     """
#     try:
#         datefin = list(Calendrier.objects.all())[-1].fin_recensement
#     except ObjectDoesNotExist:
#         # Fallback qui permet à l'application de ne pas planter, même s'il n'y a aucun calendrier dans la base
#         if request.user.is_staff:
#             datefin = datetime.now(
#                 tz=timezone.pytz.timezone(settings.TIME_ZONE)
#             ) + timedelta(1)
#         else:
#             datefin = datetime(
#                 2000, 2, 29, tzinfo=timezone.pytz.timezone(settings.TIME_ZONE)
#             )
#     """
#
#     tabs = [
#         {'img': 'local/chu-amiens-logo-small.png', "url": reverse('geprete:home', kwargs=reverse_base)},
#         {"label": _("Accueil"), "url": reverse('geprete:home', kwargs=reverse_base)},
#         {
#             "label": _("Gessaye"),
#             "entries": [
#                 {
#                     "url": reverse('geprete:listeessai', kwargs=reverse_base),
#                     "label": _("Liste des essais"),
#                 },
#                 {
#                     "url": reverse('geprete:listeessai-create', kwargs=reverse_base),
#                     "label": _("Formulaire d'essai"),
#                 }
#                 # {"url": reverse('geprete:documentessai-create',
#                 #   kwargs=reverse_base), "label": _("Ajout de document"), }
#                 # {"url": reverse('geprete:evaluationessai-create', kwargs=reverse_base),
#                 #   "label": _("Evaluer un essai"), }
#             ],
#         },
#         # {"label": _("Cockpit"), "url": reverse('drachar:cockpit', kwargs=reverse_base)},
#     ]
#
#     return dict(
#         dict(
#             {
#                 # Mettre debug_mode à False pour tester le fonctionnement en mode normal, comme en production
#                 # Le debug_mode est utilisé par les templates et
#                 # entraîne notamment l'utilisation de bibliothèques js non minifiées
#                 "debug_mode": config.settings.DEBUG,
#                 "tabs": tabs,
#                 "dem_version": config.settings.DEM_VERSION,
#                 "dem_version_date": config.settings.DEM_VERSION_DATE,
#                 "js_data": {"Test": "Données pour JS"},
#                 'can_admin': permissions.can(request.user, "admin", "access"),
#             },
#             **context,
#         ),
#         **kwargs,
#     )


class GepreteView(BiomAidViewMixin, TemplateView):
    application = "geprete"
    permissions = {'EXP', 'ACH', 'DIS', 'ARB', 'ADM'}
    application_title = _('Gestion des prêts')
    views_module = geprete

    def main_tour_steps(self, context):
        return super().main_tour_steps(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs.update({'url_prefix': context.get('url_prefix', None)})
        # context = geprete_context(self.request, context, **kwargs)
        return context


class GepreteHome(GepreteView):
    name = 'home'
    title = _("Accueil")
    permissions = '__LOGIN__'
    template_name = 'AccueilGep.html'


class GessayeV(SmartPage):
    application = 'geprete'
    name = 'listeessai'
    label = _("Gessaye")
    title = _("Gestion des essais")
    permissions = {'EXP', 'ACH', 'DIS', 'ARB', 'ADM'}
    views_module = geprete
    smart_view_class = GessayeSmartView

    # class GepreteFicheEval(GepreteView):
    #    name = 'ficheeval'
    #    title = _("Fiche d'évaluation")
    #    permissions = '__LOGIN__'
    #    template_name = 'FicheEvalGess.html'


class Geprete(SmartPage):
    application = 'geprete'
    name = 'listegeprete'  # c'est le nom de l'url qui est dans geprete/urls
    label = _("Geprete")
    title = _("Gestion des prêts")
    permissions = {'EXP', 'ACH', 'DIS', 'ARB', 'ADM'}
    views_module = geprete
    smart_view_class = GepreteSmartView
