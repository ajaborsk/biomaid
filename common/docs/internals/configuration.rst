=====================================
La gestion de la configuration
=====================================

Dans BiomAid, il existe plusieurs niveaux de configuration :

1. La configuration du projet, essentiellement tirée du ``pyproject.toml``.  Elle ne comporte que des données
   créées par les développeurs. On vu trouver dans cette catégorie, par exemple, le numéro de version de BIOM_AID ou
   les nouveautés des différentes versions (``WHATSNEW``).

2. La configuration système, qui comporte notamment la configuration de Django. On retrouve dans ce niveau tout ce
   qui est lié à l'installation de Django et tout ce qui concerne l'interface avec le système d'exploitation, y compris
   les chemins des données/fichiers utilisés par BiomAid. On retrouve dans ce niveau tout ce qui concerne les interfaces
   avec les autres systèmes (cron, mail, magh2, Asset+, structure...). Cette configuration se retrouve dans les fichiers
   python ``settings/*.py``, ``local/settings.py`` et ``site_settings.py``.

3. La configuration administrateur (super-user) "stable", qui comporte tous les éléments liés au fonctionnement de BIOM_AID
   qui ne nécessitent pas d'intervention d'un administrateur système. On trouvera par exemple à ce niveau :

   - La configuration des portails
   - L'activation (ou non) et la configuration des alarmes
   - La configuration (mise en page et contenu) des cockpits et autre indicateurs
   - L'ajout de champs calculés dans les modèles / tables
   - La définition des workflows (à vérifier !!)

   Ces données de configuration se trouvent dans le fichiers de configuration ``local/config.toml`` ainsi que dans
   les fichiers ``local/config.d/*toml``.

4. La configuration dynamique, qui est stockée dans la base de données. A la date d'aujourd'hui,
   ce niveau n'est pas utilisé.

Les trois premiers niveaux nécessitent un redémarrage de l'application pour être mis à jour / pris en compte.

La totalité de ces informations de configuration est disponible au travers de l'objet ``common.config``, qui
se comporte aussi comme un dictionnaire et un objet :

- La configuration du projet est disponible dans l'objet ``common.config.pyproject``.
- La configuration système est disponible dans l'objet ``common.config.settings`` (ainsi que dans
  ``django.conf.settings``)
- Les autres données sont dans les autres clefs de l'objet.
