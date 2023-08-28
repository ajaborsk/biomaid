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
from . import views, views21, views_tvx
from common.base_views import get_view_url_patterns

admin.autodiscover()

app_name = 'drachar'
urlpatterns = [
    path('home/', views21.DracharHome.as_view(), name='home'),
    path('mesdossiers/', views21.MesDossiersView.as_view(), name='mesdossiers'),
    path('previsionnel/', views21.PrevisionnelView.as_view(), name='previsionnel-back'),
    # path('nouveaudossier/', views.nouveau_dossier, name='nouveaudossier'),
    path('nouveaudossier/', views.NouveauDossier.as_view(), name='nouveaudossier'),
    # path('nouvelledra/', views.nouvelle_dra, name='nouvelledra'),
    path(
        'nouvelleligne/<int:dra_id>/',
        views21.NouvelleLigneView.as_view(),
        name='nouvelleligne',
    ),
    path('listedra/', views21.listedra.as_view(), name='listedra'),
    # path('nouvelledra/', views.NouvelleDra.as_view(), name='nouvelledra'),
    path('nouvelledra/', views21.Nouvelle_draView.as_view(), name='nouvelledra21'),
    path(
        'nouvelledra/<int:dra_id>/',
        views21.Nouvelle_draView.as_view(),
        name='nouvelledra21',
    ),
    # path('cockpit/', views.cockpit, name='cockpit'),
    path('cockpit/', views21.CockpitView.as_view(), name='cockpit'),
    path('suiviplan/', views21.PrevisionnelView.as_view(), name='previsionnel'),
    path('suivi_validees/', views21.SuiviAcquisitions.as_view(), name='suivi-plans'),
    path('suivi_travaux/', views_tvx.SuiviTravaux.as_view(), name='suivi-travaux'),
    path(
        'suivi_travaux_exp/',
        views_tvx.PrevisionnelTvxView.as_view(),
        name='suivi-travaux-exp',
    ),
    # "tous" en N° programme pour tout afficher
    # path('gestion_previsionnel/<str:programme>/', views.gestion_previsionnel, name='gestion_previsionnel'),
    path(
        'gestion_previsionnel/<str:programme>/',
        views.GestionPrevisionnel.as_view(),
        name='gestion_previsionnel',
    ),
    # re_path('gestion_contact_liv/', views.gestion_contact_liv, name='gestioncontactlivraison22'),
    path(
        'contactlivraison/',
        views.GestionContactLivraison22.as_view(),
        name='gestioncontactlivraison22',
    ),
]
urlpatterns.extend(get_view_url_patterns(views.GestionContactLivraison22))

