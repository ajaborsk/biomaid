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

Arrêter l'instance
==================

Cela se fait par l'arrêt du service gunicorn via supervisor

Activer l'environnement virtuel adéquat
=======================================

Aller dans le dossier de l'instance et lancer la commande :

    poetry shell

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

- La configuration locale (dossier ``/locale``)

Uniquement si c'est nécessaire

.. note::

    Dans la grande majorité des cas, la mise à jour ne concerne que le code et la structure de la base
    de données. La sauvegarde spéciquement à ce moment des fichiers de ``/media`` et de ``/local`` est à l'appréciation
    de chacun. D'autant plus que pour ``/media``, le volume de données peut être très important. Dans tous les cas,
    pour ce dossier, il est conseillé un système de sauvegarde différentiel ou incrémentiel.

Installer le nouveau code
=========================

Si #.#.# est le nom du tag de la version à installer (0.8.1 par exemple) :

::

> git checkout #.#.#


Faire la mise à jour des dépendances
====================================

::

> poetry install --no-root -E ldap



Lancer les migrations
=====================

::

> python manage.py migrate

Installer les fichiers statiques
================================

::

> python manage.py collectstatic

Relancer l'instance
===================

Informer les utilisateurs
=========================

- Que le serveur est relancé
- Quelles sont les (principales) nouveautés

.. todo::
    - Sans doute faire une information différente suivant le type d'utilisateur (ses rôles) ?
    - Intégrer cela à l'interface (box d'info à la connexion) ?

