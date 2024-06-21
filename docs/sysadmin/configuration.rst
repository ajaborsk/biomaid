***************************************************************
Configuration
***************************************************************

.. _config_local:

Le dossier ``local`` :
----------------------

Le dossier ``local`` contient toutes les données utiles à l'adaptation de l'application |Project| pour l'adapter au
fonctionnement de votre établissement ou entité. Il est fortement conseillé d'utiliser le même dossier exactement
pour l'ensemble des instances utilisées dans l'établissement.

Si les différentes instances sont sur le même système de fichiers, cela peut se faire par un simple lien symbolique.

Toutefois, nous conseillons d'utiliser un dépôt *git* dédié (privé mais partagé par toutes les instances, par exemple
dans un dépôt privatif hébergé dans l'établissement ou dans un dépôt privé herbergé sur internet).

Les paragraphes qui suivent décrivent les différents sous-ensembles de la configuration ainsi que la façon de les utiliser.

Le fichier ``settings.py``
++++++++++++++++++++++++++

Ce fichier va comporter toutes les options de configuration de Django (et certaines options de |project|). C'est un fichier 
exécutable python, qui sera exécuté pour chaque instance de l'application.

Il est important de noter que ce fichier sera chargé **après** le fichier de configuration de base de |project| mais
**avant** le fichier de configuration de l'instance ``instance_settings.py`` qui est à la racine de l'application.

Cela signifie que les options de ce fichier pourront compléter ou écraser celles du fichier de configuration de base
(situé dans le dossier ``settings/__init__.py`` depuis la racine de l'application). Par contre, la configuration 
de l'instance pourra, à son tour, compléter ou écraser les options définies dans ce fichier ``settings.py``.

Les options utilisables ici sont toutes celles définies par Django et décrites dans sa documentation :
https://docs.djangoproject.com/fr/4.2/ref/settings/

Il s'agit de paramètres importants et qui peuvent être critiques, en particulier en ce qui concerne la sécurité de
l'application. Ne changez ces paramètres que si vous savez exactement ce que vous faites.

Voici quelques paramètres utiles et qui peuvent être ajustés sans risque :

``ADMINS`` 

``MANAGERS``

``INSTALLED_APPS``

Les paramètres suivants seront, dans une version ultérieure, transférés dans la configuration *toml* (cf. ci-dessous).
Dans l'intervalle, la seule façon d'ajuster leur fonctionnement est de modifier le code de ``settings.py``. A réaliser avec
prudence et, si possible, avec les conseils des développeurs initiaux. 

``BIOM_AID_THEMES``

``DEM_DEMANDE_CREATION_ROLES``

``BIOM_AID_PORTALS``

.. warning::
    Il est fortement déconseillé de définir dans ce fichier (susceptible d'être partagé) tous les
    paramètres qui comportent des mots de passe ou des données de sécurité comme : ``DATABASES``, ``SECRET_KEY`` ou tout 
    ce qui concerne la configuration de *LDAP*, par exemple. Même si ces paramètres sont identiques pour toutes les
    instances de l'application, il est préférable de les définir dans chaque ``instance_settings.py`` pour limiter
    les risques de diffusion involontaire (via le dépôt *git* ou autre).

Le fichier ``config.ini``
+++++++++++++++++++++++++

Le fichier ``config.toml`` et le dossier ``config.d``
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Le dossier ``static/local``
+++++++++++++++++++++++++++

Le dossier ``docs``
+++++++++++++++++++



Journaux (logs)
----------------

- Todo...

Messagerie
----------

- Todo...


LDAP
----

- Todo...

Templates (aspect)
------------------

- Todo...

Tâches périodiques (cronjobs)
-----------------------------

- Todo...

cron ... systemd timers ...