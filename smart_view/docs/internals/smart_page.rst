***************************************************************
Smart Page :
***************************************************************

Une SmartPage est une View (classe) qui permet de générer plusieurs vues (ou plus exactement plusieurs URLs)
pour travailler sur un modèle unique, sur la base d'une SmartView principale (avec son modèle)
Notamment, la SmartPage donne par défaut des vues pour :

- Ajouter un élément au modèle
- Modifier un élément du modèle
- Voir un élément du modèle
- Copier un élément du modèle (pour en créer un nouveau avec certains champs identiques)
- Supprimer un élément du modèle
- Voir (tableau / Smartview) des éléments du modèle

Toutes ces opérations peuvent être configurées et en particulier tenir compte des rôles et des droits de l'utilisateur et
être limités aux contraintes données par la SmartView (par exemple objets dans un état donné)
ou être configurées vue par vue.

Les vues générées seront nommées (pour utilisation de reverse() ou du tag {% url %}) sous la forme :
appname:name-mode
où :

- appname est le nom de l'application (autodétecté)
- name est le nom de la page, fourni dans l'attribut de classe 'name'
- le nom du mode (celle décrite avec le mode 'None' a pour nom 'appname-name' tout simplement

.. note::

    Cela fonctionne avec une classe-vue unique (cf. doc de Django), mais avec plusieurs *url patterns*
    qui sont créés automatiquement par la méthode de classe ``get_url_patterns()``. Cette méthode doit donc être
    appelée dans le ``url.py`` du module (par une fonction classique ``get_view_url_patterns``). 
    Chaque vue sera effectivement crée avec une classe unique mais la méthode de classe
    ``as_view(mode=...)`` qui va définir une valeur différence de l'attribut ``mode`` de la classe pour chaque vue.

    .. code:: python 
        
        # urls.py

        from common.base_views import get_url_patterns

        urlpatterns = (
            [
                # ...
                # normal url patterns definitions...
                # ...
            ]
            + get_view_url_patterns(views.MySmartPageClass)
        )

    Il y a donc une seule classe dans le code source, mais une classe légèrement différente sera créé pour chaque vue au lancement
    de Django.

    Si on utilise la syntaxe classique de Django (avec juste l'appel à la méthode de classe ``as_view()`` ),
    on n'aura que la vue de base (tableau) et les fonctions d'ajout, de modification, de suppression, etc. ne 
    fonctionneront pas.

Les différents modes par défaut sont :

- ``None``: Une vue (dans un tableau) de la SmartView, avec un menu, des filtres, etc.

- ``'create'``: Un formulaire pour ajouter un nouvel élément dans la table

- ``'copy'``: Copie d'un élément de la table (ouvre un formulaire pour créer un nouvel élément mais avec certaines données
  pré-saisies depuis l'élément à copier.

- ``'modify'``: Un formulaire pour modifier un élément déjà dans la table

- ``'ask_delete'``: Un formulaire simple (affichage en lecture seule + boutons) pour demander à
  l'utilisateur une confirmation avant de supprimer un objet

- ``'delete'``: Suppression effective d'un élément.

Par ailleurs, il est possible de redéfinir les modes d'une SmartPage. Pour ce faire, il faut changer l'attribut ``smart_modes`` de 
la classe héritée de SmartPage.
Cet attribut est un dictionnaire avec comme clés les différents modes (le mode ``None`` est toujours le mode par défaut). 
Les valeurs de ce dictionnaire sont également des dictionnaires qui peuvent avoir les clés suivantes :

- ``'view'``: C'est la seule clé obligatoire. Elle peut prendre les valeurs suivantes :

  - ``'list'``: Vue en liste (ou plutôt tableau, type ``tabulator.js``)
  - ``''``

Exemple :
+++++++++

.. code:: python

    class MyPage(SmartPage):
        smart_modes = {
            None: {
                'view':'list',
                }
        }
        model = ...


