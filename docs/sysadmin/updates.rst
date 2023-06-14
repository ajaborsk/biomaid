--------------------------------
Mises à jour
--------------------------------

.. todo::

    On pourrait sans doute faire un script (shell ou python) avec cette procédure, avec retour automatique à la sauvegarde si tout ne se passe pas bien...
    Ce serait, en plus, plus rapide (probablement moins d'une minute).

.. note::

    Il est (très) prudent de faire cette procédure sur l'instance de test avant de la lancer sur l'instance de production...

Informer les utilisateurs
=========================

Ou au moins choisir un créneau de très faible utilisation de l'instance

.. include:: doc_local/updates.rst
    :start-after: .. _users_inform_before:
    :end-before: .. _

Arrêter l'instance
==================

Cela se fait par l'arrêt du service ``gunicorn`` via ``supervisor``

::

    > sudo service supervisor stop

.. include:: doc_local/updates.rst
    :start-after: .. _instance_stop:
    :end-before: .. _

Activer l'environnement virtuel adéquat
=======================================

Aller dans le dossier de l'instance et lancer la commande :

::

    > poetry shell

Faire une sauvegarde des données
================================

- Les données de la base
  
à partir de la version 0.13 :

::

    > python manage.py backup 

Versions antérieures à 0.13 :

Si ``the_file_name`` est le nom de la sauvegarde :

::

    > python manage.py dumpdata -a --natural-foreign -e assetplusconnect -e extable -e admin.Logentry -e contenttypes -e sessions -e auth.Permission -o ~/the_file_name.json.bz2

- Les fichiers ``media``

Uniquement si c'est nécessaire

- La configuration locale (dossier ``/local``)

Uniquement si c'est nécessaire

.. note::

    Dans la grande majorité des cas, la mise à jour ne concerne que le code et la structure de la base
    de données. La sauvegarde spéciquement à ce moment des fichiers de ``/media`` et de ``/local`` est à l'appréciation
    de chacun. D'autant plus que pour ``/media``, le volume de données peut être très important. Dans tous les cas,
    pour ce dossier, il est conseillé un système de sauvegarde différentiel ou incrémentiel.

.. include:: doc_local/updates.rst
    :start-after: .. _backup:
    :end-before: .. _

Installer le nouveau code BiomAid
=================================

Si #.#.# est le nom du tag de la version à installer (0.8.1 par exemple) :

::

> git checkout #.#.#


Installer le nouveau code local
===============================

Cela peut ne pas être nécessaire, mais il est fréquent que de nouvelles fonctionnalités nécessitent 
des configurations ou paramétrages locaux pour fonctionner parfaitement.

Les modalités dépendent de la stratégie locale (dépôt en ligne, simple dossier, etc.)

Typiquement, cela se fait en allant dans le dossier sur lequel pointe ``local/`` et en tapant la commande :

::

    > git pull

.. include:: doc_local/updates.rst
    :start-after: .. _local_dir_update:
    :end-before: .. _



Faire la mise à jour des dépendances
====================================

::

> poetry install --no-root -E ldap

.. include:: doc_local/updates.rst
    :start-after: .. _code_install:
    :end-before: .. _

Lancer les migrations
=====================

::

> python manage.py migrate

Installer les fichiers statiques
================================

::

> python manage.py collectstatic


Adapter éventuellement le ``instance_settings.py``
==================================================

Selon la mise à jour (ce n'est pas toujours utile)

Il peut aussi être utile d'ajuster le ``instance_config.toml`` 

Relancer l'instance
===================

Les modalités dépendent de la stratégie locale mais cela implique généralement de lancer le démon
qui gère ``gunicorn`` :

::

    > sudo service supervisor start

.. include:: doc_local/updates.rst
    :start-after: .. _instance_launch:
    :end-before: .. _

Informer les utilisateurs
=========================

- Que le serveur est relancé
- Quelles sont les (principales) nouveautés

.. todo::
    - Sans doute faire une information différente suivant le type d'utilisateur (ses rôles) ?
    - Intégrer cela à l'interface (box d'info à la connexion) ?

.. include:: doc_local/updates.rst
    :start-after: .. _users_inform_after:
    :end-before: .. _

