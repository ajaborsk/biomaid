*************************
Documentation du projet
*************************

|project| utilise `Sphinx <https://www.sphinx-doc.org/en/master/#>`_  comme générateur de documentation et le module
`autoapi` pour générer automatiquement la documentation des API.

La commande Django `make_docs` (`python manage.py make_docs`), à lancer à chaque mise à jour, regénère automatiquement toute
la documentation au format HTML et sous forme de documents PDF à partir des
applications (modules) installés.

.. admonition:: Le saviez-vous ?

    Le principe fondamental est de pouvoir générer une documentation complète et adaptée à chaque instance de |project|.

    Il s'agit en particulier de créer une documentation :

    - Avec toute la documentation des modules installés et seulement des modules installés
    - Avec toutes les spécificités locales d'utilisation du logiciel (comme les règles d'utilisation de certains champs ou les processus locaux)

La documentation principale se trouve dans le dossier `docs/` à la racine du projet.
Elle est composée de 5 documents différents :

*  **user** : Document destiné aux utilisateurs du portail
*  **internals** : Document qui explique le fonctionnement interne de |project| et des différentes applications. Il peut
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

.. todo::
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

Dans le fichier principal (ici `documentation.rst`), il faut donc intégrer à la fin de chaque paragraphe un point d'insertion :

.. code-block:: rest
    :caption: Exemple de point d'insertion dans le fichier de documentation principal `documentation.rst`, à la fin du paragraphe identifié `paragraph` (extrait du fichier `documentation.rst`)

    Paragraphe
    ----------

    Documentation relatif au paragraphe etc.

    .. include:: doc_local/documentation.rst
        :start-after: .. _paragraph:
        :end-before: .. _

Dans le fichier local, il faut créer un fichier nommé aussi `documentation.rst`, dans lequel on retrouve toutes les sections à insérer :

.. code-block:: rest
    :caption: Exemple de texte à insérer dans le fichier de documentation local `documentation.rst`, à la fin du paragraphe identifié `paragraph` (extrait du fichier `local/documentation.rst`)

    .. _paragraph:

        .. admonition:: Pour le cas de notre instance de BiomAid:

            Ici, on fait comme cela...

    .. _next_paragraph:
        ...

Le lien entre `local/` et `doc_local/` est fait automatiquement par la commande Django `make_docs`.

La documentation générée sera identique à celle qui aurait été générée si le texte de `documentation.rst` avait été :

.. code-block:: rest
    :caption:  Fichier de documentation `documentation.rst`, paragraphe `paragraph`, code généré

    Paragraphe
    ----------

    Documentation relatif au paragraphe etc.

    .. admonition:: Pour le cas de notre instance de BiomAid:

        Ici, on fait comme cela...

Chaque fichier de documentation locale doit impérativement se terminer par une pseudo directive

.. code-block:: rest
    :caption: texte à insérer à la fin de chaque fichier de documentation locale, pour délimiter la dernière section à insérer (extrait du fichier `doc_local/documentation.rst`)

    .. _end-of-file:



Documentation conditionnelle
----------------------------

Grâce à l'utilisation de `tag` (cf. `documentation de Sphinx sur la directive *only* <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-only>`_), 
il est possible d'insérer dans la documentation des parties qui ne seront affichées/créée que si certaines conditions sont vraies.

Applications Django / Modules |project|
+++++++++++++++++++++++++++++++++++++++

En plus des tags générés automatiquement par Sphinx (format et moteur), la commande `make_docs` 
va créer un tag pour chaque module (app) actif dans l'application |project|. Chacun de ces tags est composé du préfixe `djangoapp_` et 
du nom de l'application complet, avec les éventuels '.' remplacés par des '_'. Ainsi, si l'application `dem` est active, le tag `djangoapp_dem` sera vrai
et si l'application `django.contrib.contenttypes` est active, le tag `djangoapp_django_contrib_contenttypes` sera vrai.

Options
+++++++

Il est aussi possible d'ajouter des tags dans les fichiers de configuration TOML pour documenter certaines
fonctionnalités optionnelles. On peut penser par exemple à l'utilisation (ou non) de certaines interfaces vers 
magh2 et/ou Asset+ et/ou autre chose...

Les tags d'option sont définis à partir des entrées de configuration dans le dictionnaire `options`. Par exemple, si un des fichiers de configuration comporte
une section `options`:

.. sourcecode:: toml

    [options]
    magh2_orders = true

Cela définira le tag `option_magh2_orders` pour la génération de la documentation.

.. sourcecode:: rest

    .. only:: option_magh2_orders

        Paragraphe conditionnel
        -----------------------

        Visible seulement si le tag 'option_magh2_orders' est vrai

        .. note::

            On peut mettre des directives dans une section conditionnelle aussi

    .. only:: not option_magh2_orders

        Paragraphe conditionnel
        -----------------------

        Visible seulement si le tag 'option_magh2_orders' est faux

