=====================================================
Le calcul des montants
=====================================================

Le calcul des montants dans le workflow de gestion des demandes est assez complexe.

Pour chaque demande, seules 5 quantités impliquées dans ce calcul sont stockées dans la base de données :

  - La quantité demandée `Demande.quantite` (obligatoire, valeur par défaut = 1)
  - Le prix unitaire demandé `Demande.prix_unitaire` (facultatif)
  - Le montant unitaire donné par l'expert `Demande.montant_unitaire_expert_metier` (facultatif)
  - La quantité validée *in fine* `Demande.quantite_validee`
  - Le montant validé *in fine* `Demande.montant_valide`

Le système affiche et gère, toutefois, plusieurs autres quantités, qui sont définies dans les
SmartView et qui sont calculées "au vol", pendant la requête SQL, à chaque fois que c'est nécessaire :

  - Le montant initial `montant_initial` : Montant initial total de la demande, calculé en multipliant la quantité
    demandée avec le prix unitaire initial.
  - Le montant avant arbitrage `montant_arbitrage` : Montant calculé en multipliant la quantité demandée avec le prix
    unitaire donné par l'expert ou, si ce dernier n'est pas précisé, avec le prix unitaire initial. Ce montant
    d'arbitrage est nécessaire pour valider une demande (mais pas forcément pour la refuser) et peut être indéfini
    au début de l'expertise d'une demande.
  - Un montant dit *final*, utilisé uniquement pour les calculs internes (non affiché). **A COMPLETER**
  - Un montant intermédiaire calculé à partir de la quantité demandée et du montant arbitrage **A COMPLETER**

Par ailleurs, il existe aussi des champs "intelligents" (utilisables pour l'instant uniquement dans les tableaux)
qui permettent d'afficher et de saisir des valeurs dans une colonne unique :
  - Le "Montant corrigé expert", identifié comme `montant_conditional_expert` : Affiche sur fond blanc la valeur donnée par
    le demandeur si aucune valeur n'est donnée par l'expert ou la valeur donnée par l'expert (avec une saisie dans cette
    même colonne) sur fond jaune.
  - La quantité validée par l'arbitre (ou la commission), identifiée dans le code comme `quantite_validee`, qui affiche
    sur fond blanc la quantité demandée et sur fond jaune la valeur éventuellement donnée par l'arbitre (qui peut être
    saisie dans cette même colonne).
  - Le montant total (enveloppe) validé par l'arbitre, indentifiant `montant_valide_conditional`, qui affiche soit le
    montant calculé à partir de la quantité validée (initiale ou corrigée) et le montant unitaire (initial ou corrigé),
    sur fond blanc, mais qui peut être donnée directement par l'arbitre (sur fond jaune) directement dans cette
    colonne. C'est la valeur affichée dans cette colonne qui sera utilisé *in fine* pour déterminer l'enveloppe
    attribuée dans le plan d'équipement.

.. note::
    Tous les montants sont stockés et calculés en TTC
