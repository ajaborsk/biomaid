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
"""dra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', viewss.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin

from common.base_views import get_view_url_patterns
from . import views, views_tvx, views22
from . import views21
from django.contrib.auth.decorators import login_required

admin.autodiscover()

app_name = 'dem'  # Name of the DOMAIN (for url naming purpose)

urlpatterns = (
    [
        path('home/', views21.DemHomeView.as_view(), name='home'),
        path('', views21.DemHomeView.as_view(), name='home'),
        path('aide/', views.DemAide.as_view(), name='aide'),
        path('cockpit/', views21.DemCockpit.as_view(), name='cockpit'),
        # path('constr/', views.construction, name='constr'),
        # path('nouvelle_dmd/copy/<int:num_dmd_to_copy>/', views.nouvelle_dmd, name='copy_dmd_old'),
        # path('nouvelle_dmd/', views.nouvelle_dmd, name='nouvelle_dmd_old'),
        # path('nouvelle_dmd/<str:campagne_code>/', views.nouvelle_dmd, name='nouvelle_dmd_old'),
        # path(
        #     'demande/create/<int:num_dmd_to_copy>/',
        #     views.NouvelleDemande.as_view(),
        #     name='copy-dmd',
        # ),
        # path(
        #     'demande/create/<str:campagne_code>/',
        #     views.NouvelleDemande.as_view(),
        #     name='nouvelle-dmd',
        # ),
        # # path('demande/create/', views.NouvelleDemande.as_view(), name='nouvelle_dmd'),
        # # path('modif_demande/<int:num_dmd>/', views.modif_demande, name='modif_demande_bak'),
        # path(
        #     'demande/modify/<int:num_dmd>/',
        #     views.ModificationDemande.as_view(),
        #     name='modif-demande',
        # ),
        # # path('supprimer/<int:num_dmd>/', views.supprimer_demande, name='supprimer_demande_bak'),
        # path(
        #     'demande/ask-delete/<int:num_dmd>/',
        #     views.SuppressionDemande.as_view(),
        #     name='supprimer-demande',
        # ),
        path(
            'demandes-a-approuver/',
            views21.DemandesAApprouverView.as_view(),
            name="demandes-a-approuver",
        ),
        path(
            'demandes-a-l-etude/',
            views21.DemandesEtudeView.as_view(),
            name="demandes-a-l-etude",
        ),
        path(
            'demandes-en-cours/',
            views21.DemandesEnCoursView.as_view(),
            name="demandes-en-cours",
        ),
        path(
            'demandes-en-cours-exp/',
            views21.DemandesEnCoursExpView.as_view(),
            name="demandes-en-cours-exp",
        ),
        path(
            'demandes-tout/',
            login_required(views21.DemandesArchivees.as_view()),
            name='demandes-tout',
        ),
        path(
            'repartition/<str:campagne_code>/',
            views21.DemandesRepartitionView.as_view(),
            name='repartition',
        ),
        path('expertise/', views21.DemandesExpertiseView.as_view(), name='expertise'),
        path(
            'arbitrage/<str:programme_code>/',
            views21.DemandeArbitrageView.as_view(),
            name='arbitrage',
        ),
        path(
            'arbitrage/',
            views21.DemandeArbitrageView.as_view(),
            name='arbitrage-all',
        ),
        path(
            'demandes-archivees-expert/',
            views21.DemandesArchiveesExpert.as_view(),
            name='demandes-archivees-expert',
        ),
        # path('arbitrage/<str:programme_code>/', login_required(views21.demandes_arbitrage), name='arbitrage'),
        # path('arbitrage/cfg-<cfg>/<str:programme_code>/',
        #       login_required(views21.demandes_arbitrage), name='arbitrage'),
        # path('commission_synthese/<str:programme_code>/<str:validation_cp>',
        #       views.commission_synthese, name='commission-synthese'),
        path(
            'commission_synthese/<str:programme_code>/<str:validation_cp>',
            views.CommissionSynthese.as_view(),
            name='commission-synthese',
        ),
        # path(
        #     'commission-synthese2/<str:programme_code>/'
        #     '<str:pole_code>/<str:validation_cp>/<str:code_uf>/<str:domaines>'
        #     '/<str:colonne1>/<str:colonne2>/<str:index1>/'
        #     '<str:index2>/<str:valeur>/<str:typeag>/<str:totl>/<str:totc>',
        #     views.expert_synthese,
        #     name='expert-synthese',
        # ),
        path(
            'commission-synthese2/<str:programme_code>/<str:pole_code>/<str:validation_cp>/<str:code_uf>/<str:domaines>'
            '/<str:colonne1>/<str:colonne2>/<str:index1>/<str:index2>/<str:valeur>/<str:typeag>/<str:totl>/<str:totc>',
            views.ExpertSynthese.as_view(),
            name='expert-synthese',
        ),
        # path('vue-filtre-synthese/', views.vue_filtre_synthese, name='vue-filtre-synthese'),
        path(
            'vue-filtre-synthese/',
            views.VueFiltreSynthese.as_view(),
            name='vue-filtre-synthese',
        ),
        # path('vue-filtre-synthese2/', views.vue_filtre_synthese2, name='vue-filtre-synthese2'),
        path(
            'vue-filtre-synthese2/',
            views.VueFiltreSynthese2.as_view(),
            name='vue-filtre-synthese2',
        ),
        # ===================================================================================================
        # Partie spécifique aux travaux - Pas très intégrée pour l'instant...
        path('tvx/', views_tvx.DemTvxHome.as_view(), name='tvx-home'),
        # path('tvx/demande/', views_tvx.DemandeTvxNouvelle.as_view(), name='tvx-demande'),
        # path('tvx/demandes-en-cours/', views_tvx.DemandeTvx.as_view(), name='tvx-demande'),
        # path('tvx/demande-pre-analyse/', views_tvx.DemandeTvxPreAnalyse.as_view(), name='tvx-demande-pre-analyse'),
        # path('tvx/demande-analyse/', views_tvx.DemandeTvxAnalyse.as_view(), name='tvx-demande-analyse'),
        # path('tvx/demande-validation/', views_tvx.DemandeTvxValidation.as_view(), name='tvx-demande-validation'),
    ]
    + get_view_url_patterns(views_tvx.DemandeTvx)
    + get_view_url_patterns(views_tvx.DemandeTvxApprob)
    + get_view_url_patterns(views_tvx.DemandeTvxTech)
    + get_view_url_patterns(views_tvx.DemandeTvxPreAnalyse)
    + get_view_url_patterns(views_tvx.DemandeTvxAnalyse)
    + get_view_url_patterns(views_tvx.DemandeTvxValidation)
    + get_view_url_patterns(views_tvx.DemandeTvxArchivees)
    + get_view_url_patterns(views22.RequestView)
)
