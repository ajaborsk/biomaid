================
Smart Widget :
================

Un SmartWidget est une classe Python qui génère un objet graphique à la demande. Il est prévu pour être affiché
sur une page HTML, particulièrement dans un environnement Django.

Il possède les caractéristiques suivantes :

- Il gère ses 'media' (au sens de Django, c'est à dire les fichiers de style CSS et les scripts JS).
- Il peut être hiérarchique (un widget peut être composé d'autres widgets)
- Il peut être créé soit de façon classique / statique, dans le code, par héritage d'autres classes Widget ou
  par création dynamique "au vol".
- Il a un mode de fonctionnement très déclaratif : Un widget est paramétrique et son code est exécuté à chaque rendu
  d'une vue Django pour créer une représentation graphique.
- Il peut être 'actif' au sens http car il a une porte d'entrée et peut donc recevoir des requêtes et les
  traiter

Chronologie du rendu d'un widget (html):
========================================

1 - Définition/Création de la classe
------------------------------------

n - Instanciation de la classe
------------------------------

n - Rendu du template
---------------------

`_setup()`
++++++++++

`_prepare()`
++++++++++++

`_get_context_data()`
+++++++++++++++++++++

Le contexte en vue de l'utilisation du template est complètement calculé avec le
membre de la classe `WidgetClass._template_mapping`, qui est un dictionnaire indiquant
comment calculer les variables du contexte à partir des variables internes du widget.

*Cette méthode n'est pas destinée à être surchargée dans le cadre d'une utilisation 'classique'*

`_as_html()`
++++++++++++
Le template du widget est chargé puis rendu avec le contexte calculé ci-dessus.

*Cette méthode n'est pas destinée à être surchargée dans le cadre d'une utilisation 'classique'*

`__str__()`
+++++++++++
La méthode de conversion en chaîne de caractères utilise la méthode '_as_html()' pour renvoyer une
valeur par défaut sous forme de chaîne.

*Cette méthode n'est pas destinée à être surchargée dans le cadre d'une utilisation 'classique'*



