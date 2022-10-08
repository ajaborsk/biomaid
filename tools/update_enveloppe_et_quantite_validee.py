""" Attention : Script à exécuter une seule fois au moment du passage à la version 0.2.3 (ou 0.3)

    *** ET DANS TOUS LES CAS AVANT LES ARBITRAGES !!! ***

    avec la commande python manage.py shell < tools/update_enveloppe_et_quantitee_validee.py

    Calcule, pour toutes les demandes, la quantitée validée à partir de la quantité demandée et le
    montant de l'enveloppe validée "par défaut".

    Dans les versions suivantes, ces données se mettent à jour à chaque étape.
"""

import logging

from dem.models import Demande

logger = logging.getLogger(__name__)

logger.info("Let's go !")

for demande in Demande.objects.all():

    # Quantité
    if int(demande.quantite_validee) == 1:
        demande.quantite_validee = demande.quantite
    else:
        logger.warning(
            "Pour la demande {}, la quantitée validée est déjà différente de 1 : {}".format(demande.pk, demande.quantite_validee)
        )

    if demande.quantite_validee is not None:
        quantite = int(demande.quantite_validee)
    elif demande.quantite is not None:
        quantite = int(demande.quantite)
    else:
        quantite = 1  # should never happen...

    if demande.montant_unitaire_expert_metier is not None:
        pu = int(demande.montant_unitaire_expert_metier)
    elif demande.prix_unitaire is not None:
        pu = int(demande.prix_unitaire)
    else:
        pu = None

    if demande.montant_total_expert_metier is not None:
        enveloppe = demande.montant_total_expert_metier
    elif pu is not None:
        enveloppe = quantite * pu
    else:
        # Dans ce cas, aucun moyen de calculer l'enveloppe...
        enveloppe = None
    demande.enveloppe_allouee = enveloppe

    demande.save(update_fields=('quantite_validee', 'enveloppe_allouee'))
