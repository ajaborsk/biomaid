Documentation du projet
=======================

BIOM_AID utilise `Sphinx <https://www.sphinx-doc.org/en/master/#>`_  comme générateur de documentation et le module
`autoapi` pour générer automatiquement la documentation des API.

La commande Django `make_docs`, à lancer à chaque mise à jour, regénère automatiquement toute
la documentation au format HTML et sous forme de documents PDF à partir des
applications (modules) installés.

La documentation principale se trouve dans le dossier `docs/` à la racine du projet.
Elle est composée de 5 documents différents :

*  **user** : Document destiné aux utilisateurs du portail
*  **internals** : Document qui explique le fonctionnement interne de BIOM_AID et des différentes applications. Il peut
   être utilisé par les développeurs, les administrateurs ou même les utilisateurs avancés.
*  **admin** : Document destiné au responsable du portail (le référent du logiciel,
   qui peut modifier la configuration globale)
*  **dev** : Document destiné aux développeurs (du noyau ou des applications)
*  **sysadmin** : Document destiné à l'administrateur système, celui qui installe le logiciel (typiquement
   celui qui a les droits du superutilisateur ou root sur le serveur).

La documentation principales est rédigée dans le dossier `docs` de la hiérarchie principale du projet.

Documentation des différentes applications de BiomAid
-----------------------------------------------------

Chaque application peur définir ses propres sections dans chaque document.

Par exemple, dans l'application `dem`, il y a un répertoire `docs` qui contient lui-même un dossier `internals`.
Ce dossier (et la documentation qu'il contient) sera ajouté au document global **internals**
par la commande `make_docs`.

.. note::
    Il faudrait un exemple plus clair ici !

Documentation locale
--------------------

Il est possible (et même conseillé) de compléter la documentation des applications par de la documentation
spécifique au site d'installation.

Ce mécanisme permet de créer des guides spécifiques à la plateforme, là où elle est installée. C'est particulièrement utile pour
le guide de l'utilisateur ou pour préciser certains détails des autres documentations.

Cela se fait par l'insertion (réalisée automatiquement par la commande
`python manage.py make_docs`) de blocs spécifiques à l'utilisation locale à n'importe quel point de la documentation générique.

Par exemple, la documentation générique va inclure dans la section "installation via un dépôt" une partie de documentation (si elle existe)
qui sera dans le fichier local/docs/sysadmin/install.rst entre la balise `.. _repository:` et la balise suivante.

Il existe de nombreux points d'insertion dans la documentation générique et il est évidemment possible d'en ajouter autant
que nécessaire.

.. warning::
    Même si cela peut être tentant, il faut absolument éviter d'intégrer dans cette partie de la
    documentation des mots de passe ou d'autres données confidentielles !
