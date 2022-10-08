---------------------------
Installation
---------------------------

Prérequis
---------

Le serveur BIOM_AID fonctionne sur la base d'un serveur Web Django (donc en python) avec une base de données.

Techniquement, il y a assez peu de contraintes qui limitent le choix du système d'exploitation,
le serveur WEB frontend (reverse proxy) et du SGBD.
Toutefois, pour simplifier, la documentation se base sur une configuration typique avec :

- Système d'exploitation Linux Ubuntu 20.04 LTS
- Serveur Web ``nginx``
- SGBD PostgreSQL verstion 12

.. include:: ../../local/docs/sysadmin/installation.rst
    :start-after: .. _prerequisites:
    :end-before: .. _

Installation depuis un dépôt
----------------------------

- Todo...

Système / distribution
++++++++++++++++++++++

Linux ... Ubuntu ... Windows ...

SGBD
++++

PostgreSQL ... SQLite ... MySQL/MariaDB ? ... Autre (Oracle ?) ...

Serveur WEB
+++++++++++

nginx ... apache ? ...

gunicorn
++++++++



Installation avec des containers
--------------------------------

.. image:: containers.*

- Todo...


