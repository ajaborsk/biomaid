# Quelques idées en vue d'un module pour un plan pluriannuel

## Fonctionnalités en vrac

- Production d'un document synthétique pour les DAF
- Mise à jour automatique en fonction de l'avancement des plans d'équipement
- Construction d'un plan prévisionnel de décaissement
- Utilisation des demandes en cours (mais comment ?)
- Gestion des remplacements, des projets neufs, des mises à jour
- Gestion des projets issus de divers niveaux de "validation" :
  - Déjà acheté
  - Engagé (commande faite)
  - Plan équipement (validé explicitement)
  - PPI
  - Estimations simples
- Gestion d'enveloppes, de plus en plus fines au fur et à mesure que le niveau de validation augmente
- Possibilité de définir un "horizon" (utilisable notamment pour les remplacements)

## Fonctionnalités facultatives ?

- Aide à la construction via la GMAO (critères de remplacement ?)
- Gestion des locations ? (bascules location <-> HA ou l'inverse ?)
- Gestion d'hypothèses :
  - Si j'accepte (ou pas) tel projet, cela fait quoi ?
  - Si je pars sur une durée de vie de 10 ans au lieu de 8, cela fait quoi ?
  - Si je décale tel projet, cela fait quoi ?

## Idée d'algorithme

### Construire une liste (temporaire) d'opérations, avec chacune :

- Un code
- Son nom
- Sa hiérarchie (opération parente)
- Son niveau dans la hiérarchie des opérations ?
- Sa hiérarchie d'hypothèses ?
- Son montant
- les dates prévues (début / fin), en première approximation pour les niveaux élevés (la dépense sera étalée entre ces deux bornes)
- Des tags : "Biomédical", "Travaux", "Equipements", "Projet", "Remplacement", etc. ? liste d'identifiants
- La source de l'oparation (programme, demande, opération, etc.). Sous forme de JSON ?

### Les sources de ces "opérations" diffèrent suivant le niveau :

- Plans institutionnels
- Projets (institutionnels ou non)
- Plans validés
- Commandes en cours
- GMAO

Si la construction est "paramétrique", on peut construire plusieurs listes, donc avec différentes hypothèses

### Modèle

- Code (?)
- Source (modèle/str/GID + code/str ?) ==> GenericContent ?
- Début (Date)
- Fin (Date)
- Hypothèse (code/str ou FK)
- Montant (Amount)

### Règles pour générer les opérations

- Demandes refusées ==> Rien (ignorées)
- Pour les demandes avec prévisionnel (=validée)
  - Si prévisionnel fermé => 1 opération par commande
  - 1 opération pour le reste de la demande validée
- 1 opération par programme, avec le reste du montant de l'enveloppe entre (maintenant ou début) et fin
  - paramètre de règle possible : modification date du programme

### Définition d'une stratégie

Un jeu de règles + paramètres
Exemple de paramètres :

- Début de tel projet à telle date

Une stratégie peut servir à :

- Faire un prévisionnel des dépenses
- Rédiger/Générer automatiquement certaines demandes (voir comment valider ces stratégies et limiter leur périmètre d'action)
- Faire une simulation de l'évolution du parc (âge, état, etc.)

Différents types de règles :

- Générer une opération pour un plan d'équipement
- Modifier la date d'une opération (ou d'un ensemble d'opérations ?) dans un programme
- Modifier le montant d'une opération (ou d'un ensemble d'opérations ?) dans un programme
- Décaler un programme
- Annuler un programme

Modèle des instances de règle :

- No ordre (int)
- Code (str) ?
- Intitulé (str) ?
- Moteur (str)
- Paramètres (JSON)

L'identifiant d'une hypothèse est constitué de l'identifiant de l'hypothèse parente + un séparateur + l'identifiant/code (unique) de la sous hypothèse

Une règle d'applique dans le cadre d'une hypothèse si et seulement si le code complet de l'hypothèse commence par le code complet de la règle

## Implémentation

Les types de règles sont dans un fichier de configuration et non dans une base de données
Les hypthèses / stratégies dans une table ?
Une stratégie = 1 liste (ordonnée) de règles = 1 hypothèse
Une sous-sratégie = 1 stratégie + 1 liste de règles
Les opérations dans une table (RAZ complet possible)

### Phase 1

- Règles pour les plans d'équipement (demandes validées)
- Programmes (ensemble de demandes non encore validées)

### Phase 2

- Intégration de demandes "prévisionnelles"

### Phase 3

- Connectivité Asset+
