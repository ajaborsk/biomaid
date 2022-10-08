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

Chaque application peur définir ses propres sections dans chaque document.

Par exemple, dans l'application `dem`, il y a un répertoire `docs` qui contient lui-même un dossier `internals`.
Ce dossier (et la documentation qu'il contient) sera ajouté au document global **internals**
par la commande `make_docs`.

.. note::
    Il faudrait un exemple plus clair ici !