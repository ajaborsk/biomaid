#!/usr/bin/bash

echo "*** Installation de tout..."

# Décompresse (bzip2) la fixture si nécessaire
if [ ${vm_fixture: -4} == ".bz2" ]; then
    bzip2 -d $vm_fixture
    vm_fixture=${vm_fixture: :-4}
fi
if [ ${vm_fixture: -3} == ".gz" ]; then
    gzip -d $vm_fixture
    vm_fixture=${vm_fixture: :-3}
fi

echo "**********************************************************************************"
echo "*** Installation de PostgreSQL..."
apt install -y -qq libpq-dev postgresql postgresql-contrib

echo "*** Crée la base de données $vm_db_name ..."
sudo -u postgres createdb $vm_db_name

echo "*** Crée l'utilisateur et lui donne les droits nécessaires..."
sudo -u postgres psql -c "CREATE ROLE $vm_db_user LOGIN PASSWORD '$vm_db_pwd';" -c "ALTER DATABASE $vm_db_name OWNER TO $vm_db_user;" -c "ALTER ROLE $vm_db_user CREATEDB;"

echo "*** Ajoute les droits pour se connecter au serveur en local (même s'il n'existe pas d'utilisateur linux $vm_db_user)"
sed -i.bak -e "s/^\(\# TYPE\s*DATABASE.*$\)/\1\n\nlocal\t$vm_db_name\t\t$vm_db_user\t\t\t\tmd5/" /etc/postgresql/12/main/pg_hba.conf

echo "*** Redémarre le serveur PostgreSQL ..."
systemctl restart postgresql

# echo "*** test de variable : vm_db_name="$vm_db_name

echo "**********************************************************************************"
echo "*** Installation de Nginx..."
apt install -y -qq nginx

sed -i.bak \
-e "s|####VM_HOSTNAME####|$vm_hostname|" \
-e "s|####VM_DRA_USER####|$vm_dra_user|" \
-e "s|####VM_DRA_BASE_PATH####|$vm_dra_base_path|" \
-e "s|####VM_DRADEM_BASE_PATH####|$vm_dradem_base_path|" \
install_vm_site_nginx_dra.conf

cp -f install_vm_site_nginx_dra.conf /etc/nginx/sites-available/dra
ln -sf /etc/nginx/sites-available/dra /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
service nginx reload

apt install -y -qq nginx

echo "**********************************************************************************"
echo "*** Installation du serveur Django..."

apt install -y -qq python3-pip python3-dev

useradd -m -s /usr/bin/bash -p '$6$y6JA912vZ/LLgJlM$yylJhlLD2glHAqPgW4j.lRyiVxcqhpwQo3YSbOQkFT901US4MDoegJyACowrakjUFEaKRqRIc49dRHY/d5crn0' $vm_dra_user
sudo -u $vm_dra_user mkdir $vm_dra_base_path
pip3 install virtualenv
sudo -u $vm_dra_user virtualenv -p python3 $vm_dra_base_path/myvenv
sudo -u $vm_dra_user -i git clone https://ajaborsk:alexandrE1520@bitbucket.org/kig13/dem.git $vm_dradem_base_path

sudo -u $vm_dra_user -i git -C $vm_dradem_base_path checkout $vm_dra_version
sudo -u $vm_dra_user -i ln -sf $vm_dradem_base_path/local_ghtsls $vm_dradem_base_path/local
sudo -u $vm_dra_user -i mkdir $vm_dradem_base_path/media

sudo -u $vm_dra_user -i $vm_dra_base_path/myvenv/bin/pip install -r $vm_dradem_base_path/requirements.txt
sudo -u $vm_dra_user -i $vm_dra_base_path/myvenv/bin/pip install -r $vm_dradem_base_path/requirements-dev.txt
sudo -u $vm_dra_user -i $vm_dra_base_path/myvenv/bin/pip install gunicorn

echo "Création du fichier settings spécifique à cette VM :"
sed -i.bak \
-e "s|####VM_SECRET####|"`openssl rand -base64 40`"|" \
-e "s|####VM_HOSTNAME####|$vm_hostname|" \
-e "s|####VM_DB_USER####|$vm_db_user|" \
-e "s|####VM_DB_NAME####|$vm_db_name|" \
-e "s|####VM_DB_PWD####|$vm_db_pwd|" \
install_vm_settings.py
cat install_vm_settings.py

cp install_vm_settings.py $vm_dradem_base_path/site_settings.py
chown $vm_dra_user $vm_dradem_base_path/site_settings.py
chmod 0666 $vm_dradem_base_path/site_settings.py

cd $vm_dradem_base_path
sudo -u $vm_dra_user $vm_dra_base_path/myvenv/bin/python manage.py migrate
sudo -u $vm_dra_user $vm_dra_base_path/myvenv/bin/python manage.py collectstatic


if [ -f /home/$SUDO_USER/$vm_fixture ]; then
    sudo -u $vm_dra_user $vm_dra_base_path/myvenv/bin/python manage.py loaddata /home/$SUDO_USER/$vm_fixture
else
    sudo -u $vm_dra_user $vm_dra_base_path/myvenv/bin/python manage.py loaddata $vm_dradem_base_path/fixtures/tests_db.json
fi

# Retour dans le répertoire de départ
cd /home/$SUDO_USER

echo "**********************************************************************************"
echo "*** Installation de Gunicorn & supervisor..."
apt-get install -y -qq gunicorn
apt-get install -y -qq supervisor

sed -i.bak \
-e "s|####VM_HOSTNAME####|$vm_hostname|" \
-e "s|####VM_DRA_USER####|$vm_dra_user|" \
-e "s|####VM_DRA_BASE_PATH####|$vm_dra_base_path|" \
-e "s|####VM_DRADEM_BASE_PATH####|$vm_dradem_base_path|" \
install_vm_dra_gunicorn.conf

cp -f install_vm_dra_gunicorn.conf /etc/supervisor/conf.d/dra-gunicorn.conf

supervisorctl reread
supervisorctl update
