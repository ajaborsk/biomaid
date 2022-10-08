#  Copyright (c)

#
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
from django.utils.translation import gettext_lazy as _

from common import config
from dem.smart_views import DemandeEqptSmartView
from smart_view.smart_page import SmartPage


class RequestView(SmartPage):
    application = 'dem'
    name = 'request'
    label = _("Demandes")
    permissions = config.settings.DEM_DEMANDE_CREATION_ROLES
    record_ok_message = _("Demande {code} enregistrée avec succès")
    deleted_done_message = _("La demande {code} a été supprimée.")
    no_grant_to_delete_record_message = _("Vous n'avez pas les droits suffisants pour supprimer la demande {code}.")
    try_to_delete_wthout_confirm_message = _(
        "La demande {code} ne peut être supprimée sans passer par le formulaire de confirmation"
    )
    smart_view_class = DemandeEqptSmartView
    smart_modes = {
        # L'entrée None décrit le comportement par défaut (sans vue) car la page est aussi une vue !
        None: {
            'view': 'list',  # lister les objets du modèle est la vue par défaut
        },
        'create': {
            'view': 'create',  # Facultatif car c'est la vue par défaut si le nom est 'create"
            'title': _("Ajouter une demande"),
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et ajouter un autre élément"),
                    'value': 'record',
                    'redirect': 'create',
                    'redirect_url_params': lambda vp: vp['request_get'].urlencode(),
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                    'redirect_url_params': lambda vp: vp['request_get'].urlencode(),
                },
            ),
        },
        'update': {
            'args': (('pk', 'int'),),
            'title': _("Modifier la demande"),
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et continuer à modifier"),
                    'value': 'record-then-update',
                    'message': '',
                    # 'redirect': None,  # Attention : Redirection vers le mode None (mode par défaut)
                    'redirect': 'update',  # Attention : Redirection vers le mode None (mode par défaut)
                    'redirect_params': '{%load l10n%}{"pk":{{pk|unlocalize}}}',
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                },
            ),
        },
        'copy': {
            'title': _("Copier une demande"),
            'args': (('pk', 'int'),),
            'exclude': (),
            'next': 'create',  # Par défaut, l'action après avoir copié le contenu d'une instance, c'est d'en créer une nouvelle
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Enregistrer et ajouter un autre élément"),
                    'value': 'record',
                    'redirect': 'create',  # Attention : Redirection vers le mode None (mode par défaut)
                },
                {
                    'type': 'reset',
                    'label': _("Réinitialiser le formulaire"),
                },
            ),
        },
        'view': {
            'args': (('pk', 'int'),),
        },
        'ask-delete': {
            'title': _("Supprimer un élément"),
            'view': 'view',
            'args': (('pk', 'int'),),
            'next': 'delete',
            'buttons': (
                {
                    'type': 'submit',
                    'label': _("Confirmer la suppression"),
                    'value': 'delete',
                    'message': _("<br>Vous allez être redirigé vers le tableau."),
                    'redirect': None,  # Attention : Redirection vers le mode None (mode par défaut)
                },
            ),
        },
        'delete': {
            'args': (('pk', 'int'),),
            'view': 'view',
            # Back to the default view after delete
            'next': None,
        },
    }
