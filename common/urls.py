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
"""common URL Configuration

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

from common import views, auth_views
from common.base_views import get_view_url_patterns
from common.user_settings import ApiUserSettingsView

admin.autodiscover()

app_name = 'common'
urlpatterns = [
    path('api/settings/', ApiUserSettingsView.as_view(), name='api_user_settings'),
    path('sign/<str:what>/', auth_views.Sign.as_view(), name='sign'),
    path('sign/', auth_views.Sign.as_view(), name='sign'),
    path('login_check/', auth_views.LoginCheck.as_view(), name='login_check'),
    path('signed_up/', auth_views.SignedUp.as_view(), name='signed_up'),
    path('account/', views.BiomAidAccount.as_view(), name='account'),
    path('account/<int:id>/', views.BiomAidAccount.as_view(), name='account'),
    path('account/<str:username>/', views.BiomAidAccount.as_view(), name='account'),
    path('user_alerts/', views.UserAlerts.as_view(), name='user-alerts'),
    # path('user_alerts/<int:id>/', views.UserAlerts.as_view(), name='user-alerts'),
    # path('user_alerts/<str:username>/', views.UserAlerts.as_view(), name='user-alerts'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('preferences/', views.Preferences.as_view(), name='preferences'),
    # path('pas_encore_fait/', views.not_done_yet, name='pas_encore_fait'),
    path('accueil/', views.BiomAidAccueil.as_view(), name='accueil'),
    path('about/', views.BiomAidAbout.as_view(), name='about'),
    path('cockpit/', views.BiomAidCockpit.as_view(), name='cockpit'),
    path('admin/', views.AdminHome.as_view(), name='admin-home'),
    path('manager/', views.ManagerHome.as_view(), name='manager-home'),
    # path('structure/<str:level>/<str:code>/', views.structure, name='structure'),
    # path('programme_view/', views.ProgrammeView.as_view(), name='programme'),
    # path('calendrier_view/', views.CalendrierView.as_view(), name='calendrier'),
    # path('roles_view/', views.RoleScopeView.as_view(), name='role-scope'),
    path('no_ie/', views.no_ie_view, name='no_ie_view'),
    # path('gestion_fournisseurs/', views.gestion_fournisseurs, name='gestion_fournisseurs'),
    path('gestion_marques/', views.GestionMarques.as_view(), name='gestion_marques'),
    path('gestion_types/', views.GestionTypes.as_view(), name='gestion_types'),
    path('gestion_comptes/', views.GestionComptes.as_view(), name='gestion_comptes'),
    path('gestion_uf/<str:etabid>/', views.GestionUf.as_view(), name='gestion_uf'),
    path('gestion_pole/<str:etabid>/', views.GestionPole.as_view(), name='gestion_pole'),
    path(
        'gestion_service/<str:etabid>/',
        views.GestionService.as_view(),
        name='gestion_service',
    ),
    path(
        'gestion_centreresponsabilite/<int:etabid>/',
        views.GestionCentreResponsabilite.as_view(),
        name='gestion_centreresponsabilite',
    ),
    path('gestion_site/<str:etabid>/', views.GestionSite.as_view(), name='gestion_site'),
    path(
        'gestion_etablissement/',
        views.GestionEtablissement.as_view(),
        name='gestion_etablissement',
    ),
    path(
        'gestion_structure/<str:etabid>/',
        views.GestionStructure.as_view(),
        name='gestion_structure',
    ),
    path('structure21/', views.StructureView.as_view(), name='structure21'),
    path('admin_config/', views.AdminConfig.as_view(), name='admin-config'),
    path(
        'attachment/<root>/<path:path>/',
        views.AttachmentView.as_view(),
        name='attachment',
    ),
    path(
        'alerts-documentation/',
        views.AlertsDocumentationView.as_view(),
        name='alerts-documentation',
    ),
    # Juste pour les tests
    # path('test_403/', views.Error403View.as_view()),
    # path('test_404/', views.Error404View.as_view()),
]

urlpatterns.extend(get_view_url_patterns(views.ProgrammePage))
urlpatterns.extend(get_view_url_patterns(views.RoleScopeView))
urlpatterns.extend(get_view_url_patterns(views.CalendrierView))
urlpatterns.extend(get_view_url_patterns(views.FournisseurPage))
