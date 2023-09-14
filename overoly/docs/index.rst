Overoly
=======

Overoly est une bibiothèque (pas une application) pour Django (4+) qui permet d'ajouter des fonctionnalités au niveau
des modèles :

- Ajout de champs calculés 'en ligne' (non stockés dans la base), avec gestion des dépendances
- Ajout d'un système de gestion souple d'attributs pour les champs
- Gestion fine des droits (par enregistrement et par champ), basée sur un mécanisme flexible de rôles
- Notion (facultative) d'objets 'actifs' vs. 'désactivés' systématique
  
La totalité de ces fonctionnalités est paramétrable via un attribut des modèles mais aussi grâce
à une configuration sous forme de dictionnaire, permettant d'utiliser facilement un fichier de configuration externe.

La grande majorité de la surcharge de calcul liée à ces nouvelles fonctionnalités est concentrée au lancement
(grâce à l'utilisation de métaclasses), limitant les pertes de performances lors du fonctionnement du serveur.

Utilisation d'Overoly
---------------------

Pour qu'un modèle puisse bénéficier des fonctionnalités d'Overoly, il suffit
de le faire hériter de la classe OModel :

.. code:: python

    from django.db.models import CharField
    from overoly.base import OModel, OField

    class MonModele(OModel):

        class OMeta:
            pass

        normal_field = CharField()
        computed_field = OField()

Les nouveaux 'Manager' :
------------------------

.. note:: 

    Expliquer comment fonctionnent les nouveaux manager () et pourquoi les manager par défault `objects` ne sont plus disponibles.

    Expliquer la méthode `setup()` des nouveaux managers.

Gestion des attributs :
-----------------------

.. note::

    Expliquer le fonctionnement (avec des exemples et comment on s'en sert)

Configuration externe :
-----------------------

.. note:: 
    Expliquer le fonctionnement de l'attribut `config` de la classe `OMeta` et donner un 
    exemple d'utilisation avec un fichier de configuration externe type `toml`

Roles, états et permissions :
-----------------------------

C'est la partie la plus complexe, mais aussi la plus puissante. Elle repose notamment sur les champs calculés.

C'est ce qui permet de faire des worflows complexes (y compris avec des sous-workflows qui fonctionnent en parallèle) avec des rôles multiples par utilisateur et des permissions très fines.

Les rôles :
+++++++++++

Expressions de rôles :
~~~~~~~~~~~~~~~~~~~~~~
Les valeurs qui sont constantes vues de l'expression (destinée à être évaluée pour chaque ligne), 
comme l'utilisateur, le timestamp, etc. sont, par convention, en majuscules (logique de Python).

Par convention, on pourra utiliser les constantes suivantes :

- `USER`
- `NOW`

Les fonctions prédéfinies (`builtins`) sont les suivantes :

- `is_staff()`
- `is_superuser()`

Pour chaque rôle, si l'expression ne comporte pas de champ du modèle, l'expression sera évaluée (en python) avant la requête SQL.
Si, par contre, l'expression comporte des champs du modèle, l'expression sera transformée, via l'ORM de Django,
en SQL et sera calculée pour chaque ligne (chaque enregistrement) au cours de la requête SQL.

La méthode `save()` :
+++++++++++++++++++++

.. note:: 
    TODO...