Le "logging"
============

Sources de log
--------------

- nginx
- supervisor / gunicorn
- commandes / jobs
- requêtes SQL / Qui Fait Quoi / Activité des utilisateurs
- tests

Format des fichiers de log
--------------------------

Les fichiers de log sont des fichiers texte, comportant une ligne par événement.
Exceptionnellement, il est possible de trouver un événement décrit sur plusieurs lignes,
mais chaque ligne doit respecter le format d'un événement unique.

Un événement comporte toujours 5 parties :

- un timestamp, au format ISO (yyyy-mm-ddThh:mm:ss.sss), **en temps universel**
- la source de l'événement, sous la forme d'un identifiant ne comportant pas d'espace.
  Cet identifiant peut être composé de plusieurs parties, séparées par des '.'
- le type (niveau) d'événement. Ce niveau doit être dans la liste FATAL, ERROR, WARN, NOTICE, INFO, DEBUG
- le message de l'événement. Certains événements peuvent imposer un format mais le cas général est que texte
  jusqu'à la fin de la ligne est le message de l'événement

Les différents champs sont séparés par des caractères d'espace.

Politique de logging:
---------------------

Le niveau par défaut doit être NOTICE (tout ce qui est inférieur, c'est à dire
INFO et DEBUG, n'est pas affiché)

Pour les commandes et les jobs, le logging se fait sur la sortie standard (`stdout`). Il existe 4 niveaux de "verbosity", de 0 à 3,
avec les comportements suivants :

- Niveau 0 (quiet) : Aucune sortie ne doit être faite sur `stdout`, sauf éventuellement un événement critique (de type `FATAL`).
- Niveau 1 (défaut) : C'est le niveau utilisé par les scripts de type `cron`. Si tout se passe correctement
  (pas d'erreur ni de warning), la sortie ne doit pas excéder quelques lignes par exécution (résumé des actions réalisées,
  nombre d'enregistrements traités, etc.). La sortie doit se conformer au format décrit ci-dessus.
- Niveau 2 (verbose) : Plutôt destiné à une utilisation par un humain, "à la main". A ce niveau, les événements de niveau `INFO`
  doivent être affiché. La sortie est plus détaillée : liste des objets traités, etc.
  Il est possible d'utiliser de la couleur dans les messages, des barres de progression, etc.
- Niveau 3 (debug) : Destiné uniquement au développement. La sortie peut être très détaillée.


.. note::
  Dans la version 0.12.2 (au 18 décembre 2022), cette spécification n'est pas encore mise en oeuvre partout dans BiomAid.