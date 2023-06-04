Les tests de régression
=======================

Pour l'instant, pas vraiment de tests unitaires mais plutôt des tests de régression et des embryons de tests
End-to-End (E2E) ou tests "de bout en bout".

- Utilisation de Playwright
- tests par module/application
- Base de tests avec structure (description + outils pour la faire évoluer au cours du développement)

La base de tests
================

Les tests de BiomAid utilisent une base de tests qui intègre un jeu de données minimal et bien contrôlé pour pouvoir réaliser des tests unitaires et/ou de régression et/ou E2E.

Cette base de tests est stockée sous la forme d'une fixture json, format qui est le moins sensible aux modifications de structure de la base de données. 
Cette fixture est nommée `tests_db.json` et est disponible dans le dossier `fixtures`


Cette base comporte :
    - 2 établissements
    - 3 Pôles
    - X Services
    - 1 Discipline : BI (Biomédical)
    - 1 Domaine : 324 (Perfusion...)
    - 2 Programmes :
        - BIO-00-PE : Programme biomédical courant, enveloppe de 1M€
        - TVX-00-PC : Programme travaux courants, enveloppe de 250k€
    - 11 utilisateurs :
        - `root`, mot de passe `introuvable`, qui est le super-utilisateur (n'a pas de droits DRAV2)
        - Ella de Bozieux, `deboziel` mot de passe `yQ6FfiKypa7h8Hc`, directrice adjointe
        - Sylvie Cekilépamor, `cekilesy` mot de passe `yQ6FfiKypa7h8Hc`, chef du pôle AAAA - Chirurgie
        - Yvon Enbaver, `enbaveyv` mot de passe `yQ6FfiKypa7h8Hc`, Cadre supérieur du pôle AAAA - Chirurgie
        - Théo Courant, `couranth` mot de passe `yQ6FfiKypa7h8Hc`, Cadre du service de Chirurgie
        - Lana Tomie `tomiela` mot de passe `yQ6FfiKypa7h8Hc`, acheteur/expert
        - Vincent Timettre `timettvi` mot de passe `yQ6FfiKypa7h8Hc`, expert en perfusion
        - Harry Staukrate `arbitre_biomed` mot de passe `yQ6FfiKypa7h8Hc`, arbitre biomédical
        - Jean Bonbeure `bonbeuje` mot de passe `yQ6FfiKypa7h8Hc`, conducteur de travaux
        - Lorie Zonlointin `zonloilo` mot de passe `yQ6FfiKypa7h8Hc`, ingénieur travaux
        - Paul Igonne `igonnepa` mot de passe `yQ6FfiKypa7h8Hc`, arbitre travaux
    - 4 Demandes :
        - 1 : Demande simple (uniquement les champs obligatoires)
        - 2 : Demande complète (sauf documents et coûts complémentaires)
        - 3 : Demande non validée par le chef de pôle
        - 4 : Demande validée par le chef de pôle

La structure
++++++++++++

Les utilisateurs
++++++++++++++++

Les demandes pré-rentrés
++++++++++++++++++++++++

Les opérations pré-rentrées
+++++++++++++++++++++++++++

pytest
======

.. note:: 
    A compléter, indiquer comment la bibliothèse est utilisée dans BiomAid

Le voyage dans le temps
=======================

.. note:: 
    A compléter : expliquer pourquoi le voyage dans le temps est nécessaire et comment l'utiliser
    pour faire des tests

Playwright
==========

.. note:: 
    A compléter, indiquer comment la bibliothèse est utilisée dans BiomAid

La classe BiomAidPage
+++++++++++++++++++++

.. note:: 
    A compléter : donner les méthodes utiles (logging, locator pour les SmartViews, goto_name)