===========================================
La gestion des alertes
===========================================

BIOM_AID dispose d'un mécanisme d'alerte afin de signaler
aux utilisateurs les points qui nécessitent leur attention.

Configuration
-------------

La configuration des alarmes se fait dans un dictionnaire défini dans la classe
configuration de chaque application.

:roles: Liste des rôles concernés par l'alerte (tuple ou liste de strings)
:label: Intitulé de l'alerte (string)
:help_text: Description plus complète de l'alerte. Sera utilisé pour générer la documentation (string)
:hint: Aide qui indique ce qu'il faut faire pour désactiver l'alerte (string)
:message: Texte de l'alerte (string paramétrique)
:alert_level: Niveau de l'alerte (int)
:user_settings: Configuration de l'alerte par chaque utilisateur (ayant un des rôles lié à l'alerte)
:groups: Liste des groupes auxquels appartient l'alerte (inutilisé pour l'instant, liste de strings)
:check_func: Function de détection de l'alerte (fonction python)


Sources d'alertes
-----------------

Détection ponctuelle
~~~~~~~~~~~~~~~~~~~~



Détection par "pool"
~~~~~~~~~~~~~~~~~~~~

L'autre mécanisme de détection des alertes fonctionne par pool ou ensemble, comme par exemple l'ensemble des demandes.
Dans ce cas, le script de détection retourne la liste des enregistrements/objets concernés par l'alerte et le système
considère que si une alerte de ce type était active sur un enregistrement et n'est pas dans la nouvelle liste des alertes
sur le même ensemble, c'est que l'alerte n'est plus active (c'est une désactivation implicite).

.. note::
     Il faudrait faire un exemple car le concept n'est pas simple à comprendre au premier abord...

Enregistrements
---------------

Le système conserve une liste de toutes les alertes, qu'elles soient actives ou qu'elles aient été neutralisées.

.. note::
     On pourrait facilement imaginer une commande, appelée périodiquement par un job,
     qui supprimerait de la table les alertes inactives depuis un certain temps (plusieurs mois ?)

Signalement aux utilisateurs
----------------------------

Liste des alertes
~~~~~~~~~~~~~~~~~

Depuis leur menu personnel (généralement en haut à droite, en cliquant sur leur nom),
les utilisateurs peuvent accéder à un tableau qui liste toutes les alertes
qui le concernent.

Par défaut, seules les alertes actives sont affichées, mais il est possible d'afficher
aussi les alertes devenues inactives.

Badges
~~~~~~

Email
~~~~~

Boîte d'alerte
~~~~~~~~~~~~~~

Simple idée non implémentée pour l'instant : Ouvrir une boîte de dialogue avec un
résumé des alertes, à chaque utilisation de BIOM_AID (avec évidemment une période réfractaire assez longue,
12 heures par exemple, qui donne environ un affichage par jour).

Bandeau persistant
~~~~~~~~~~~~~~~~~~

Simple idée non implémentée pour l'instant : Un bandeau en haut de l'écran,
éventuellement d'une couleur dépendant des niveaux d'alerte...

