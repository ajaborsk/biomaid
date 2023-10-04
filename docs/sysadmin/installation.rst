---------------------------
Installation
---------------------------

.. include:: doc_local/installation.rst
    :start-after: .. _containers:
    :end-before: .. _

Prérequis
---------

Le serveur |project| fonctionne sur la base d'un serveur Web Django (donc en python) avec une base de données.

Techniquement, il y a assez peu de contraintes qui limitent le choix du système d'exploitation,
le serveur WEB frontend (reverse proxy) et du SGBD.
Toutefois, pour simplifier, la documentation se base sur une configuration typique avec :

- Système d'exploitation Linux Ubuntu 20.04 LTS
- Serveur Web ``nginx``
- SGBD PostgreSQL verstion 12

.. include:: doc_local/installation.rst
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

**Ce mode d'installation n'est pas encore pris en charge**

.. image:: containers.*

- Todo...

Installation multiple (plusieurs instances sur un seul serveur)
---------------------------------------------------------------

Ce mode d'installation permet d'installer plusieurs instances de BiomAid sur un serveur unique. Il peut s'agir, par exemple,
d'une instance de production, d'une instance de test et d'une instance de démonstration ou d'instances pour différentes entités
juridiques. Dans tous les cas, ces instances sont complètement indépendantes, mise à part le fait qu'elle partagent un même système
d'exploitation et les mêmes ressources physiques.

Le principe consiste à créer et installer un utilisateur par instance.

Cette documentation est prévue pour un système utilisant `systemd` comme mécanisme de gestion des services.

Installation du serveur
+++++++++++++++++++++++

Installation et configuration de PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO...

Installation et configuration de nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO...

Cas d'un serveur avec SELinux
+++++++++++++++++++++++++++++

Les serveurs basés sur une distribution RedHat (CentOS, Almalinux, ...) sont par défaut configurés avec le système de sécurité
SELinux. Ce système apporte des sécurités supplémentaires, mais l'installation de BiomAid demande l'installation de quelques
politiques de sécurité complémentaires.

TODO...

Installation d'une instance
+++++++++++++++++++++++++++

TODO...
- Créer l'utilisateur `demo` : sudo adduser
