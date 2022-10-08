================================================
Description du fonctionnement interne de BiomAid
================================================

Ce chapitre décrit les structures et les procédures internes de BIOM_AID.

Introduction
============

On peut voir une instance de serveur <biomAid> comme une pile de 4 couches assez indépendantes les unes des autres (même si
chaque couche dépend nécessairement des couches inférieures, au moins pour leur structure) :

.. image:: stack.*

- Le "système" est le système d'exploitation (ou à l'avenir des containers, des pods voire des kubernetes).
  C'est normalement une machine virtuelle Linux, Ubuntu 20.04, avec tous les packages nécessaires au bon fonctionnement
  du serveur (nginx, gunicorn...). Il peut être (re)créé à partir d'images ou de dépôts publics et librement accessibles
  sur internet.

- BIOM_AID est un peu le moteur du serveur. C'est un projet Django et un ensemble d'applications Django dont les
  fonctionnalités sont décrites dans ce chapitre. Il peut être (re)créé à partir du dépôt de biom_aid (privé pour le moment)
  ou des packages distribués (par les auteurs ?).

- L'instance locale est l'ensemble des templates (pour l'aspect du ou des sites), les portails, la configuration (les
  fonctionnalités actives, les différents paramètres, etc.). Elle est normalement complètement contenue dans le dossier
  `local/` de l'application et peut être (re)créée à partir d'une simple copie de ce dossier.

- Les données, composées du contenu de la base de données et des fichiers (contenus dans le dossier `media/`). Ces données
  peuvent être (re)créées à partir des sauvegardes régulières configurées par l'administrateur système.

Les applications BiomAid
========================

.. toctree::
   :maxdepth: 2
   :caption: Contenu :

   doc_common/index
   doc_dem/index
   doc_smart_view/index
   doc_finance/index


**à compléter...**
