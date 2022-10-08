#!/usr/bin/sh
#
# Installation d'une VM pour les tests
#
# Prérequis : Une VM sous VirtualBox, avec une configuration réseau opérationnelle (tout se fait en headless)
#             Un snapshot de cette VM soit être enregistré
# Il faut que la VM ait un accès à internet (pour installer les packages debian et pip)
# Toutes les variables de configuration peuvent être définie avant de lancer le script (et dans ce cas, ce sont ces valeurs qui sont utilisées)

# Chemin où stocker la machine virtuelle
: ${vm_path:=$HOME"/VMs"}

# Nom de la machine virtuelle (nom dans VirtualBox)
: ${vm_name:="trinidad2"}

# Nom réseau de la machine virtuelle
: ${vm_hostname:=$vm_name".local"}

# This should be a ubuntu server > 20.04 modified ISO image with 'autoinstall' appended
#  to the kernel cmdline. Without this modification, you will have to type 'yes' to allow
#  autoinstall.
# : ${install_iso_image:=$HOME/"Téléchargements/ubuntu-20.04.3-live-server-amd64.iso"}
: ${install_iso_image:=$HOME/"autoinstall-testing.iso"}

# Nom de l'utilisateur principal de la machine virtuelle.
# Il doit pouvoir se connecter par ssh sans donner de mot de passe (utilisation d'une clef privée/publique)
# Il doit avoir les droits sudo (le mot de passe sera demandé une fois à l'utilisateur)
: ${vm_user:="alexandre"}

: ${vm_user_key:=`cat $HOME/.ssh/id_rsa.pub`}

# Nom (au sens de VirtualBox) du snapshot de VM avec l'accès réseau activé et l'utilisateur ci-dessus
: ${vm_snapshot:="fresh_with_network_and_packages"}

# Nom de la fixture pour initialiser la bdd (facultatif mais conseillé)
# Si non fourni ou si le fichier n'existe pas, ce sera la base de tests qui sera chargée
: ${vm_fixture:="dem_db.json"}

#--------------------------------------------------------------------------------------
# Configuration de BIOM_AID
#--------------------------------------------------------------------------------------

# Nom de la base de données PostgreSQL
: ${vm_db_name:="dem_db"}

# Utilisateur PostgreSQL ("rôle")
: ${vm_db_user:="user_dra"}

# Mot de passe de l'utilisateur PostgreSQL
: ${vm_db_pwd:="dra_pwd"}

# Utilisateur qui exécute le site (et qui aura les fichiers dans son $HOME)
: ${vm_dra_user:="user_dra"}

# Dossier (chemin absolu) où sera installé le projet dans le répertoire de l'utilisateur dra
: ${vm_dra_base_path:="/home/"$vm_dra_user"/projet_dra"}

# Dossier (chemin absolu) où seront installés les sources dans le répertoire de l'utilisateur dra
: ${vm_dradem_base_path:=$vm_dra_base_path"/dem"}

# Version de BIOM_AID à installer/configurer (doit correspondre à un tag ou un commit dans le git)
: ${vm_dra_version:="master"}

#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
# Création de la VM si nécessaire
#--------------------------------------------------------------------------------------

if vboxmanage showvminfo $vm_name > /dev/null 2>&1 ; then
echo "VM found"
# TODO: Check for snapshot presence...
else
echo "VM not found => Creating !"
# Basic virtual machine
VBoxManage createvm --basefolder $vm_path --name $vm_name --ostype Ubuntu_64 --default --register

# Hard drive
VBoxManage createmedium --filename $vm_path/$vm_name/hdd.vdi --size 10240

# Add a SATA controller
# (useless, done with default config)
#VBoxManage storagectl $vm_name --name SATA --add SATA --controller IntelAhci

# Attach drive to VM
VBoxManage storageattach $vm_name --storagectl SATA --port 0 --device 0 --type hdd --medium $vm_path/$vm_name/hdd.vdi

# Attach CDROM image
VBoxManage storageattach $vm_name --storagectl IDE --port 0 --device 0 --type dvddrive --medium $install_iso_image

# Network mode is bridget so we can reach it and use ssh
VBoxManage modifyvm $vm_name --nic1 bridged --bridgeadapter1 enp0s13f0u2u1

# Create the configuration cloud-init image
crypted_pass=`openssl passwd -6 -stdin <<< "dra_pwd"`
rm -f $vm_path/seed.iso
mkdir -p $vm_path/cidata
pushd $vm_path/cidata
cat > user-data << __EOF__
#cloud-config
autoinstall:
  version: 1
  identity:
    hostname: $vm_hostname
    password: "$crypted_pass"
    username: $vm_user
  keyboard:
    layout: fr
  packages:
    - avahi-daemon
  ssh:
    install-server: true
    authorized-keys:
      - $vm_user_key
  late-commands:
    - curtin in-target -- systemctl enable avahi-daemon
__EOF__
touch meta-data
# Build the cloud-init ISO image
cloud-localds $vm_path/seed.iso user-data meta-data
popd

# Attach the cloud-init drive
VBoxManage storageattach $vm_name --storagectl IDE --port 0 --device 1 --type dvddrive --medium $vm_path/seed.iso

# Launch the virtual machine => Ubuntu unattended installation
VBoxManage startvm $vm_name --type=gui

# ensure there is no old key stored in known_hosts...
ssh-keygen -R $vm_hostname > /dev/null 2>&1

# Wait until the VM can be accessed via ssh
# during this time, the VM will boot, autoinstall with cloud-init (see cloud-config above)
# then reboot with everything OK

echo -n "Waiting for $vm_hostname..."
ssh -o StrictHostKeyChecking=no $vm_hostname ls > /dev/null 2>&1
while test $? -gt 0
do
   sleep 10 # Avoid to flood the network with connection attempts
   echo -n "."
   ssh -o StrictHostKeyChecking=no $vm_hostname ls > /dev/null 2>&1
done
echo "ok"
echo "VM $vm_name is now installed and ready"

# Get snapshot...
VBoxManage snapshot $vm_name take $vm_snapshot
fi

# Si la VM est déjà en fonctionnement :
if vboxmanage list runningvms | grep -q $vm_name ; then
# Arrêt violent, mais on va l'écraser de toute façon...
echo "La VM "$vm_name" fonctionne. Arrêt..."
vboxmanage controlvm $vm_name poweroff
sleep 1
fi

echo "Restauration de la VM avec le snapshot "$vm_snapshot" ..."
vboxmanage snapshot $vm_name restore $vm_snapshot

echo "Lancement de la VM (headless)..."
vboxmanage startvm $vm_name --type=headless

# Petite pause, le temps du boot :
#TODO: sleep tant qu'on arrive pas à joindre la machine plutôt qu'une durée fixe
# Inutile si le snapshot a été enregistré machine en marche (--live)
# sleep 5

echo "Envoi des scripts d'install sur la VM :"
scp ./install_vm_* $vm_user@$vm_hostname:

if [ -f $vm_fixture ]; then
  echo "Envoi de la fixture complète (toutes les données de la base) :"
  scp $vm_fixture $vm_user@$vm_hostname:
fi

echo "lancement du script d'installation en su..."
echo "----------------------------------------------------------------------------"
echo "-- Sur la VM "$vm_name
echo "----------------------------------------------------------------------------"
ssh $vm_user@$vm_hostname -tt "sudo \
vm_hostname=$vm_hostname vm_user=$vm_user vm_fixture="`basename $vm_fixture`" \
vm_db_name=$vm_db_name vm_db_user=$vm_db_user vm_db_pwd=$vm_db_pwd \
vm_dra_user=$vm_dra_user vm_dra_base_path=$vm_dra_base_path vm_dradem_base_path=$vm_dradem_base_path \
vm_dra_version=$vm_dra_version \
bash install_vm_all.sh"
echo "----------------------------------------------------------------------------"
