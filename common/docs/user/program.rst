Les programmes
--------------

Un programme correspond à une enveloppe financière à laquelle on vient rattacher des dépenses.

Seul le responsable applicatif ('manager') peut créer et modifier des programmes.

.. note:: 
    Dans une version ultérieure, on pourrait imaginer un rôle de responsable financier,
    qui pourrait créer et modifier ces programmes.

Chaque programme a les propriétés intrinsèques (enregistrées) suivantes :

- Un code
- Un intitulé
- Une discipline
- Une campagne de rattachement
- Un établissement OU un pôle OU une UF de rattachement : Portée/périmètre de l'enveloppe
- Un arbitre : Utilisateur en charge de valider les demandes rattachées à ce programme
- Un montant estimatif (indicatif)
- Une limite (facultatif) : Montant total à partir duquel BiomAid bloquera les validations
- Une date de fin : Date à partir de laquelle le programme sera/est inactif
- Des pièces jointes (documents attachés)
- Un champs commentaire (texte libre)

Par ailleurs, à chaque modification d'une demande ou d'une opération rattachée
à un programme et au moins une fois par jour, le montant effectivement consommé sur ce programme est calculé et stocké dans la table.
Ce montant consommé est calculé en faisant la somme du montant **le plus fiable possible** de toutes les demandes validées **définitivement**.

Techniquement, c'est la somme du montant validé (donc éventuellement amendée par l'arbitre) 
de toutes les demandes validées mais sans opération rattachée (en attendant la création automatique de cette opération) auquel on ajoute la somme,
pour chaque opération rattachée au programme du meilleur montant estimé de l'opération. Ce montant est lui-même calculé de la façon suivante :

Si l'opération n'est pas soldée, c'est le montant maximum entre l'enveloppe allouée effectivement et le montant effectivement dépensé sur l'opération.

Si l'opération est soldée, c'est le montant effectivement dépensé sur l'opération.

Le montant effectivement dépensé sur une opération est lui-même calculé de la façon suivante :

- Si l'utilisateur a saisi une valeur dans le champ "Montant", c'est cette valeur qui est utilisée.
- Sinon et si au moins une commande rattachée est trouvée par le système, il utilise la meilleure valeur des lignes commandes liées à cette opération :
    - Si une commande n'est rattachée qu'à une opération, toutes les lignes de la commande sont utilisées
    - Si une commande est rattachée à plusieurs opérations, seules les lignes avec la même UF sont utilisées
    - Par ailleurs, le montant utilisé est celui de l'engagement si la ligne de commande n'est pas soldée et le montant liquidé si la ligne est soldée.
- Sinon et si aucune commande rattachée n'est trouvée, la valeur nulle (0 €) est utilisée.

.. note:: 
    Le rattachement aux commandes (et à leurs états) est dépendant du processus analytique "commandes_update" qui
    devrait être lancé au moins une fois par jour (la nuit). Sans cette connexion avec les commandes, disponible seulement pour
    magh2 à la date d'écriture de cette documentation, seul le mode manuel (où le chargé d'opération indique lui-même le montant de l'opération à la main)
    est pertinent.

.. note:: 
    Le process d'analyse des commandes réalise aussi un contrôle sur la cohérence entre les opérations et les commandes et 
    identifie les erreurs (cf. **TODO**)

.. note:: 
    Ce processus nécessite de considérer qu'une opération *soldée* doit s'entendre au sens financier (= une commande soldée ne fera plus l'objet d'une commande en plus)
    et non au sens procédurale (= une opération *soldée* ne nécessite plus aucune action d'aucune sorte de la part du chargé d'opération) 