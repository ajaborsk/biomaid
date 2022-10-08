.. sectnum::
    :suffix: . -

==================================
Le "workflow" des demandes
==================================


Campagne de recensement
------------------------------------------

Une campagne de recensement représente en quelque sorte le point
d'entrée pour une demande. Il existe trois types principaux de campagne :

- Les campagnes annuelles,

- Les campagnes exceptionnelles,

- Les campagnes "virtuelles".

Chaque campagne comporte les champs suivants :

:code: C'est un code qui pourra être utilisé par une future interface.
    Typiquement, il comporte l'année et le type de campagne. **(obligatoire)**.
:nom: C'est le nom de la campagne qui sera affichée dans les menus et dans les formulaires. **(obligatoire)**.
:debut_recensement: Date de lancement de la campagne.
    Il ne sera pas possible de saisir des demandes dans cette campagne avant cette date. **(obligatoire)**
:fin_recensement: Date de fin de la campagne. Il ne sera plus possible, sauf cas particulier,
    de saisir des demandes dans cette campagne après cette date. **(obligatoire)**.
:discipline: Discipline de la campagne. Si cette valeur est définie,
    toutes les demandes saisies dans le cadre de la campagne auront leur champ ``discipline`` remplis avec cette valeur.
:dispatcher: Lien vers l'utilisateur qui sera chargé de répartir les demandes vers les différents experts et les différents
    programmes. Si celle valeur n'est pas définie (``NULL``), alors la campagne est dite *virtuelle* (cf. ci-dessous).
:message: Message qui sera affiché systématiquement (dans une boîte de dialogue puis en haut du formulaire)
    à chaque fois qu'un utilisateur commencera à remplir une demande. Pour les campagnes virtuelles, c'est le message
    qui est mis dans le commentaire de non validation de chaque demande pour expliquer la raison du rejet de la demande.
    **(facultatif)**.
:description: Commentaire éventuel (n'est pour l'instant pas affiché pour les demandeurs). **(facultatif)**.


Les campagnes annuelles
+++++++++++++++++++++++

Une campagne annuelle est une campagne "normale". Elle a
un code, un titre, une discipline, un dispatcheur, une date de début et une date de fin.

Au moins un programme (cf. ci-dessous) doit y être rattaché. Ce sera au dispatcheur de choisir le programme à utiliser.

Les campagnes exceptionnelles
+++++++++++++++++++++++++++++

Une campagne exceptionnelle est quasiment identique à une campagne normale.
La seule différence est qu'un message d'alerte peut être défini et sera présenté systématiquement à l'utilisateur
avant la saisie de sa demande.
Ce message peut par exemple comporter les règles particulières de traitement de la demande.

Les campagnes "virtuelles"
+++++++++++++++++++++++++++

Une campagne virtuelle est une campagne utilisée uniquement pour réorienter une demande vers un circuit
extérieur au logiciel. Il n'est pas possible de créer directement des demandes avec cette campagne et il ne faut pas y
attacher de programme.

On créée une campagne virtuelle en n'y attachant pas de dispatcher.

Une commande Django, lancée périodiquement, se charge de refuser systématiquement toutes
les demandes enregistrées dans ces campagnes et d'en expliquer la raison au demandeur.

.. todo::
    Implémentation à finaliser dans la version 0.9 de BiomAid.

Programmes
-----------------

Un programme représente une "enveloppe" à distribuer. Cela peut être, par exemple :

- L'enveloppe d'investissement définie pour un plan annuel d'équipement,
- L'enveloppe attribuée à un projet particulier au moment de sa validation,
- Une subvention,
- etc.

Un programme de BiomAid correspond sensiblement à un programme de la GEF magh2.

Chaque programme possède les champs suivants :

:code: Code utilisé en interne pour le programme. Idéalement, il faut utiliser le même système
    que pour la GEF, afin de faciliter les échanges (mais ce n'est pas toujours possible). **(obligatoire)**.
:nom: Nom du programme, tel qu'affiché sur les écrans des utilisateurs. **(obligatoire)**.
:calendrier: Lien vers le calendrier de recensement associé au programme. **(facultatif)**.
:enveloppe: Montant de l'enveloppe dévolue à ce programme (en euros TTC). **(obligatoire)**.
:description: Description textuelle du programme. Uniquement affiché, pour info, sur les pages de gestion. **(facultatif)**.
:discipline: ... doc à écrire ... **(obligatoire mais inutilisé ?)**.
:arbitre: Lien vers l'utilisateur qui sera chargée de valider (ou pas) les demandes associées à ce programme.
    C'est en quelque sorte la personne qui assurera le respect de l'enveloppe (au stade de la planification,
    donc avant l'exécution). **(facultatif)**.

.. note::
    Le programme est également utilisé par d'autres modules de BiomAid (et notamment DRACHAR).
    Il fait donc partie de l'application ``common`` et non de l'application ``dem``.

Nouvelle demande
----------------

Avis des cadres supérieurs
--------------------------

Approbation par le chef de pôle ou le directeur adjoint
-------------------------------------------------------

Répartition par le "dispatcher"
-------------------------------



La réorientation d'une demande
++++++++++++++++++++++++++++++

.. note::
    Description du process, mais non encore disponible.

Lorsqu'un dispatcher juge qu'une demande est inadaptée à la campagne dans laquelle elle
a été faite, il peut choisir de la "rerouter" ou "rediriger".

Dans ce cas, un message est adressé au demandeur pour l'informer de cette disposition.

Si la campagne de destination est une campagne réelle (annuelle ou exceptionnelle), c'est à dire
avec un dispatcher de défini, elle est simplement transférée (son lien vers la campagne est changé).

.. note::
    Dans ce cas, il faut voir si les champs remplis par le demandeur sont toujours adaptés...
    Notamment si on passe de travaux à équipement ou l'inverse...

Si la campagne de destination est une campagne virtuelle,
la demande est dans ce cas directement arbitrée comme "invalide".

.. note::
    Comme les arbitrages sont définis par programme, cela pose un problème car il n'y a dans ce cas pas de programme...
    Ou alors on crée un programme unique par campagne ? Mais cela ne semble pas très cohérent...

Analyse / vérification par l'expert métier
------------------------------------------

Arbitrage
---------

Arbitrage définitif
-------------------
