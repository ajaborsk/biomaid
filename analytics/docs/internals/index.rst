Le système d'analyse de données (analytics)
===========================================

Les moteurs
-----------

C'est du code python (une classe ?)

Mécanisme de reporting pour les opérations longues (exemple : balayer une table entière)

Types des entrées et des sorties ("signature")

Configurable

Pas de sémantique

Les datasources
---------------

Une datasource = 1 moteur configuré avec ses entrées et ses sorties

Est-ce une instance du moteur ???

Peut être créé à partir d'un fichier de config ou d'une entrée dans la BDD

Propriétés :
  - Commentaire
  - ...

Les data
--------

C'est l'entrée ou la sortie d'une datasource

Cela a un format, une structure (tableau 2d, 3d, autre)

Propriétés :
  - Nom (identifiant unique)
  - Stockage (BDD, colonne, fichier, alerte, néant)
  - Une durée de validité (si stockée)
  - Dépendances (calculées à partir de l'arbre des datasources ?)
  - Un mécanisme pour le calcul automatique régulier (mode forward)
  - Historisation O/N, avec quelle période et quelle politique de conservation
  - Des tags ?

C'est ce qu'on affiche dans les widgets (suivant le format, la structure)

Data de base :
- date/heure
- toutes les tables de BiomAid
- Configuration de BiomAid
- Constantes ?

