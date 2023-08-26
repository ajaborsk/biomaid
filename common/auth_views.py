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
import logging

from django.apps import apps
from django.contrib.auth import authenticate, login, get_backends
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from django.contrib.auth import views as auth_views

from common import config
from django.conf import settings

from common.base_views import BiomAidViewMixin
from common.forms import BiomAidUserCreationForm
from common.models import User

try:
    from common.auth_backends import MyLDAPBackend

    USING_LDAP = True
except ImportError:
    USING_LDAP = False


logger = logging.getLogger(__name__)


class LoginView(BiomAidViewMixin, auth_views.LoginView):
    title = _("Connexion")
    permissions = '__PUBLIC__'

    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        # messages.info(self.request, "Vous êtes connecté (ou pas) !")
        return resp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'next' not in context or not context.get('next'):
            # if self.portal:
            #    context['next'] = reverse(self.portal['home'], kwargs=self.reverse_base)
            # elif self.url_prefix:
            context['next'] = self.reverse('common:login_check')

        return context


class LogoutView(BiomAidViewMixin, auth_views.LogoutView):
    title = _("Déconnexion")
    permissions = '__PUBLIC__'

    def dispatch(self, request, *args, **kwargs):
        self.next_page = self.reverse(config.settings.LOGOUT_REDIRECT_URL_NAME)
        return super().dispatch(request, *args, **kwargs)


class PasswordChangeView(BiomAidViewMixin, auth_views.PasswordChangeView):
    pass


class PasswordChangeDoneView(BiomAidViewMixin, auth_views.PasswordChangeDoneView):
    pass


class PasswordResetView(BiomAidViewMixin, auth_views.PasswordResetView):
    permissions = '__PUBLIC__'

    def setup(self, request, *args, **kwargs):
        if 'url_prefix' in kwargs:
            self.extra_email_context = {'url_prefix': kwargs['url_prefix']}
        super().setup(request, *args, **kwargs)

    def get_success_url(self):
        return self.reverse('password_reset_done')


class PasswordResetDoneView(BiomAidViewMixin, auth_views.PasswordResetDoneView):
    permissions = '__PUBLIC__'

    def get_success_url(self):
        return self.reverse('password_reset_complete')


class PasswordResetConfirmView(BiomAidViewMixin, auth_views.PasswordResetConfirmView):
    permissions = '__PUBLIC__'

    def get_success_url(self):
        return self.reverse('password_reset_complete')


class PasswordResetCompleteView(BiomAidViewMixin, auth_views.PasswordResetCompleteView):
    permissions = '__PUBLIC__'


class Sign(BiomAidViewMixin, TemplateView):
    """
    Page de connexion / perte mot de passe / inscription combinée, héritée de CommonView/BiomAidView
    La partie liée à la perte de mot de passe devra être adaptée si utilisation de LDAP/AD
    """

    name = 'sign'
    biom_aid = True
    permissions = '__PUBLIC__'
    template_name = 'common/sign.html'

    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = 'password_reset_done'
    title = _("Connexion")
    token_generator = default_token_generator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = ""

    @method_decorator(sensitive_post_parameters('password', 'password1', 'password2'))
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.extra_email_context = {'url_prefix': self.url_prefix}

    def get(self, request, *args, **kwargs):
        # debug("SignUp.get()")
        # self.message = _(
        #     """Vous pouvez créer un nouveau compte pour accéder à {portal_name}.<br/>
        # Ce compte n'aura initialement aucune UF associée et aucun droit sur le portail.<br/>
        # La seule action possible sera de demander à un responsable de structure (pôle, service, etc.)
        # des droits sur certaines UF."""
        # ).format(portal_name="GEQIP")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Kind of a dangerous print() : Write on the console the (unencrypted) user password...
        # print("Sign.post()", repr(request.POST))

        if 'form' in request.POST and request.POST['form'] == 'sign-up':
            form = BiomAidUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # etablissement = Etablissement(id=1)
                # ext_user = ExtensionUser(user=user, etablissement=etablissement)
                # ext_user.save()

                a_user = authenticate(username=user.username, password=request.POST['password1'])
                if a_user is not None:
                    login(request, a_user)
                else:
                    # Don't know how this can be possible...
                    pass

                return redirect('common:login_check', url_prefix=self.url_prefix)
            else:
                return self.get(
                    request,
                    *args,
                    signup_form=form,
                    message=_("Problème") + str(form.errors),
                    **kwargs,
                )
        elif 'form' in request.POST and request.POST['form'] == 'sign-in':
            a_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if a_user is not None:
                login(request, a_user)
                # Redirect to correct page
                # TODO: Redirect to correct page
                return redirect('common:login_check', url_prefix=self.url_prefix)
            else:
                # a_user is None => No identification
                form = AuthenticationForm(request.POST)

                if USING_LDAP and MyLDAPBackend in [b.__class__ for b in get_backends()]:
                    message = _(
                        """Ces identifiants de connexion ne permettent pas de vous connecter au portail.
                    Si vous avez des identifiants Windows, vous pouvez les utiliser avec GEQIP/KOS."""
                    )
                else:
                    message = _("""Ces identifiants de connexion ne permettent pas de vous connecter au portail.""")

                return self.get(request, *args, signin_form=form, message=message, **kwargs)
        if 'form' in request.POST and request.POST['form'] == 'password-reset':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                opts = {
                    'use_https': self.request.is_secure(),
                    'token_generator': self.token_generator,
                    'from_email': self.from_email,
                    'email_template_name': self.email_template_name,
                    'subject_template_name': self.subject_template_name,
                    'request': self.request,
                    'html_email_template_name': self.html_email_template_name,
                    'extra_email_context': self.extra_email_context,
                }
                form.save(**opts)
                return redirect(self.success_url, url_prefix=self.url_prefix)
            else:
                form = PasswordResetForm(request.POST)
                return self.get(
                    request,
                    *args,
                    password_reset_form=form,
                    message=_("Problème") + str(form.errors),
                    **kwargs,
                )

        # Should never happen but...
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'signup_form' in kwargs:
            context['signup_form'] = kwargs['signup_form']
        else:
            context['signup_form'] = BiomAidUserCreationForm()

        if 'signin_form' in kwargs:
            context['signin_form'] = kwargs['signin_form']
        else:
            context['signin_form'] = AuthenticationForm()

        if 'password_reset_form' in kwargs:
            context['password_reset_form'] = kwargs['password_reset_form']
        else:
            context['password_reset_form'] = PasswordResetForm()

        if 'message' in kwargs:
            context['message'] = kwargs['message']
        else:
            context['message'] = self.message

        return context


class SignUp(BiomAidViewMixin, CreateView):
    """Vue utilisée par un utilisateur non inscrit pour se créer un compte (sans aucun droits)
    sur le portail.
    """

    name = 'signup'
    permissions = '__PUBLIC__'
    form_class = BiomAidUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    biom_aid_applications = {
        'common': {
            'config': apps.app_configs['common'],
            'verbose_name': apps.app_configs['common'].verbose_name,
            'roles': set(apps.app_configs['common'].biom_aid_roles),
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Création d'un compte"
        context['message'] = self.message

        return context

    def get(self, request, *args, **kwargs):
        # debug("SignUp.get()")
        self.message = _(
            """Vous pouvez créer un nouveau compte pour accéder à GÉQIP.<br/>
        Ce compte n'aura initialement aucune UF associée et aucun droit sur le portail.
        Il vous faudra contacter un administrateur pour obtenir les droits nécessaires."""
        )
        return super().get(request, *args, **kwargs)

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request, *args, **kwargs):
        # debug("SignUp.post()", request.POST)

        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # etablissement = Etablissement(id=1)
            # ext_user = ExtensionUser(user=user, etablissement=etablissement)
            # ext_user.save()

            # debug("ext_user", ext_user)
            return redirect(self.reverse('common:signed_up'))
        else:
            self.message = _("Problème" + str(form.errors))
            return super().post(request, *args, **kwargs)


class SignedUp(BiomAidViewMixin, TemplateView):
    """Vue affichée une fois que l'utilisateur a créé un compte pour lui-même"""

    name = 'signed_up'
    permissions = '__PUBLIC__'
    template_name = 'common/signed_up.html'


class LoginCheck(BiomAidViewMixin, TemplateView):
    """Vue affichée une fois que l'utilisateur a créé un compte pour lui-même"""

    name = 'login_check'
    permissions = '__LOGIN__'
    template_name = 'common/signed_up.html'

    def post(self, request, **kwargs):
        # print("POST:")
        # 1 - Vérifier que les conditions de la fusion/mutation sont toujours valides
        user = request.user
        old_user = User.records.filter(~Q(pk=request.user.pk), email__iexact=request.user.email).get()

        # 2 - Rechercher tous les champs avec une ref externe de User
        user_links = []
        for app_cfg in apps.get_app_configs():
            for model in app_cfg.get_models():
                for field in model._meta.fields:
                    model_attrname = field.attname
                    if field.is_relation:
                        if issubclass(field.related_model, User):
                            user_links.append((model, model_attrname))

        # 3 - Faire la modif partout dans une unique transaction
        with transaction.atomic():
            # 3.1 - Dans les tables avec un lien vers User
            for user_link in user_links:
                # print(user_link)
                qs = user_link[0].records.filter(**{user_link[1]: old_user.pk})
                # print("  Nb:", qs.count())
                qs.update(**{user_link[1]: request.user})

            # 3.2 - Copier les champs de User sauf ceux fournis par LDAP (=username, nom, prénom, email)
            for field in User._meta.fields:
                if field.attname not in settings.AUTH_LDAP_USER_ATTR_MAP.keys() and not field.primary_key:
                    setattr(user, field.attname, getattr(old_user, field.attname))
            # print(user, user.pk)

            # 3.3 - Save updated user
            user.save()

            # 3.4 - Désactiver l'ancien compte
            old_user.is_active = False
            old_user.save()

        # Et voilà !

        # Si tout s'est bien passé, rediriger vers l'accueil (ou une page spéciale ?)
        # return redirect('dem:home', **kwargs)

        return self.get(request, **kwargs)

    def get(self, request, **kwargs):
        # print("User check", self._user_roles)
        if self._user_roles:
            # print('has roles !')
            return redirect(self.reverse(self.portal['home']))
        # return super().get(request, **kwargs)

        response_kwargs = {}
        response_kwargs.setdefault('content_type', self.content_type)
        context = self.get_context_data(**kwargs)
        context['message'] = _(
            "Votre compte est opérationnel, mais vous n'avez pour l'instant aucune autorisation"
            " dans GÉQIP et/ou KOS.<br><br>"
            " Vous pouvez rendre contact par messagerie avec les auteurs du logiciel (ci-dessous)"
            " et demander les autorisations sur votre secteur (UF, pôle...), avec l'accord de votre"
            " responsable."
        )
        if request.user.from_ldap:
            template = 'common/new_ldap_account.html'
            users = User.records.filter(~Q(pk=request.user.pk), email__iexact=request.user.email)
            n_users = users.count()
            logger.debug("Comptes {n_users} {users.values_list('username', flat=1)}")

            if n_users == 0:
                context['message'] = _(
                    "Votre compte est opérationnel, mais vous n'avez pour l'instant aucune autorisation"
                    " dans GÉQIP et/ou KOS.<br><br>"
                    " Il n'existe pas de compte existant avec exactement la même adresse email que"
                    " ce nouveau compte Microsoft (Windows) et qui pourrait être le vôtre. <br><br>"
                    " Si vous aviez un compte sur GÉQIP/KOS, il n'a pas été détecté."
                    "<br>Merci de contacter les administrateurs du site (cf. bandeau ci-dessous) pour"
                    " résoudre le problème.<br><br>"
                    " Votre ancien compte, s'il existe, reste fonctionnel."
                )
            elif n_users > 1:
                context['message'] = _(
                    "Votre compte est opérationnel, mais vous n'avez pour l'instant aucune autorisation"
                    " dans GÉQIP et/ou KOS.<br><br>"
                    " Il existe plusieurs comptes existants avec la même adresse email que ce nouveau compte"
                    " Microsoft (Windows) et il n'est pas possible de faire un rapprochement automatique."
                    "<br>Merci de contacter les administrateurs du site (cf. bandeau ci-dessous) pour"
                    " résoudre le problème.<br><br>"
                    " Votre ancien compte reste fonctionnel."
                )
            else:
                context['message'] = _(
                    "Votre compte est opérationnel, mais vous n'avez pour l'instant aucune autorisation"
                    " dans GÉQIP et/ou KOS.<br><br>"
                    " Il existe un compte existant avec exactement la même adresse email que ce nouveau compte"
                    " Microsoft (Windows) et qui est probablement le vôtre. <br><br>"
                    " Si vous confirmez le formulaire, Tous les droits seront copiés et"
                    " l'ancien compte supprimé."
                )
                context['old_user'] = users.get()
        else:
            template = 'common/empty_account.html'

        return TemplateResponse(
            request=self.request,
            template=[template],
            context=context,
            using=None,
            **response_kwargs,  # default template engine
        )
