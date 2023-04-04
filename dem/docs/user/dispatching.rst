Répartition / aiguillage
========================

Cette section est principalement destinée aux utilisateurs qui sont désignés comme "dispatcher" d'une campagne
de recensement. Ce sont les seuls qui peuvent effectivement faire cette répartition. 

Vue d'ensemble
--------------

La répartition (ou l'aiguillage) a pour objectif de vérifier qu'une demande est 
dans le bon circuit de décision, d'une part, et de l'orienter vers le bon programme et l'expertise
le plus adapté à son analyse.

A la date d'écriture de cette documentation (avril 2023), un seul utilisateur peut réaliser cette opération. 
Il est désigné, pour chaque campagne, dans le champs "dispatcher". Seul un "manager" peut modifier ce dispatcher.

Pour répartir une demande, il y a donc plusieurs tâches à effectuer :

- Vérifier que la campagne est correcte et réorienter la demande au besoin
- Indiquer le programme dans lequel la demande sera arbitrée
- Déterminer le domaine technique de la demande
- Sélectionner l'expert le plus pertinent en vue de l'analyse de la demande


Lors de la création d'une demande par un utilisateur, la campagne est déjà déterminée 
(même s'il est possible de la changer) tandis que le programme, 
le domaine et l'expert ne sont pas déterminés (champs vides).  

Une demande est considérée comme "répartie" par le système si toutes ces champs ont une valeur 
(il restera néanmoins possible de les changer par la suite)

Accès à l'interface de répartition
----------------------------------

L'interface n'est disponible que pour les utilisateurs ayant le rôle de "dispatcher" pour au moins une campagne.

L'accès se fait :

- en sélectionnant l'application "Gestion des demandes de matériel" dans le menu de sélection du
portail (bouton avec les trois trais horizontaux en haut à gauche).
- Puis en choisissant dans le cockpit qui s'affiche le lien vers la répartion pour la campagne à répartir (lien "pour moi").
- Alternativement, il existe un menu déroulant qui permet d'accéder aussi à la répartion pour les différentes campagnes.

Réorientation vers une autre campagne
-------------------------------------

Evidemment, si une demande est dans le bon circuit, il n'y a rien à faire. Heureusement, c'est normalement le cas
le plus fréquent !

Toutefois, si l'utilisateur qui a saisi la demande n'est pas bien informé des circuits de décision (ou s'il fait mine de ne pas l'être), 
il peut avoir saisi la demande dans la mauvaise campagne, ou même avoir fait une demande sur le portail alors que
c'est un circuit qui n'est pas (encore) géré.

Il est possible, pour le "dispatcher" de modifier la campagne d'une demande pour rerouter la demande vers le
bon circuit. Deux cas se présentent : Soit rediriger vers une autre campagne (ouverte) du portail soit vers une
campagne virtuelle, pour les demandes à traiter autrement, ce qui clôturera de fait la demande.

Il peut s'agir d'une action assez "définitive" : Le dispatcher de la campagne en cours peut ne pas
être le dispatcher de la campagne de destination (et ne pourra donc pas faire la manoeuvre inverse en cas d'erreur). 
Pire, en cas de redirection vers une campagne virtuelle, la demande est fermée et ne peut pas être rouverte...

De ce fait, les modifications de la campagne ne sont pas immédiats : La campagne modifiée apparaît en surbrillance (jaune)
et le changement définitif ne sera mis en oeuvre que lors de l'exécution d'une commande automatique spéciale, généralement au milieu de la 
nuit.

Campagnes classiques
++++++++++++++++++++

Pour les redirections vers les campagnes classiques, il n'est pas nécessaire d'avoir des droits sur cette campagne. Par contre, il faut qu'elle soit ouverte (qu'on soit entre les dates d'ouverture).

.. warning::
    Au 3 avril 2023, le code ne fait aucune autre vérification sur la validité de la campagne et, en particulier, ne vérifie pas
    que l'UF ou le pôle ou l'établissement sont dans la liste des programmes attachés à cette campagne...

.. include:: ../doc_local/doc_dem/dispatching.rst
    :start-after: .. _rerouting-normal:
    :end-before: .. _

Campagnes virtuelles
++++++++++++++++++++

Une campagne "virtuelle" est une campagne qui ne possède pas de dispatcher. 
Les campagnes virtuelles sont reconnaissable dans le menu déroulant 
car elles commencent par les caractères ">>".

Il n'est pas possible de saisir directement des demandes dans les campagnes virtuelles.

Lorsqu'on reroute vers une campagne virtuelle, la demande est clôturée et la raison du refus
est indiquée dans le champs "Commentaire définitif arbitre" et oriente vers le bon circuit pour
la demande.

De plus, si le demandeur a autorisé l'envoi des mails, il reçoit un message qui lui indique immédiatement
que la demande est refusée et lui indique quelle est la marche à suivre.

.. include:: ../doc_local/doc_dem/dispatching.rst
    :start-after: .. _rerouting-virtual:
    :end-before: .. _

Indication du programme
-----------------------

Le programme correspond, en quelque sorte, à l'enveloppe dans laquelle on va "puiser" pour
satisfaire la demande. 

Il peut s'agir d'un programme d'investissement pour la classe 2 (cas classique) mais aussi d'un 
budget d'exploitation (pour la classe 6) ou même d'une enveloppe de location de matériel (même
si la structure n'est pas très adapté à cette façon de procéder).

Il est possible de sélectionner pour chaque demande n'importe quel programme ouvert et pas seulement
les programmes liés à la campagne de la demande.

.. todo:: 
    Il serait sans doute pertinent au moins de favoriser les programmes liés à la campagne de la demande
    en les mettant en premier voire de signaler par une couleur différente les programmes non liés à cette
    campagne...

.. include:: ../doc_local/doc_dem/dispatching.rst
    :start-after: .. _program:
    :end-before: .. _

Détermination du domaine
------------------------

Le domaine permet de préciser quel est la spécialité technique concernée par la demande.

Cette information n'est pour l'instant (avril 2023) utilisée que pour les requêtes statistiques et les 
filtres lors du traitement mais n'a pas de rôle direct dans le processus d'arbitrage.
C'est un champ qui peut, par exemple, servir à filtrer les demandes pour avoir une
vision d'ensemble sur un domaine particulier lors des arbitrages (échographie, perfusion, etc.)

Les domaines disponibles correspondent aux racines (3 caractères) des anciens codes CNEH avec quelques ajouts, ce 
qui donne une vingtaines de grandes catégories.

.. note:: 
    Il était initialement envisagé d'utiliser cette information pour déterminer automatiquement l'expert. 
    Cette fonctionnalité n'est pas implémentée actuellement (avril 2023).


.. include:: ../doc_local/doc_dem/dispatching.rst
    :start-after: .. _domain:
    :end-before: .. _


Choix de l'expert
-----------------

L'expert à désigner est celui qui instruira la demande, c'est à dire qu'il sera chargé de vérifier (ou de déterminer) le prix unitaire
et d'apporter son analyse sur la cohérence de la demande vis à vis de la politique de l'établissement. Il pourra également
donner des indications utiles à l'arbitre, comme le parc actuel ou un historique du dossier, si c'est pertinent.

La liste d'experts proposée au dispatcher est composée de tous les utilisateurs qui ont au moins un domaine d'expertise. Il
n'y a pas de sélection ou de tri sur la discipline, la campagne, le programme ou le domaine.

.. include:: ../doc_local/doc_dem/dispatching.rst
    :start-after: .. _expert:
    :end-before: .. _

