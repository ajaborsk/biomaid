---------------------------
Installation
---------------------------

.. include:: doc_local/installation.rst
    :start-after: .. _containers:
    :end-before: .. _

Introduction
------------

Le serveur |project| fonctionne sur la base d'un serveur Web Django (donc en python) avec une base de données.

Techniquement, il y a assez peu de contraintes qui limitent le choix du système d'exploitation,
le serveur WEB frontend (reverse proxy) et du SGBD.
Toutefois, pour simplifier, la documentation se base sur une configuration typique avec :

- Système d'exploitation Linux Ubuntu 22.04 LTS
- Serveur Web ``nginx``
- SGBD PostgreSQL verstion 14
- Python 3.10

.. include:: doc_local/installation.rst
    :start-after: .. _prerequisites:
    :end-before: .. _

Installation d'une maquette sous Linux
--------------------------------------

Installation d'une maquette sous Windows
----------------------------------------

Installation Linux 'standard'
-----------------------------

Ce chapitre décrit une installation complète d'une instance unique de |project| sur un serveur Linux/Ubuntu. Si plusieurs instances
doivent être installées sur la même machine, il faudra répéter la procédure autant de fois que nécessaire (sauf la première partie).

Système / distribution
++++++++++++++++++++++


.. admonition:: Objectif

    L'objectif de cette première partie est de disposer d'une machine (virtuelle ou non) disposant des paquets nécessaires 
    à l'installation complète de |project|.

Les commandes décrites correspondent à l'utilisation d'une distribution Ubuntu 22.04 (LTS) mais l'installation est facilement 
adaptable à d'autres distributions (ArchLinux et AlmaLinux ont été testées avec succès).

Système d'exploitation
~~~~~~~~~~~~~~~~~~~~~~

A la date d'écriture de ces lignes, la dernière version d'Ubuntu LTS (Long Term Support) est la 22.04.3.

L'image disque d'installation est disponible à l'adresse suivante : https://releases.ubuntu.com/jammy/.

Cette version dispose déjà de python 3.10 (commande `python3`), qui convient à |project|.

|project| n'est pas très exigeant en terme de configuration technique. Il a été installé sans problème sur une machine avec la 
configuration minimale suivante :

- 1 CPU/Core
- 2 Go RAM
- 20 Go de stockage

Toutefois, cette configuration, qui est suffisante pour une maquette ou une démonstration, est limitée pour un usage 
en production, pour laquelle la configuration recommandée est :

- 4 Cores
- 8 Go RAM
- 40 Go de stockage + 20 Go de stockage sur un disque différent pour les sauvegardes

Lors de l'installation d'Ubuntu (la méthode de lancement dépend de la machine, virtuelle ou non) :

- Choisissez un nom de machine (le nom du serveur). Dans la suite de cette documentation, 
  nous utiliserons le nom **`biomaid-server`**.
- Choisissez un nom d'utilisateur pour vous (l'administrateur système). Dans la suite de cette documentation, 
  nous utiliserons le nom **`user`**. Cet utilisateur sera utilisé pour toutes les commandes d'administration par le biais
  de la commande `sudo` lorsque les droits de `root` seront nécessaires.
- Validez l'installation de `ssh`. Que la machine soit virtuelle ou non, il est toujours utile de pouvoir y accéder à distance de 
  façon sécurisée
- Ne demandez par l'installation de PostgreSQL proposée dans la liste initiale des serveurs. C'est un version ancienne
  (PostgreSQL 10) et nous utiliserons la version 14.
- Pour tout le reste, validez les options par défaut proposées par la distribution.

Une fois l'installation terminée (ce qui peut prendre quelques minutes), le système redémarre
(veillez à retirer le CD, virtuellement ou pas, du lecteur).

Connectez-vous une première fois sur la console avec le login `user`. Votre *prompt* doit être `user@biomaid-server:~$`.

A ce stade, il est recommandé de faire une première mise à jour du système d'exploitation en tapant les commandes suivantes :

.. code:: shell

    user@biomaid-server:~$ sudo apt-get update
    user@biomaid-server:~$ sudo apt-get upgrade

Acceptez toutes les options par défaut et validez toutes les boîtes de dialogue.

A ce stade, il est conseillé, surtout si la mise à jour a concerné des paquets de base (comme `linux`, `systemd`, etc.)
de redémarrer une dernière fois la machine.

.. admonition:: Point d'étape

    A ce stade, vous devez donc avoir une machine virtuelle opérationnelle et à jour, à laquelle vous pouvez vous connecter 
    avec un utilisateur ayant les droits de `sudo` (pouvant exécuter des commandes système). Python 3.10 est disponible de base 
    sur cette machine (avec Ubuntu 22.04).

Gestionnaire de base de données (SGBD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Serveur WEB
~~~~~~~~~~~

nginx ... apache ? ...




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
