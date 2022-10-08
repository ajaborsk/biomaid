#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from django.utils import timezone
from django.utils.translation import gettext as _

from assetplusconnect.smart_views import AssetPlusMarcheSmartView
from common.models import Marque
from django.conf import settings
from progress.bar import Bar

# from progress.spinner import Spinner
from django.db.models import Q
from common.models import Cnehs, Discipline, ClasseCode, Type
from smart_view.smart_page import SmartPage

# Create your views here.
# TODO : prévoir partie du code quand la connexion a GMAO ne marche pas


class ConnectorAssetPlus:
    def V10_8(self, request, BddImportation, *args, **kwargs):
        if self.model_update == "Marque":
            start_time = timezone.now()
            data = BddImportation.import_data_gmao(self).order_by(
                'ma_nom'
            )  # TODO : utiliser une table gérant les dates de dernières MAJ pour optimiser le code ici
            # TODO : ligne de code pour sauvegarder la date de l'Update dans le model common.updates_monitor
            # data_biom_aid = self.model.objects.all() UNUSED, comment by AJA
            # TODO : attention, cette partie est a extraire et a mettre en automatisme : fonctionnalité uniquement lié à Asset+
            for item in data:
                try:
                    # instance = self.model.objects.get(**self.fields_to_get(item))
                    instance = self.model.objects.get(id_gmao=item.auto_id)
                    if instance.nom == item.ma_nom:
                        pass
                    else:
                        instance.nom = item.ma_nom
                        instance.save()
                    if instance.cloture == item.date_refor or instance.cloture is None or instance.cloture == "Null":
                        pass
                    else:
                        instance.cloture = item.date_refor
                        instance.save()
                except self.model.DoesNotExist:
                    new = self.model.objects.create(nom=item.ma_nom, id_gmao=item.auto_id)
                    new.save()
                    pass
            elapsed_time = timezone.now() - start_time
            print("elapsed_time : ")
            print(elapsed_time)
            return self.get(request, *args, **kwargs)

        '''######################################### CODE UPDATE TABLE TYPE #########################################'''
        if self.model_update == "Type":
            start_time = timezone.now()
            print('start_time : ' + str(start_time))
            print('Chargement des données de GMAO, veuillez patienter...')
            data = BddImportation.import_data_gmao(self).order_by('tp_type')
            '''//////////////////////////////////////////////////////////////////////////////////////////////////////'''
            '''PROCESSING'''
            message = ""
            with Bar('Processing', max=len(data)) as bar:
                for item in data:
                    try:
                        '''chargement de l'instance__________________________________________________________________'''
                        instance = self.model.objects.get(id_gmao=item.auto_id)
                        # print(" instance : " + str(instance))
                        '''check sur type____________________________________________________________________________'''
                        if instance.type == item.tp_type:
                            # print("pas de modif type")
                            pass
                        else:
                            instance.type = item.tp_type
                            # print("modif type")
                            # instance.save()
                        '''check sur marque__________________________________________________________________________'''
                        if instance.marque is not None:
                            if instance.marque.nom == item.marque:
                                # print("pas de modif marque")
                                pass
                            else:
                                if item.marque is None or not item.marque:
                                    # print("Marque non renseignée dans la GMAO, pas de modification")
                                    pass
                                else:
                                    try:
                                        marque_selected = Marque.objects.get(nom=item.marque)
                                        instance.marque = marque_selected
                                        # print('instance.marque : ' + str(instance.marque))
                                        # instance.save()
                                    except Exception:
                                        # print("marque inexistante ou non renseignée,
                                        #   veuillez l'enregistrer avant : " + str(item.marque))
                                        message = (
                                            message
                                            + ", marque inexistante ou non renseignée, veuillez l'enregistrer avant : "
                                            + str(item.marque)
                                        )
                                        pass
                                        # TODO : generer automatiquement si en mode auto la MAJ de la table :marque ?
                        '''check sur cneh_type_______________________________________________________________________'''
                        if instance.cneh_code is not None:
                            if instance.cneh_code.code == item.cneh_type:
                                # print("pas de modif cneh_type")
                                pass
                            else:
                                if item.cneh_type is None or not item.cneh_type:
                                    # print("Classe non renseignée dans la GMAO, pas de modification")
                                    pass
                                else:
                                    try:
                                        id_cneh = Cnehs.objects.get(code=item.cneh_type)
                                        # print('id_cneh : ' + str(id_cneh))
                                        instance.cneh_code = id_cneh
                                        # print("modif cneh_type")
                                        # instance.save()
                                    except Exception:
                                        # print("code CNEH inexistant ou non renseigné,
                                        #   veuillez l'enregistrer avant : " + str(item.cneh_type))
                                        message = (
                                            message
                                            + ", code CNEH inexistant ou non renseigné, veuillez l'enregistrer avant : "
                                            + str(item.cneh_type)
                                        )
                                        # TODO : generer automatiquement si en mode auto la MAJ de la table CNEH ?
                        elif item.cneh_type is None or not item.cneh_type:
                            # print("CNEH non renseigné dans la GMAO, pas de modification")
                            pass
                        else:
                            # print("non renseigné, donc modif CNEH")
                            try:
                                instance.cneh_code = Cnehs.objects.get(code=item.cneh_type)
                                # print('modif instance.cneh_code par : ' + str(instance.cneh_code))
                                # instance.save()
                            except Exception:
                                # print("code CNEH de la gmao inexistant dans bdd Drachar, "
                                #           "veuillez l'enregistrer avant : " + str(item.cneh_type))
                                message = (
                                    message + ", code CNEH de la gmao inexistant dans bdd Drachar,"
                                    " veuillez l'enregistrer avant : " + str(item.cneh_type)
                                )
                        '''check sur désignation (nom2)______________________________________________________________'''
                        if instance.complement == item.nom2:
                            # print("pas de modif nom2")
                            pass
                        else:
                            instance.complement = item.nom2
                            # print("modif nom2")
                            # instance.save()
                        '''check sur Classe code ____________________________________________________________________'''
                        if instance.classe_code is not None:
                            if instance.classe_code.code == item.classe_eqp:
                                # print("pas de modif de la Classe")
                                pass
                            else:
                                if item.classe_eqp is None or not item.classe_eqp:
                                    # print("Classe non renseignée dans la GMAO, pas de modification")
                                    pass
                                else:
                                    try:
                                        id_classe = ClasseCode.objects.get(code=item.classe_eqp)
                                        # print('id_classe : ' + str(id_classe))
                                        instance.classe_code = id_classe
                                        # print("modif Classe")
                                        # instance.save()
                                    except Exception:
                                        # print("code de Classe de la gmao inexistant dans bdd Drachar,"
                                        #       " veuillez l'enregistrer avant : " + str(item.classe_eqp))
                                        message = (
                                            message + ", code de Classe de la gmao inexistant dans bdd"
                                            " Drachar, veuillez l'enregistrer avant : " + str(item.classe_eqp)
                                        )
                        elif item.classe_eqp is None or not item.classe_eqp:
                            # print("Classe non renseignée dans la GMAO, pas de modification")
                            pass
                        else:
                            # print("non renseigné, donc modif classe_code")
                            try:
                                instance.classe_code = ClasseCode.objects.get(code=item.classe_eqp)
                                # print('modif instance.classe_code : ' + str(instance.classe_code))
                                # instance.save()
                            except Exception:
                                # print("code de Classe inexistant, veuillez l'enregistrer avant : "
                                #           + str(item.cneh_type))
                                message = message + ", code de Classe inexistant," " veuillez l'enregistrer avant : " + str(
                                    item.cneh_type
                                )
                        '''check sur Discipline/Vocation fonctionnelle_______________________________________________'''
                        if instance.discipline is not None:
                            if instance.discipline.code == settings.LOCALDISCIPLINE[str(item.voc_fonc)]:
                                # print("pas de modif discipline")
                                pass
                            else:
                                instance.discipline = Discipline.objects.get(code=settings.LOCALDISCIPLINE[str(item.voc_fonc)])
                                # print("modif discipline : " + str(instance.discipline.code))
                                # instance.save()
                        elif item.voc_fonc is None or not item.voc_fonc:
                            # print("Discipline non renseignée dans la GMAO, pas de modification")
                            pass
                        else:
                            # print("non renseigné, donc modif Discipline")
                            try:
                                instance.discipline = Discipline.objects.get(code=settings.LOCALDISCIPLINE[str(item.voc_fonc)])
                                # print('modif instance.classe_code : ' + str(instance.discipline))
                                # instance.save()
                            except Exception:
                                # print("Discpline inexistante, veuillez l'enregistrer avant : " + str(item.voc_fonc))
                                message = message + ", Discpline inexistante, veuillez l'enregistrer avant : " + str(item.voc_fonc)
                        '''check sur date de réforme________________________________________________________'''
                        if instance.cloture == item.date_refor or instance.cloture is None or not instance.cloture:
                            # print("pas de réforme ou déjà réformé")
                            pass
                        else:
                            # print(instance.cloture)
                            instance.cloture = item.date_refor
                            # print(instance.cloture)
                            # print(item.date_refor)
                            # print("date réforme mise à jour")
                            # instance.save()
                    except self.model.DoesNotExist:
                        '''Fonction en cas de non existance dans la BDD actuelle :
                        - vérification que l'ensemble des FK existent
                        - si une FK obligatoire est manquante, blocage de cet ajout + envois d'un message;
                        '''
                        add_ok = True
                        '''Objet marque_____________________________________________________________________________'''
                        try:
                            obj_marque = Marque.objects.get(nom=item.marque)
                        except Exception:
                            add_ok = False
                            message = message + "marque manquante : " + str(item.marque) + " "
                        '''Objet Classe_____________________________________________________________________________'''
                        try:
                            obj_classe = ClasseCode.objects.get(code=item.classe_eqp)
                        except Exception:
                            obj_classe = None
                            message = message + "Classe équipement manquante : " + str(item.classe_eqp) + " "
                            pass
                        '''Objet CNEH_____________________________________________________________________________'''
                        try:
                            obj_cneh = Cnehs.objects.get(code=item.cneh_type)
                        except Exception:
                            obj_cneh = None
                            message = message + "Discipline manquante : " + str(item.cneh_type) + " "
                            pass
                        '''Objet Discipline__________________________________________________________________________'''
                        try:
                            obj_discipline = Discipline.objects.get(code=settings.LOCALDISCIPLINE[str(item.voc_fonc)])
                        except Exception:
                            obj_discipline = None
                            message = message + "Discipline manquante : " + str(item.voc_fonc) + " "
                            pass
                        '''Fonction d'ajout__________________________________________________________________________'''
                        if add_ok:
                            # print("item.tp_type =" + str(item.tp_type))
                            new = self.model(
                                type=item.tp_type,
                                marque=obj_marque,
                                cneh_code=obj_cneh,
                                classe_code=obj_classe,
                                complement=item.nom2,
                                discipline=obj_discipline,
                                id_gmao=item.auto_id,
                            )
                            # new.save()
                            # print(
                            #    "new : " + str(new.type) + ", " + str(new.marque) + ", " + str(new.cneh_code) + ", " + str(
                            #        new.classe_code) + ", " + str(new.complement) + ", " + str(new.discipline) + ", " + str(
                            #        new.id_gmao) + " ")
                        else:
                            message = (
                                "type : " + str(item.tp_type) + ", non ajouté à cause des problèmes suivants : " + message + " "
                            )
                            # print(message)
                            pass
                    bar.next()
                elapsed_time = timezone.now() - start_time
                print("elapsed_time : " + str(elapsed_time))
                print("message : " + str(message))
                '''//////////////////////////////////////////////////////////////////////////////////////////////////'''
                '''PROCESSING'''
                '''le système regarde l'ensemble des types qui n'ont pas de '''
                '''id_gmao et les supprimes si le même type pour une marque existe'''
                print('Check des doublons, veuillez patienter...')
                types_noidgmao = Type.objects.filter(
                    Q(cloture__isnull=True) & (Q(id_gmao__exact='') | Q(id_gmao=None) | Q(id_gmao__isnull=True))
                )
                types_withidgmao = Type.objects.filter(Q(id_gmao__isnull=False) & Q(cloture__isnull=True))
                if (types_noidgmao is not None or not types_noidgmao) and types_noidgmao != 0:
                    with Bar('Processing', max=len(types_noidgmao)) as bar:
                        for typewithout in types_noidgmao:
                            # print('element without:' + str(typewithout))
                            for typewith in types_withidgmao:
                                if typewith.type == typewithout.type:
                                    # print('element with:' + str(typewith))
                                    if typewith.marque == typewithout.marque:
                                        typewithout.cloture = timezone.now()
                                        # typewithout.save()
                                        # print('element en doublon, supprimé'
                                        #       + str(typewithout.type) + 'date fin =' + str(typewithout.cloture))
                            bar.next()
            return self.get(request, *args, **kwargs)

        '''######################################## CODE UPDATE TABLE BUDGET ########################################'''
        if self.model_update == "Compte":
            start_time = timezone.now()
            print('start_time : ' + str(start_time))
            print('Chargement des données de GMAO, veuillez patienter...')
            data = BddImportation.import_data_gmao(self).order_by('nu_compte')
            '''//////////////////////////////////////////////////////////////////////////////////////////////////////'''
            '''PROCESSING'''
            message = ""
            with Bar('Processing', max=len(data)) as bar:
                for item in data:
                    try:
                        # TODO : partie a faire : attention, pas d'ID GMAO, Unicité sur le numero de code et an_exo
                        print(item)
                    except Exception:
                        print('error')
                    bar.next()
            pass
        '''##################################### CODE UPDATE TABLE FOURNISSEUR ######################################'''
        if self.model_update == "Fournisseur":
            message = 'Connecteur non conçu, voir votre administrateur'
            pass
        '''###################################### CODE UPDATE TABLE CONTACTs ########################################'''
        '''code update table des contacts fournisseurs : Contact, ContactPersonn, ContactDescription'''
        if self.model_update == "Contact":
            message = 'Connecteur non conçu, voir votre administrateur'
            pass
        '''###################################### CODE UPDATE TABLE CLASSECODE ########################################'''
        '''code update table des contacts fournisseurs : Contact, ContactPersonn, ContactDescription'''
        if self.model_update == "ClasseCode":
            # TODO : automatiser cette partie : champs ClasseCode et Classelabel
            message = 'Connecteur non conçu, voir votre administrateur'
            pass


class MarcheView(SmartPage):
    name = 'marche'
    application = 'assetplus'
    permissions = '__LOGIN__'
    smart_view_class = AssetPlusMarcheSmartView
    title = _("Marchés dans Asset+")
