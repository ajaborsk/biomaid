***************************************************************
Installation
***************************************************************

Introduction
--------------

Le serveur |project| fonctionne sur la base d'un serveur Web Django (donc en python) avec une base de données.

Techniquement, il y a assez peu de contraintes qui limitent le choix du système d'exploitation,
le serveur WEB frontend (reverse proxy) et du SGBD.
Toutefois, pour simplifier, la documentation se base sur une configuration typique avec :

* Système d'exploitation Linux Ubuntu 22.04 LTS, qui inclut de base
  
  * python 3.10
  * git
  * curl
* Serveur Web ``nginx``
* SGBD PostgreSQL verstion 14

.. include:: doc_local/installation.rst
    :start-after: .. _prerequisites:
    :end-before: .. _

.. note::

    Cette procédure peut également s'appliquer à l'installation sur une machine windows avec WSL2 (qui est en fait
    un gestionnaire de machine virtuelle). Evidemment, il faudra choisir pour WSL2 une configuration "Ubuntu 22.04" !

Installation Linux 'standard'
-------------------------------

Ce chapitre décrit une installation complète d'une instance unique de |project| sur un serveur Linux/Ubuntu. Si plusieurs instances
doivent être installées sur la même machine, il faudra répéter la procédure autant de fois que nécessaire (sauf la première partie).

Système / distribution
++++++++++++++++++++++++++


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
**configuration minimale** suivante :

- 1 CPU/Core
- 2 Go RAM
- 20 Go de stockage

Toutefois, cette configuration, qui est suffisante pour une maquette ou une démonstration, est limitée pour un usage 
en production, pour laquelle la **configuration recommandée** est :

- 4 Cores
- 8 Go RAM
- 40 Go de stockage + 20 Go de stockage sur un disque différent pour les sauvegardes

Lors de l'installation d'Ubuntu (la méthode de lancement dépend de la machine, virtuelle ou non) :

- Choisissez le français comme langue principale du système. De cette façon, la configuration par défaut des services,
  et en particulier du gestionnaire de bases de données PostgreSQL, sera le français avec un encodage UTF-8,
- Choisissez un nom d'utilisateur pour vous (l'administrateur système). Dans la suite de cette documentation, 
  nous utiliserons le nom **`utilisateur`**. Cet utilisateur sera utilisé pour toutes les commandes d'administration par le biais
  de la commande `sudo` lorsque les droits de `root` seront nécessaires.
- Choisissez un nom de machine (le nom du serveur). Dans la suite de cette documentation, 
  nous utiliserons le nom **`serveur`**.  
- Validez l'installation de `ssh`. Que la machine soit virtuelle ou non, il est toujours utile de pouvoir y accéder à distance de 
  façon sécurisée,
- Ne demandez par l'installation de PostgreSQL proposée dans la liste des "Snaps". C'est une version ancienne
  (PostgreSQL 10) et nous utiliserons la version 14.
- Pour tout le reste, validez les options par défaut proposées par la distribution.

Une fois l'installation terminée (ce qui peut prendre quelques minutes), le système redémarre
(veillez à retirer le CD, virtuellement ou pas, du lecteur).

Connectez-vous une première fois sur la console avec le login `utilisateur`. Votre *prompt* doit être 

.. code:: console

    utilisateur@serveur:~$

A ce niveau, il est recommandé de faire une première mise à jour du système d'exploitation en tapant les commandes suivantes :

.. code:: console

    utilisateur@serveur:~$ sudo apt-get update
    utilisateur@serveur:~$ sudo apt-get upgrade

Donnez votre mot de passe lorsqu'il est demandé, acceptez toutes les options par défaut et validez toutes les boîtes de dialogue.

Après cela, il est conseillé, surtout si la mise à jour a concerné des paquets de base (comme `linux`, `systemd`, etc.)
de redémarrer une dernière fois la machine.

Les services du serveur
~~~~~~~~~~~~~~~~~~~~~~~

L'installation de PosgreSQL 14 et de nginx se fait en une seule étape (avec Ubuntu 22.04 ;
ce n'est pas nécessairement le cas des autres distributions)

L'installation des paquets se fait avec une seule commande :

.. code:: console

    utilisateur@serveur:~$ sudo apt-get install nginx postgresql gcc python3-dev libpq-dev

`nginx` 
   est le serveur HTTP(S) ; il sera utilisé en direct pour les fichiers simples (fichiers "statiques") et servira de 
   "reverse proxy" pour le serveur Django/gunicorn.
`postgresql`
   est le serveur de base de données de PostgreSQL et quelques bibliothèques pour l'utiliser,
`gcc`
   est le compilateur C, qui sera utilisé pour compiler les modules python depuis les sources 
   (notamment `psycopg2`, driver pour PosgreSQL).
`python3-dev`
   est la bibliothèque de développement pour Python 3, qui sera utilisée pour compiler les modules python depuis les sources 
   (notamment `psycopg2`, driver pour PosgreSQL).
`libpq-dev`
   est le paquet avec les bibliothèques de développement de PostgreSQL, nécessaire pour disposer de la dernière version
   du pilote python.

L'installation des paquets réalise également l'initialisation de la base de données primitive, l'activation et le lancement des
services `systemd` associés.

.. admonition:: Point d'étape

    A ce stade, vous devez donc avoir une machine virtuelle opérationnelle et à jour, à laquelle vous pouvez vous connecter 
    avec un utilisateur ayant les droits de `sudo` (pouvant exécuter des commandes système). Python 3.10 est disponible de base 
    sur cette machine (avec Ubuntu 22.04). Cette machine virtuelle comporte les services de base (PostgreSQL 14 et nginx) pour
    pouvoir installer des instances de |project|

Installation d'une instance de |project|
++++++++++++++++++++++++++++++++++++++++

.. admonition:: Objectif

    L'objectif de cette partie est d'installer une instance de |project| dans l'espace disque d'un utilisateur dédié et de
    configurer les services (base de données et serveur WEB) de façon à ce qu'elle soit techniquement fonctionnelle. Pour autant,
    il restera à configurer cette instance pour pouvoir l'utiliser.

Création de l'utilisateur
~~~~~~~~~~~~~~~~~~~~~~~~~

Le principe général est de créer un utilisateur par instance et installer dans son dossier personnel `$HOME` tout ce qui est 
nécessaire au fonctionnement de cette instance. Dans cette documentation, nous allons appeler cette instance et cet utilisateur 
*`instance`* mais vous pouvez la nommer comme vous le souhaitez et même en créer plusieurs, comme *`production`*, *`demo`*, 
*`test`*, *`evaluation`*, etc.

.. code:: console

    utilisateur@serveur~$ sudo adduser instance

Mis à part pour le mot de passe, qu'il faut définir, vous pouvez laisser vide les autres champs lorsque la question est posée.

.. note:: 

    Il n'est pas conseillé d'utiliser la commande ``useradd``, beaucoup plus primitive et qui demande d'ajuster beaucoup plus de 
    paramètres ultérieurement.

Configuration de l'instance dans la base de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On va maintenant créer l'utilisateur et la base de données dans PostgreSQL qui seront utilisés pour l'instance.

Pour commencer, il faut se connecter comme administrateur de la base de données (utilisateur ``postgres``) :

.. code:: console

    utilisateur@serveur~$ sudo su - postgres

Il faut ensuite créer l'utilisateur et la base de données associés à l'instance et donner à l'utilisateur en question les droits 
suffisants. Vous pouvez choisir les identifiants (et le mot de passe) à votre guise mais nous allons utiliser ici et dans la suite
``instance_db``, ``instance_user`` et ``instance_pwd``.

.. code:: console

    postgres@serveur:~$ createuser --createdb --pwprompt instance_user 
    Enter password for new role: 
    Enter it again: 
    postgres@serveur:~$ createdb --owner instance_user instance_db

Vous devez saisir deux fois le mot de passe (ici ``instance_pwd``).

Pour vérifier, on peut lancer l'interface en ligne de la base de données et lister les bases de données avec la commande ``\l``:

.. code:: console

    postgres@serveur~$ psql
    psql (14.9 (Ubuntu 14.9-0ubuntu0.22.04.1))
    Type "help" for help.

    postgres=# \l
                                         List of databases
        Name     |     Owner     | Encoding |   Collate   |    Ctype    |   Access privileges   
    -------------+---------------+----------+-------------+-------------+-----------------------
     instance_db | instance_user | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 | 
     postgres    | postgres      | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 | 
     template0   | postgres      | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 | =c/postgres          +
                 |               |          |             |             | postgres=CTc/postgres
     template1   | postgres      | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 | =c/postgres          +
                 |               |          |             |             | postgres=CTc/postgres
    (4 rows)

    postgres=# 
    postgres=# ^d
    postgres@serveur~$ ^d
    utilisateur@serveur~$ 

Création du dossier de l'instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Une fois l'utilisateur de l'instance créé et la base de données créée et configurée, vous pouvez vous connecter sous l'identité 
de l'utilisateur lié à l'instance :

.. code:: console

    utilisateur@serveur~$ sudo su - instance
    instance@serveur~$

Après avoir décidé du nom que vous donnerez à votre dossier de configuration locale 
(ici, on utilisera ``local_mon_ets`` pour l'exemple), installez le code depuis le dépôt et 
créez les trois dossiers qui hébergeront les données dynamiques de l'instance :

.. code:: console

    instance@serveur~$ git clone https://bitbucket.org/ajaborsk/biomaid.git
    instance@serveur~$ mkdir static media log

.. note::

    L'architecture du dossier de l'utilisateur propriétaire de l'instance comporte cinq dossiers :

    ``biomaid``
      c'est le dossier qui contient le code du logiciel. Mis à part un lien et le fichier de configuration principal,
      les fichiers de ce dossier ne devraient pas être modifiés pour une installation normale (sans développement).
    ``local_mon_ets``
      va contenir tous les fichiers de configuration qui sont spécifiques au site d'installation. Ce sont donc 
      les fichiers de ce dossier qu'il faudra modifier pour adapter |project| à votre établissement. Ce dossier
      peut éventuellement être partagé entre plusieurs instances (locales) et il est possible de le gérer comme un dépôt
      `git` pour bénéficier des fonctionnalités de cet outil.
    ``static``
      sera utilisé pour stocker les fichiers statiques (qui ne sont pas calculés "au vol") de l'application. Son
      contenu est généré par Django et il ne faut pas le modifier à la main
    ``media``
      va contenir tous les fichiers ajoutés par les utilisateurs de l'application ("pièces jointes"). Il sera nécessaire
      de sauvegarder son contenu lors des sauvegardes régulières.
    ``log`` 
      sera utilisé pour ranger les différents fichiers de "log" lors du fonctionnement de l'application. C'est ici 
      qu'il faudra venir des informations en cas de problème...

Initialisation de l'environnement d'exécution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toujours comme utilisateur de l'instance (``instance``), rendez-vous dans le dossier ``biomaid`` pour initialiser 
l'environnement d'exécution.

.. code:: console

    instance@serveur~$ cd biomaid
    instance@serveur~/biomaid$

Choisissez ensuite quelle version de |project| vous souhaitez installer et ajustez l'arbre de git en conséquence. Pour cette
documentation, nous allons installer la dernière version stable (branche ``stable``).

.. code-block:: console

    instance@serveur~/biomaid$ git checkout stable
    Branch 'stable' set up to track remote branch 'stable' from 'origin'.
    Switched to a new branch 'stable'
    instance@serveur~/biomaid$


.. note::

    Il peut y avoir plusieurs branches et plusieurs versions disponibles dans l'arbre *git*. On peut se caler (faire un *checkout*)
    sur une branche ou sur un *tag* précis créé par les développeurs. Il existe normalement un *tag* par version publiée de
    |project|. On peut en faire la liste avec la commande ``git tag --list``. Par ailleurs, les deux branches principales du projet
    sont ``stable``, qui doit normalement pointer sur la dernière version stable de |project| et ``main``, qui pointe vers la
    dernière version de développement (**à ne pas utiliser en production !**).

    Reportez-vous à la documentation de *git* : https://git-scm.com/doc pour plus de détails

Il faut maintenant installer le gestionnaire 'Poetry', qui va gérer les environnements virtuels python et surtout les 
dépendances de |project|. 

.. note::
    Il est important d'utiliser cette méthode pour installer poetry. Cette méthode est la seule permettant de faire des mises à jour
    de poetry lui-même sans perturber le fonctionnement de |project|.

    Vous pouvez trouver toutes les explications sur ce projet à cette adresse :
    https://github.com/python-poetry/install.python-poetry.org

.. code:: console

    instance@biomaid:~/biomaid$ curl -sSL https://install.python-poetry.org | python3 -
    Retrieving Poetry metadata

    # Welcome to Poetry!

    This will download and install the latest version of Poetry,
    a dependency and package manager for Python.

    It will add the `poetry` command to Poetry's bin directory, located at:

    /home/instance/.local/bin

    You can uninstall at any time by executing this script with the --uninstall option,
    and these changes will be reverted.

    Installing Poetry (1.7.0): Done

    Poetry (1.7.0) is installed now. Great!

    To get started you need Poetry's bin directory (/home/instance/.local/bin) in your `PATH`
    environment variable.

    Add `export PATH="/home/instance/.local/bin:$PATH"` to your shell configuration file.

    Alternatively, you can call Poetry explicitly with `/home/instance/.local/bin/poetry`.

    You can test that everything is set up by executing:

    `poetry --version`

    instance@biomaid:~/biomaid$ 

Comme le préconise le message d'installation, il faut maintenant ajouter ``/home/instance/.local/bin/`` dans le PATH 
de l'utilisateur ``instance``. C'est d'ailleurs une configuration qui pourra être utile par la suite pour d'autres outils.

Pour ce faire, le plus simple est d'ajouter à la fin du fichier ``/home/instance/.bashrc`` (fichier exécuté à chaque connexion) 
la commande ``export PATH="/home/instance/.local/bin:$PATH"``, comme indiqué. Vous pouvez utiliser l'éditeur ``nano``, qui est présent
sur toutes les distributions modernes et facile d'utilisation :

.. code-block:: console

    instance@biomaid:~/biomaid$ nano ~/.bashrc

Allez à la fin du fichier et ajoutez sur une nouvelle ligne la commande ``export PATH="/home/instance/.local/bin:$PATH"``.

Vous pouvez sauvegarder et quitter ``nano`` en tapant ``ctrl-s`` puis ``ctrl-x`` (parfois abrégé en ``^s`` ``^x``).

Activez ensuite le fichier (lors de vos prochaines connexions, cela se fera automatiquement) :

.. code-block:: console

    instance@biomaid:~/biomaid$ source ~/.bashrc

N'hésitez pas à consulter la documentation de ce script d'installation de poetry : 
https://github.com/python-poetry/install.python-poetry.org et à la documentation de l'outil poetry lui-même : 
https://python-poetry.org/docs/

La configuration poetry de |project| comporte trois groupes de dépendances et deux "extensions" (groupes de dépendances 
optionnelles). Les groupes de dépendances sont :

- **docs** : Outils nécessaires à la création de la documentation (*html* et *pdf*) à partir des sources 
  (inclus dans l'arbre *git*). Il est recommandé d'installer les dépendances de ce groupe, même pour la production.
- **tests** : Outils nécessaires à l'exécution des tests de régression. Il n'est pas recommandé d'installer ce groupe en production.
- **dev** : Outils nécessaires pour le développement. Il n'est pas recommandé d'installer ces dépendances pour la production.

Les dépendances optionnelles sont :

- **oracle** : Bibliothèques pour accéder directement à une base de données Oracle (pour la GMAO Asset+). Cela demande aussi 
  l'installation de fichiers dans le système d'exploitation.
- **ldap** : Bibliothèques pour accéder au LDAP (Advance Directory par exemple) institutionnel 
  (notamment pour la gestion des mots de passe). 

Pour installer, par exemple, les dépendances d'une version de production sans aucune dépendance optionnelle :

.. code:: console

    instance@biomaid:~/biomaid$ poetry install --no-root --without=dev --without=tests

.. note::

    L'option ``--no-root`` sert à indiquer à poetry que |Project| n'est pas une bibiothèque python et qu'il n'y a donc pas
    de fichiers python à installer dans le dossier des bibliothèques python de l'environnement virtuel. Il faut juste installer les
    dépendances.

Pour installer les dépendances d'une version de développement avec la connexion Oracle :

.. code:: console

    instance@biomaid:~/biomaid$ poetry install --no-root -E oracle

Création du dossier de configuration locale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'ensemble des données de configuration d'une installation de |project| est rangé dans un dossier unique, qui pourra être copié
pour configurer différentes instances (production, test, développement, etc.) ou, mieux encore, installé dans un dépôt *git* dédié.
Ce dépôt pourra être, par exemple, hébergé comme un dépôt privé dans un *hub* public (gituh.com, gitlab.com, bitbucket.org...) 
ou dans un gestionnaire de dépôt privé de l'établissement. Cette option permet de bénéficier des avantages d'un dépôt *git*, et 
notamment la possibilité de travailler à plusieurs, de tester des configurations dans des *branches* dédiées et surtout d'avoir
un historique complet (et réversible) de toutes les modifications.

Le plus simple, pour créer ce dossier local, est de copier le dossier de configuration locale de la version de démo (qui est inclus
dans le dépôt *git* public des sources) :

.. code-block:: console

    instance@biomaid:~/biomaid$ cp -R local_biomaid ../local_mon_ets

En remplaçant ``local_mon_ets`` par un nom de dossier spécifique à votre établissement.

Il faut ensuite faire un lien symbolique de ce dossier vers le dossier `local` de l'arbre des sources :

.. code-block:: console

    instance@biomaid:~/biomaid$ ln -sf ../local_mon_ets local

Initialisation de l'application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'avant dernière étape à mettre en oeuvre avant de pouvoir lancer une instance, c'est de créer le fichier de configuration de 
l'instance. Ce fichier, qui est placé à la racine de l'application (dans le dossier ``biomaid``), est toujours nommé 
``instance_settings.py``. Ce fichier n'est pas disponible dans le dépôt car c'est le fichier qui va contenir toutes les options 
spécifiques à cette instance et en particulier tous les mots de passe et les clés secrètes.

La distribution comporte néanmoins un fichier d'exemple, qu'on peut copier et modifier pour créer un fichier de configuration 
d'instance :

.. code:: console

    instance@biomaid:~/biomaid$ cp example_instance_settings.py instance_settings.py
    instance@biomaid:~/biomaid$ nano instance_settings.py

Les modifications minimales à faire pour avoir une instance opérationnelle sont :

- Indiquer le nom de l'hôte qui héberge le serveur (par défaut, seul un accès en local ``localhost`` est possible). C'est le nom qui
  sera utilisé pour accéder au serveur depuis le navigateur des utilisateurs. Ainsi, si votre VM est accessible à l'adresse IP
  192.168.122.128 ou sous le nom 'serveur.local' pour les utilisateurs, vous devez ajouter '192.168.122.128' et/ou 'serveur.local'
  à la liste ``ALLOWED_HOSTS``.
- Choisir une valeur de ``DEBUG`` : Choisir ``False`` pour une instance de production ou de test et ``True`` pour une instance de
  développement.
- Configurer l'accès à la base de données PostgreSQL avec les identifiants définis plus haut (``instance_db``, ``instance_user`` et 
  ``instance_pwd`` ici)
- Changer la clé secrète ``SECRET_KEY`` pour une instance de production. Le site https://djecrety.ir/ permet de générer une clef 
  secrète facilement, par exemple.

Le résultat (le fichier ``~/biomaid/instance_settings.py``) pourra ressembler à cela :

.. code-block:: python

    #  Copyright (c) 2020-2023 Brice Nord, Romuald Kliglich, Alexandre Jaborska.
    #  This file is part of the BiomAid distribution.
    #  This program is free software: you can redistribute it and/or modify
    #  it under the terms of the GNU General Public License as published by
    #  the Free Software Foundation, version 3.
    #  This program is distributed in the hope that it will be useful, but
    #  WITHOUT ANY WARRANTY; without even the implied warranty of
    #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    #  General Public License for more details.
    #  You should have received a copy of the GNU General Public License
    #  along with this program. If not, see <http://www.gnu.org/licenses/>.

    import logging

    from settings import DEBUG_TOOLBAR, MIDDLEWARE, INSTALLED_APPS

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
    logging.getLogger(__name__).info("Example instance.")

    DEFAULT_DOMAIN = 'http://localhost:8000'

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
    ]

    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    SMARTVIEW_DEBUG = DEBUG

    AUTHENTICATION_BACKENDS = ('common.auth_backends.MyAuthBackend',)

    if DEBUG_TOOLBAR:
        INSTALLED_APPS += [
            'debug_toolbar',
        ]
        MIDDLEWARE = [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ] + MIDDLEWARE
        INTERNAL_IPS = [
            # ...
            '127.0.0.1',
            # ...
        ]

    INSTALLED_APPS += []

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '1zjt*b2da6b4vc22@yirnix1w!&#$&hk08yh31%^hv2@)05h)6'

    DATABASES = {
        # For a demonstration instance, the easiest is to use a SQLite3 database
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': 'db.sqlite3',
        # },
        # But you could also use a PostgreSQL server if you want !
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'instance_db',
            'USER': 'instance_user',
            'PASSWORD': 'instance_pwd',
            'HOST': 'localhost',
            'PORT': '',
        },
        # Asset+ SQL/Oracle access ; use with care...
        # 'gmao': {
        #     'ENGINE': 'oraclenvc',
        #     'NAME': 'your_asset_plus_db_name',
        #     'USER': 'your_asset_plus_db_user',
        #     'PASSWORD': 'your_asset_plus_db_password',
        #     'HOST': 'your_asset_plus_db_server_name',
        #     'PORT': 'your_asset_plus_db_server_port',
        # },
    }

    # local email tests on port 8025 (using aiosmtpd python module)
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT = 8025

    MEDIA_ROOT = '../media'


Une fois ce fichier créé, il doit être possible de rentrer dans l'environnement virtuel et de lancer l'application 
et en particulier la première commande :

.. code-block:: console

    instance@biomaid:~/biomaid$ poetry shell
    (biomaid-py3.10) instance@serveur:~/biomaid$ python manage.py migrate

La commande peut mettre un certain temps à s'exécuter. Elle va créer toutes la structure de la base de données nécessaire à
l'exécution de l'application django |project|.

.. admonition:: Point d'étape

    A partir de ce point, le code de l'instance doit être opérationnel. Il doit en particulier être possible de lancer un 
    serveur de test avec la commande ``python manage.py runserver --insecure 0.0.0.0:8000``.

    Vous pouvez même faire un essai avec la base de tests :

    .. code:: console

        (biomaid-py3.10) instance@serveur:~/biomaid$ python manage.py loaddata fixtures/tests_db.json
        (biomaid-py3.10) instance@serveur:~/biomaid$ python manage.py runserver --insecure 0.0.0.0:8000
    
    Et revenir à une base vide après avoir arrêté le serveur :

    .. code:: console

        (biomaid-py3.10) instance@serveur:~/biomaid$ python manage.py reset_db
        (biomaid-py3.10) instance@serveur:~/biomaid$ python manage.py migrate


Ajout de l'instance dans la configuration système
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo::

    nginx

    installation service 

    collectstatics

    systemd start/enable


Configuration d'une instance de |project|
+++++++++++++++++++++++++++++++++++++++++

.. admonition:: Objectif

    L'objectif de cette partie est de configurer une instance de |project|. Cela correspond à la modification des fichiers 
    de configuration pour adapter l'instance au fonctionnement souhaité. Il va s'agit par exemple des noms de champs, des 
    textes, des couleurs, du logo, des importations automatiques, etc. Il est possible de faire cette configuration autant de 
    fois que nécessaire et de relancer le serveur `gunicorn` pour l'activer.

Installation d'une maquette sous Linux
--------------------------------------

Installation d'une maquette sous Windows
----------------------------------------

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

Installation avec des containers
--------------------------------

.. include:: doc_local/installation.rst
    :start-after: .. _containers:
    :end-before: .. _

**Ce mode d'installation n'est pas encore pris en charge**

.. image:: containers.*

- Todo...

