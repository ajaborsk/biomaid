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

.. note:: 
    Partie restant à rédiger...

Mode "projection"
+++++++++++++++++

.. note:: 
    Partie restant à rédiger...

Les différents arbitrages
-------------------------

.. note:: 
    Partie restant à rédiger...

Les validations partielles
--------------------------

.. note:: 
    Partie restant à rédiger...

Bascule vers le plan d'équipement
---------------------------------

.. note:: 
    Partie restant à rédiger...
