=========================================================
Portail, configuration locale et thème : Le préfixe d'URL
=========================================================

Les URL de BiomAid commencent toutes par un préfixe, qui la forme de deoux ou trois identifiants
séparés par un '-' (hyphen ou tiret du 6) : `ppppp-ccccc-ttttt`.

Ainsi, au CHU Amiens-Picardie, la page d'accueil de GEQIP est à l'URL : `https://geqip-chuap/dem/home`

Les trois parties de ce préfixe correspondent à trois notions, complètement configurables :
Le portail, la configuration locale et, optionnellement, le thème.

Le portail
==========

Le portail peut être défini comme « l'univers » auquel on donne accès. C'est un ensemble de pages et de
liens (internes ou externes), structuré dans un jeu de menus.

Cela peut être considéré comme un "sous-site" du site principal. C'est un sous-ensemble cohérent de pages avec les
menus permettant de naviguer entre ces pages.

Un portail peut être dirigé vers une catégorie d'utilisateurs (comme les unités de soins) ou un process spécifique.

Ainsi, le portail GéQIP rassemble toutes les pages pertinentes pour un utilisateur d'un service de soins :
Demande d'équipement, validation interne, suivi de l'avancement du traitement ou des réponses, ...
alors que le portail « Demandes de matériel » comporte toutes les pages et tous les liens nécessaires à la gestion
des demandes de matériel, y compris les pages liées à l'expertise des demandes ou les tableaux de bord de suivi
du processus dans son ensemble.

.. note::
    La gestion des droits (qui a accès à quelle page) est indépendante du portail.

.. note::
    Lors de la conception des pages, il n'est pas nécessaire de se préoccuper du portail ou de
    la gestion du préfixe. L'utilisation des classes dans Python (héritage d'une vue BiomAid via le Mixin
    `BiomAidViewMixin`) et l'utilisation du tag de template `<% url_prefix... %>` dans les templates permet la gestion (presque)
    complètement transparente des préfixes au cours de la navigation.

Configuration des portails :
----------------------------

... A rédiger ...

- Portail par process/module/application
- Portails supplémentaires (GéQIP, KOS...)
- thème par défaut = `default`

La configuration locale
=======================

- Ce qui est spécifique à l'établissement (ou le GHT ou le groupe) dont fait partie l'utilisateur. Typiquement
  il s'agit de données comme la forme de l'adresse mail (`@chu-amiens.fr`), des liens vers l'intranet,
  le thème par défaut (aspect graphique, couleurs, etc.)

... A rédiger ...


Le thème
========

... A rédiger ...

Défini par ordre de priorité :

- Par l'URL
- Par la configuration locale
- Par le portail

.. note::
    Il manque probablement un niveau d'indirection pour qu'un portail puisse *choisir* un thème parmi ceux définis par
    la configuration locale. A creuser...


Utilisation dans le code (fonctionnement du mixin) :
====================================================

Lors de l'instantiation des objets « vue » (hérités de `BiomAidViewMixin`), le nom du portail, de la configuration de
site et du thème sont extraits de l'URL, traités et les données stockées dans des attributs de la vue. Cette opération
est réalisée dans la méthode `setup()` du mixin, qui est exécutée **après** la méthode `setup()`
des ancêtres de la classe.


Algorithme de détermination du triplet portail-configuration-thème :
====================================================================
