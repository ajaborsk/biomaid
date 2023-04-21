Arbitrage
=========

Vue d'ensemble
--------------

Une fois que l'expert a analysé une demande, il est logique de l'arbitrer, c'est à dire de l'accepter ou de la refuser.

Toutefois, si l'analyse de l'expert met en évidence qu'il y a eu une erreur d'aiguillage (il peut l'Indiquer
dans son commentaire, par exemple), il reste possible pour un dispatcher de réorienter la demande, comme à l'étape de répartion.

L'arbitrage une opération qui est liée au programme. En effet, l'arbitre est la personne à qui un "manager"
a donné le droit de valider (ou non) une consommation de l'enveloppe, le responsable de cette enveloppe, en quelque sorte.

De ce fait, dès qu'une demande est affectée à un programme (actif), il est **possible** de l'arbitrer. On dit qu'elle
est **arbitrable**. 

Un des rôles de l'expert est de valider le prix unitaire, si celui-ci a été donné par le demandeur,
ou d'en indiquer un, si ce n'est pas le cas. Ce prix unitaire, validé, multiplié par la quantité spécifiée par  
le demandeur, donne le montant d'arbitrage. C'est à dire le montant à consommer sur le programme
si la demande est validée telle que.

En fait, si la demande est arbitrable et s'il n'y a pas de montant d'arbitrage ou d'expert désigné, la seule option possible est de refuser 
la demande...

.. warning:: 
    Sur la version 0.12, en avril 2023, on peut essayer de valider une demande (de façon définitive) sans montant d'arbitrage ou sans expert. 
    C'est un **défault** / **bug** important car 
    dans ce cas, la demande ne peut pas être transférée dans le plan d'équipement et elle disparaît pourtant
    des demandes en cours... La seule solution est de demander à un administrateur de la "dé-valider" en passant par
    l'interface d'administration de Django :-( ...

Si une demande est affectée à un programme actif, qui possède un arbitre, qu'un montant a été déterminé ou validé par l'expert 
et que ce dernier a donné un avis (dans un sens ou dans l'autre), la demande **doit** être arbitrée. On dit qu'elle est
**à arbitrer**.

Accès à l'interface
-------------------

L'accès à l'interface d'arbitrage se fait uniquement depuis le portail "Gestion des demandes".

Il y a ensuite deux accès possibles, avec un fonctionnement légèrement différent :

- Via le menu "Arbitrage", l'utilisateur a accès à tous les programmes pour lesquels il a les droits d'arbitrage ET 
  pour lesquels il y a des demandes **arbitrable**. Dans ce cas, la page d'arbitrage qui est ouverte lors du choix du programme
  est dédiée au programme en question. Il s'agit d'un filtre "de vue" qui n'est pas modifiable par l'utilisateur (il n'apparaît pas 
  dans la barre des filtres).

- Via le cockpit : L'utilisateur peut choisir d'arbitrer toutes les demandes liées à une campagne. Cette fois le filtre mis en place par 
  l'application est un filtre "utilisateur" qu'il est possible de modifier. Dans cette vue, même si l'utilisateur
  peut voir toutes les demandes de la campagne, il n'a le droit d'arbitrer que celles pour lesquelle le programme est déterminé et si l'utilisateur 
  est aussi arbitre dudit programme.


.. note:: 
    A faire : parler de la vue "toutes les demandes en cours", dans laquelle on peut aussi arbitrer.


Mode "projection"
+++++++++++++++++

Il existe parfois un mode "condensé et plein écran" qui permet de ne garder dans la 
fenêtre du navigateur que le tableau et la barre des filtres, afin d'optimiser l'espace
sur des écrans de faible définition ou pour faciliter la lisibilité. Ce mode est particulièrement
utile lorsqu'on utilise un vidéo-projecteur, par exemple lors d'une réunion d'arbitrage.

Ce mode n'est pour l'instant pas accessible via l'interface utilisateur et il faut modifier
l'URL dans le navigateur en ajoutant `-vp` dans la seconde partie de l'URL : La première qui est entre
deux caractères `/` et qui est généralement composée de deux parties séparées par un caractère `-`

L'arbitrage en pratique
-----------------------

Les commentaires
++++++++++++++++

.. note:: 
    Partie restant à rédiger...

Les différents arbitrages
+++++++++++++++++++++++++

.. note:: 
    Partie restant à rédiger...

Les validations partielles
++++++++++++++++++++++++++



.. note:: 
    Partie restant à rédiger...

Bascule vers le plan d'équipement
+++++++++++++++++++++++++++++++++

.. note:: 
    Partie restant à rédiger...
