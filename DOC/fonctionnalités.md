# Description des fonctionnalités de DRA V2

*Les fonctionnalités notées (V#.#+) sont envisagées à partir de la version #.#*

## Plan d'équipement annuel

### Roadmap (à discuter)

----

***Discussion***

1. **BN** : Ok avec ce planning, mais la difficulté va être de disponibilité pour le projet qui va diminuer et la période creuse d'été.
1. **AJA** : Oui, c'est vrai, mais l'essentiel et le vraiment bloquant est déjà fait. Si on a du retard, on rebasculera sur les outils traditionnels...

----

* v0.01 : Début juillet 2020 : suffisamment avancé pour permettre un test par les cadres du service biomédical/équipements généraux
* v0.1 : 17 juillet 2020 : Lancement du recensement sur le CHU pour les équipements biomédicaux et généraux
* v0.2 : septembre 2020 : Amélioration des fonctionnalités de fin de recensement
* v0.3 : octobre 2020 : Outils d'instruction des demandes
* v0.4 : novembre 2020 : Outils d'aide à l'arbitrage
* v0.5 : février 2021 ? : Mise en place du suivi de l'éxécution

### Chronologie

----

***Discussions***

1. **BN** : OK
1. **AJA** : On peut imaginer une sous-phase **fin du recensement** (v0.2+) qui servirait à :

    * Alerter les services qui n'ont pas encore fait de demande (voir comment ?)
    * Alerter les chefs de poles sur des demandes non validées
    * Pendant cette sous-phase, le bandeau d'alerte serait plus visible.

1. **BN** : ou alors seulement l'indication rencessement clos mais alerte avant cloture : ce qui serait plus propre.
1. **BN** : Si on a les mails, on peut imaginer un mail auto à tous pour signaler in recenssement dans 10jours ? je pense qu'il faut alerter tout le monde car on ne peut pas définir si un service a terminé ou non. pour les chefs de pôle un filtre devrait être faisable.
1. **AJA** : Si on a les mails, on va pouvoir faire beaucoup de choses (mon imagination dérive déjà...) !!
1. **AJA** : Signaler à tout le monde, c'est souvent peu efficace... Ou alors, il faudrait au moins y joindre un résumé de ce qui a déjà été demandé/validé. En meme temps, c'était juste une idée comme ça, rien d'indispensable.

Autre sujet :

1. **AJA** : *A discuter (v0.2+)* : Les membres de la commission peuvent créer des demandes pour n'importe quelle UF ?

Autre sujet :

1. **AJA** : *A discuter (v0.2+)* : Possibilité pour les experts de regarder en allant les demandes et de conseiller voire d'aider sur le remplissage
1. **BN** : dans notre cas on aura accès à tout cela ira... voir plutot pour les autres services

----

La création du plan se décompose en 4 phases principales :

* Recensement
* Instruction
* Arbitrage (et validation)
* Exécution

#### Recensement

Pendant le recensement, toutes les personnes possédant un login (cadres ou référents matériel) peuvent
saisir des demandes, pour les UF pour lesquelles elles ont les droits.

Pour chaque demande, on a plusieurs niveaux de remplissage :

1. Les données minimales, sans lesquelles la demande ne peut techniquement pas etre enregistree,
2. Les données de base, qui, si elles sont saisies correctement, permettent d'instruire et d'arbitrer la demande,
3. Les données détaillée qui permettent aux personnes chargées de l'arbitrage de mesurer finement les enjeux de la demande (réglementation, activité...),
4. Les données économiques qui permette de juger de la pertinence économique du projet.

Les niveaux 1 et 2 sont indispensables à la prise en compte de la demande et les niveau 3 et 4, factultatifs, permettent d'appuyer l'argumentaire.

Une fois les demandes saisies, le chef de pole doit valider les demandes afin qu'elles
soient effectivement prises en compte *BN : pour l'instruction*.

Les demandes validées ne peuvent plus etre modifiées par les cadres ou les référents matériel.


#### Instruction

----

***Discussion***

1. **AJA**: Il faut un mécanisme pour gérer les exceptions (oublis, erreurs, loupés...). Peut-etre un système de passe-droit temporaire par login ?
1. **BN**: On a des droits admin, qui plus est les chmaps commentaires de la commissions doivent servir à ca ? (ainsi on a des traces)
1. **AJA**: Utiliser les commentaires, ce serait l'idéal mais c'est peut-etre un peu beaucoup de travail, non ?

----

Pendant la phase d'instruction, il n'est plus possible de saisir des nouvelles demandes

#### Arbitrage

**A finaliser...**

#### Exécution

**A finaliser...**

#### Résumé des roles pendant chaque phase

----

***Discussion***

1. **BN**: On oublie un rôle important : celui qui gère la création des dates d'ouverture fermeture du recensement

----


| Phase                     | recensement                                                                            | Instruction | Arbitrages | Exécution |
|---------------------------|----------------------------------------------------------------------------------------|-------------|------------|-----------|
| Cadre / référent matériel | Création des demandes   + modification des demandes   non validées par le chef de pole | **TODO**    | **TODO**   | **TODO**  |
| Chef de pole              | Création/modification des demandes + validation des demandes                           | **TODO**    | **TODO**   | **TODO**  |
| Expert / acheteur         | Création de demandes sur tous les services ?                                           | **TODO**    | **TODO**   | **TODO**  |
| Membre de la commission   | **TODO**                                                                               | **TODO**    | **TODO**   | **TODO**  |
| Administrateur            | Gère le calendrier                                                                     | **TODO**    | **TODO**   | **TODO**  |

### Prix, cout, enveloppe et montants

----

***Discussion***

**AJA** : C'est une première proposition.

----

Tous les calculs et toutes les estimations se font en **euros TTC**.

Dans le contexte du recensement des besoins, le seul **prix** à prendre en considération est le **prix** unitaire, établi soit à partir d'une estimation (qui doit pouvoir etre confirmée par un expert) soit sur la base d'un devis.

Le **montant estimé** du besoin (de la demande) est le produit du **prix** unitaire par le **nombre** d'équipements demandés. Cela correspond au montant qu'il faudra prélever sur l'enveloppe globale si la demande est acceptée.

Le **cout du projet** (qui est, le plus souvent, l'acquisition du matériel) est plus complexe et peut servir à mesurer l'intéret du projet. Ce **cout** vient en comparaison des **bénéfices** du projet (cf. argumentaire), qui peuvent etre économiques ou qualitatifs (de différentes natures).

Le **cout** peut comporter notamment :

* Le **montant estimé** de l'acquisition, éventuellement réparti sur plusieurs années, s'il s'agit d'investissement,
* Le **cout** de la maintenance
* Le **cout** des consommables (stériles ou non) nécessaires à l'utilisation du matériel
* Le **cout** de main d'oeuvre supplémentaire pour faire fonctionner le matériel
* Le **cout** des travaux nécessaires pour mettre en place le projet
* Les **couts** annexes (mobilier, informatique...) en investissement ou en exploitation

L' **enveloppe** est, en cas de validation de la demande, le montant qui peut effectivement etre dépensé. Elle peut etre inféreure au montant demandé, notamment en cas de réduction des quantités accordées.
