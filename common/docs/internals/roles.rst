========================
Les rôles dans BiomAid :
========================

Dans BiomAid, la gestion des permissions (les "droits") s'appuie sur la notion de rôle.

POur faire simple, un rôle s'apparente au groupe qu'on peut rencontrer dans les systèmes
de gestion des permissions des systèmes de fichiers, mais sont dépendantes du contexte et/ou de l'objet
concerné par la permission. Ainsi, si on considère les demandes de matériel (application ``dem``),
un utilisateur peut être *chef de pôle* pour certaines demandes (celles qui concernent son pôle)
mais avoir un autre rôle (*expert* par exemple) pour les autres demandes.

Les rôles globaux
-----------------

Certains rôles ne dépendent pas de l'objet considéré et sont donc nommés *globaux*. Il s'agit par exemple du
rôle de super utilisateur ou d'administrateur du site.

Les codes de rôle
-----------------

Les rôles peuvent être aussi utilisés par d'autres programmes que Django et en particulier par du javascript
inclus dans les pages WEB.

Pour faciliter les échanges, chaque rôle a donc un code alphanumérique, généralement un code de 3 ou 4 lettres en
majuscules.

La chaîne/liste de codes de rôles :
+++++++++++++++++++++++++++++++++++
Ce code est aussi utilisé dans les requêtes SQL pour créer dynamiquement une liste de codes rôle,
représentée par une chaîne de caractère composée des différents codes rôle, encadrés et séparés par des virgules.
Pour des raisons techniques liées en particulier aux limitations de certains moteurs SQL pour les concaténations,
c'est la seule représentation possible pour l'instant. Par exemple, pour un objet pour lequel l'utilisateur est
à la fois expert (rôle ``EXP``) et créateur/propriétaire de l'objet (code ``OWN``), la chaîne de caractères sera : ``",EXP,OWN,"``.
Cette représentation permet de savoir si un utilisateur a un rôle particulier, comme ``OWN``, simplement en vérifiant
que la chaîne de caractères ``",OWN,"`` est bien incluse (fonction simple et incluse dans tous les langages)
dans la chaîne qui donne l'ensemble des rôles.
L'utilisation de ``","`` en début et fin de la chaîne permet d'éviter les erreurs liées à d'éventuels codes qui seraient
des sous-chaînes d'autres codes.

.. note::

   L'encadrement par les ``,`` n'est pas opérationnel à la date d'écriture de ces lignes (novembre 2021) car
   il n'y a pour l'instant pas de code inclus dans un autre, mais c'est
   clairement à prendre en compte rapidement et avant l'ouverture à de nouveaux codes.

Codes utilisés :
++++++++++++++++

``ADM`` : **Administrateur**, rôle global
    - Rôle calculé à partir du champs ``User.is_staff`` de Django (intégré dans le système de base)
    - Permet d'accéder aux pages d'administration (Django) du site et à toutes les pages globales de gestion.

.. note::

    A terme, il serait sans doute judicieux de séparer les rôles d'administrateur système et de super-utilisateur.

``EXP`` : **Expert métier**, dépend à la fois de la structure (établissement, UF, pôle, etc.) et du domaine (& discipline)
    - Rôle calculé à partir des objets concernés (champs donnant l'UF, la discipline et le domaine)
    - Peut analyser les demandes dans son domaine, c'est à dire vérifier les prix, faire un commentaire et
      donner un avis

``CHP`` : **Chef de pôle**
    - Rôle calculé à partir de l'objet (champ donnant l'UF)
    - Permet d'approuver les demandes de son pôle
    - A ne pas confondre avec le rôle ``P-CHP`` (qui signifie *Etre chef d'au moins un pôle*)
