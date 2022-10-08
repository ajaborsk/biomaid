Alertes (propositions) :
========================

Interventions Asset+ :
++++++++++++++++++++++

Intervention en cours depuis longtemps
--------------------------------------

Et pas mise à jour...

Intervention mixte sans numéro de commande
------------------------------------------

Voir suivant l'état car dans la première partie du traitement de l'intervention, il n'y a pas de commande...

Intervention mixte en cours depuis longtemps et sans devis
----------------------------------------------------------

Relancer la société ?

On peut imaginer que ce ne soit pas le technicien qui relance, si la fiche est bien remplie. On pourrait
par exemple avoir un `LIB_STATUS` "En attente de devis"

Commandes :
+++++++++++

1 - Commande en cours depuis longtemps :
----------------------------------------

Commande non reçue depuis longtemps... (90 jours ?). Voir comment on peut enregistrer la relance (peut-être via Asset+ ?)

2 - Commande non liée à une intervention Asset+
-----------------------------------------------

Commande sans correspondance dans Asset+

3 - Commande non soldée alors que l'intervention Asset+ l'est
-------------------------------------------------------------

Commande non soldée alors que l'intervention Asset+ est archivée

**Q**: L'inverse n'est pas normal non plus... Plutôt parler de discordance d'état ?

**R**: Non, car l'action à mener n'est pas la même !

4 - Discordance entre commande et Asset+
----------------------------------------

Une commande (ou seulement une ligne ?) doit avoir un numéro d'intervention et l'intervention correspondante doit avoir
le numéro de commande (le même !). Si ce n'est pas le cas, c'est qu'il y a un problème...

Intégrer l'alerte 2 ? ("Commande non liée à une intervention Asset+")

4 - Discordance de montant entre commande et Asset+
---------------------------------------------------

La commande (ligne ?) et l'intervention Asset+ sont bien liées, mais les montants ne correspondent pas...

Factures :
++++++++++

1 - Facture encore en attente alors que la commande est soldée
--------------------------------------------------------------

Il faut tout de même qu'il y ait concordance des montants et des fournisseurs (= rapprochement OK)

