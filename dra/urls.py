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
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from common import config
import common.views
import common.auth_views
from extable.initialize import init

# Extable initialization
# It seems this is the best place to do it since _all_ apps are fully initialized but the server isn't launched yet
init()

if config.settings.BIOM_AID_USE_PREFIX:
    urlpatterns = [
        # Avoid server error when a browser try to get the default favicon (at /)
        path(
            'favicon.ico',
            lambda request: redirect(config.settings.STATIC_URL + 'local/favicon.ico', permanent=True),
        ),
        path(
            '<str:url_prefix>/not_found/',
            common.views.Error404View.as_view(),
            name='error_404',
        ),
        path(
            '',
            common.views.redirect_to_home,
            kwargs={'url_prefix': 'geqip-chuap'},
            name='root',
        ),
        path(
            'dem/home/',
            common.views.redirect_to_home,
            kwargs={'url_prefix': 'geqip-chuap'},
            name='home-old',
        ),
        path(
            'kos/',
            common.views.redirect_to_kos_home,
            kwargs={'url_prefix': 'kos-chuap'},
            name='kos-start',
        ),
        path(
            'geqip/',
            common.views.redirect_to_home,
            kwargs={'url_prefix': 'geqip-chuap'},
            name='geqip-start',
        ),
        path('admin/', admin.site.urls, name='admin'),
        path(
            '<str:url_prefix>/index/',
            common.views.BiomAidAccueil.as_view(),
            name='home',
        ),
        path('<str:url_prefix>/common/', include('common.urls')),
        path('<str:url_prefix>/assetplus/', include('assetplusconnect.urls')),
        path('<str:url_prefix>/dem/', include('dem.urls')),
        path('<str:url_prefix>/drachar/', include('drachar.urls')),
        path('<str:url_prefix>/marche/', include('marche.urls')),
        path('<str:url_prefix>/finance/', include('finance.urls')),
        path('<str:url_prefix>/geprete/', include('geprete.urls')),
        path('<str:url_prefix>/admin/doc/', include('django.contrib.admindocs.urls')),
        # Login and Logout
        path(
            '<str:url_prefix>/signup/',
            common.auth_views.SignUp.as_view(),
            name='signup',
        ),
        path(
            '<str:url_prefix>/login/',
            common.auth_views.LoginView.as_view(),
            name='login',
        ),
        path(
            '<str:url_prefix>/logout/',
            common.auth_views.LogoutView.as_view(),
            name='logout',
        ),
        path(
            '<str:url_prefix>/password_change/',
            common.auth_views.PasswordChangeView.as_view(),
            name='password_change',
        ),
        path(
            '<str:url_prefix>/password_change/done/',
            common.auth_views.PasswordChangeDoneView.as_view(),
            name='password_change_done',
        ),
        path(
            '<str:url_prefix>/password_reset/',
            common.auth_views.PasswordResetView.as_view(
                template_name="registration/password_reset.html",
                email_template_name="registration/password_reset_email.html",
            ),
            name='password_reset',
        ),
        path(
            '<str:url_prefix>/password_reset/done/',
            common.auth_views.PasswordResetDoneView.as_view(),
            name='password_reset_done',
        ),
        path(
            '<str:url_prefix>/reset/<uidb64>/<token>/',
            common.auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm',
        ),
        path(
            '<str:url_prefix>/reset/done/',
            common.auth_views.PasswordResetCompleteView.as_view(),
            name='password_reset_complete',
        ),
    ] + static(config.settings.MEDIA_URL, document_root=config.settings.MEDIA_ROOT)
else:
    urlpatterns = [
        path('', common.views.BiomAidAccueil.as_view(), name='accueil'),
        path('common/', include('common.urls')),
        path('dem/', include('dem.urls')),
        path('drachar/', include('drachar.urls')),
        path('marche/', include('marche.urls')),
        path('finance/', include('finance.urls')),
        path('geprete/', include('geprete.urls')),
        path('admin/doc/', include('django.contrib.admindocs.urls')),
        path('admin/', admin.site.urls),
        # Login and Logout
        path('signup/', common.auth_views.SignUp.as_view(), name='signup'),
        path('login/', common.auth_views.LoginView.as_view(), name='login'),
        path('logout/', common.auth_views.LogoutView.as_view(), name='logout'),
        path(
            'password_change/',
            common.auth_views.PasswordChangeView.as_view(),
            name='password_change',
        ),
        path(
            'password_change/done/',
            common.auth_views.PasswordChangeDoneView.as_view(),
            name='password_change_done',
        ),
        path(
            'password_reset/',
            common.auth_views.PasswordResetView.as_view(
                template_name="registration/password_reset.html",
                email_template_name="registration/password_reset_email.html",
                # success_url=reverse_lazy('password_reset_done'),
            ),
            name='password_reset',
        ),
        path(
            'password_reset/done/',
            common.auth_views.PasswordResetDoneView.as_view(),
            name='password_reset_done',
        ),
        path(
            'reset/<uidb64>/<token>/',
            common.auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm',
        ),
        path(
            'reset/done/',
            common.auth_views.PasswordResetCompleteView.as_view(),
            name='password_reset_complete',
        ),
    ] + static(config.settings.MEDIA_URL, document_root=config.settings.MEDIA_ROOT)

# Page d'erreur
handler403 = common.views.Error403View.as_view()
handler404 = common.views.Error404View.as_view()

if config.settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
