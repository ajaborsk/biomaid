# Nouveautés

## Version 0.15 (21 juin 2024)

- [X] Un manager a maintenant accès à la gestion des rôles
- [X] Ajout de la notion de "clôture" globale aux opérations (en plus du "solde" purement lié aux commandes)
- [X] Documentation d'installation plus complète

## Version 0.14 (26 septembre 2023)

- [X] Todo...

## Version 0.13 (9 juin 2023) :

### Nouveautés
- [X] Ajout de fonctions analytics pour le suivi financier des plans d'équipement
- [X] Début d'implémentation du suivi financier précis en temps réel
- [X] Première fonction analyse pour les immobilisations
- [X] Possibilité de définir (par l'administrateur) des arbitres et des dispatcheurs "adjoints"

### Documentation
- [X] Changement du thème Sphinx (passage à 'book')
- [X] Nombreuses pages rédigées et/ou complétées:
   - documentation sur la documentation
   - dem:dispatch
   - dem:arbitration
   - ...

### Corrections bugs :

- [X] Corrections des problèmes multiples avec le workflow des travaux

### Sous le capot :

- [X] Bascule de la gestion des fichiers DRA94 sur extable
- [X] Création d'une commande de backup
- [X] Utilisation d'extable pour l'inventaire Asset+
- [X] Meilleure gestion du délai pour les bascules automatiques sur les plans d'équipement
- [X] Mise à jour des dépendances et passage à Django 4.2
- [X] Avancées sur la migration des tests vers Playwright

## Version 0.12.2 (22 novembre 2022) :

### Nouveautés

- [X] Ajout d'une colonne pour signaler un problème dans le workflow (ex. demande sur un mauvais programme). Voir comment l'utiliser...
- [X] Les utilisateurs/demandeurs peuvent maintenant voir les demandes acceptées dans le détail (possibilité d'ouvrir la demande avec l'outil 'oeil')
- [X] Ajout d'un module 'analytics' qui permet d'afficher des graphiques (expérimental pour l'instant) et surtout de lancer des 'analyses' en série (notamment pour les commandes)
- [X] Nouveau portail dédié 'commandes et gestionnnaires', avec accès aux analyses des commandes, etc.
- [X] Ajout d'un tableau des exceptions marchés (code HMn)
- [X] Remise à plat colonnes affichées (ou pas) dans les différentes pages

### Corrections bugs :

- [X] Correction colonnes calcul prix final
- [X] Correction format colonne 'conditionnelle' en cas de retour à la valeur initiale (redevient blanche)
- [X] Correction filtres programmes et campagnes (plus limités aux campagnes ouvertes mais à toutes les valeurs dans la table)

### Sous le capot :

- [X] Mise à jour vers fontawesome 6
- [X] Code préliminaire pour une gestion des "widgets"
- [X] Début de code pour génération de la documentation

## Version 0.11.3 (12 août 2022) :

### Corrections bugs :

- [X] Correction bug liens dans les alertes entraînait une erreur 500
- [X] Correction désélections/sélections intempestives lignes dans suivi drachar
- [X] Les campagnes inutilisées ne sont plus montrées dans le cockpit
- [X] Les utilisateurs inactifs ne peuvent plus être choisis
- [X] Bloqué pour l'instant à Django 4.0 => retour lien Asset+ (oracle 11.2 non supporté par Django 4.1)

## Version 0.11.2 (1er août 2022) :

### Corrections bugs :

- [X] Correction problème chemin des pièces jointes

## Version 0.11.1 (unpublished) :

### Corrections bugs :

- [X] Ajout des droits pour permettre de faire de demandes informatiques
- [X] Correction des scripts pour les jobs périodiques (alertes, transferts de demandes entre programmes,
      validations auto...)

## Version 0.11 (29 juillet 2022) :

### Pour tout le monde :

- [X] Nouvelle page de connexion, avec trois parties (connexion, mot de passe oublié et nouveau compte)
- [X] Connexion grâce au compte Windows (LDAP/AD)
- [X] La colonne 'actions' est verrouillée à droite dans les tableaux
- [X] Gestion complète des demandes d'intéressement
- [X] Correction du bug de tri des valeurs numériques (montants)

### Services demandeurs :

- [X] Correction du bug empêchant la copie d'une demande
- [X] Nouveau workflow pour les demandes de travaux (demandes par les cadres avec validation par l'encadrement du pôle)
- [X] Mise à jour du lien vers l'annuaire du CHU

### Experts :

- [X] Champ UF dans le prévisionnel maintenant dédié et modifiable par l'arbitre du programme
- [X] L'enveloppe du prévisionnel peut être modifiée par l'arbitre du programme
- [X] Portail dédié au backoffice pour les travaux (KOS)
- [X] Possibilité de donner un avis directement à la saisie d'une nouvelle demande

### Sous le capot :

- [X] Renommage de tous les 'Drav2' vers 'BiomAid'
- [X] Mise à jour vers Tabulator 5.3
- [X] Toutes les données de l'utilisateur sont dans le modèle User (suppression modèle ExtensionUser)
- [X] L'argumentaire étendu est dans le modèle Demande pour tous les types de demande (suppression modèle ArgumentaireDetaille)
- [X] Toutes les vues sont maintenant des classes (plus de vues "fonctions")
- [X] Tous les formulaires de l'appli `dem` sont générés et gérés automatiquement
