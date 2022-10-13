=====================================================
Le calcul des montants
=====================================================

Le calcul des montants dans le workflow de gestion des demandes
est assez complexe.

Pour chaque demande, seules 5 quantités sont stockées dans la base de données :

  - La quantité demandée (obligatoire, valeur par défaut = 1)
  - Le prix unitaire demandé (facultatif)
  - Le montant unitaire donné par l'expert (facultatif)
  - La quantité validée *in fine*
  - Le montant validé *in fine*

Le système affiche et gère, toutefois, plusieurs autres quantités, qui sont définies dans les
SmartView et qui sont calculées "au vol", pendant la requête SQL à chaque fois que c'est nécessaire :

  - Le montant unitaire corrigé :
  - klj

blabla
