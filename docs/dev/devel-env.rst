Créer un environnement de développement
=======================================

- Poetry
- flake9
- selenium
- pytest
-

Sous Linux
----------


Sous Windows
------------

Dans une VM séparée
-------------------

Exemple avec AlmaLinux9. Avec Ubuntu, les commandes pour installer les paquests "de base"
sont un peu différentes, mais presque tout le reste est sans doute identique.

- mettre à jour le système

   dnf update
   dnf clean all

- Installer dans la VM les packages de base indispensables :
  - tar (n'est pas toujours installé)
  - git
  - python311
  - python3.11-devel
  - python3-pip (utilisé par vscode)
  - postgresql-server
  - libpq-devel (utilisé pour construire le pilote psycopg2)
  - group "development tools"
  - nginx
  
.. note:: 
    Pour l'instant, il faut au moins python 3.10 mais on devrait pouvoir travailler avec
    python3.9 au besoin...

- créer l'utilisateur qui gèrera l'instance (dans la suite, on utilisera l'utilisateur *biomaid*):

    adduser biomaid

    usermod -G nginx -a

- Donner les droits au groupe 'nginx' d'accéder en lecture à /home/biomaid/ et /home/biomaid/staticfiles/

- Créer un fichier 'simple-biomaid.conf' dans /etc/nginx/conf.d et y insérer :

    server {
      server_name simple_biomaid;

      location /static {
        alias /home/biomaid/staticfiles/;
      }

      location / {
            proxy_set_header        Host $http_host;
            proxy_set_header        X-Real-IP $remote_addr;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header        X-Forwarded-Proto $scheme;
            add_header P3P 'CP=""';

            proxy_pass http://unix:/home/biomaid/biomaid.sock;
      }
    }


- initialiser le gestionnaire de bases de données

    # postgresql-setup initdb
    # systemctl start postgresql
    # systemctl enable postgresql
    # sudo -i -u postgres
    
    $ createuser --interactive
    Enter name of role to add: biomaid_user
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) y
    Shall the new role be allowed to create more new roles? (y/n) n

    $ psql

    postgres=# 
    postgres=# alter role biomaid_user with password 'biomaid_pwd';

- configuration des accès à postgresql :

    # cd /var/lib/pgsql/data
    # nano pg_hba.conf

    mettre 'md5' comme méthode d'identification sur le port local en IPv4

- ouverture des ports de firewalld :

    # firewall-cmd --zone=public --add-port=8000/tcp --permanent
    # firewall-cmd --zone=public --add-service=http --permanent
    # firewall-cmd --reload

- désactiver SELinux

    # nano /etc/selinux/config

    mettre 'disabled' au lieu de 'enforcing' dans SELINUX=

- se connecter comme *biomaid*

- créer le dossier qui accueillera les logs :

    $ mkdir log

- Créer la BDD 
  
    $ createdb -h localhost -U biomaid_user biomaid_db

- cloner biomaid dans le dossier home de *biomaid*

    $ git clone https://ajaborsk@bitbucket.org/ajaborsk/biomaid.git

- installer Poetry
  
    $ curl -sSL https://install.python-poetry.org | python3 -
    
- aller dans le dossier du projet biomaid et installer les dépendances :

    $ cd biomaid
    $ poetry install --no-root

- local:

    $ ln -sf local_biomaid local

- instance configuration

    $ cp mktests_instance_settings.py instance_settings.py
    $ nano instance_settings.py

    mettre les bonnes infos dans la connexion BDD
    ajouter l'IP de la VM 
    choisir DEBUG=True pour commencer

- migration initiale :

    $ poetry shell
    $ python manage.py migrate

- revenir comme root

- activer le démon nginx :

    # systemctl enable --now nginx


- Créer le fichier de service suivant dans /etc/systemd/system/