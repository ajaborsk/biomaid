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
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F, Case, Value, When, ExpressionWrapper, TextField
from django.db.models.functions import Cast, Coalesce, Concat

from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from common.base_views import BiomAidViewMixin

from common.models import Fournisseur, ContactFournisseur, UserUfRole, User
from dem.smart_views import DemandeSmartView
from drachar.smart_views import PrevisionnelSmartView, DraSmartView, PrevisionnelSmartView21, PrevisionnelUtilisateursSmartView

from drachar.models import Previsionnel, ContactLivraison, Dra, Dossier
from drachar.forms import NouvelleDraForm, LigneForm
from smart_view.smart_page import SmartPage
from smart_view.smart_view import ComputedSmartField
from smart_view.smart_widget import BarChartWidget
from smart_view.views import DoubleSmartViewMixin
from marche.models import Marche


class DracharView(BiomAidViewMixin, TemplateView):
    """
    Classe à dériver pour toutes les vues de DRACHAR.
    C'est une classe abstraite (qui n'est pas conçue pour être instanciée)
    C'est cette classe qui configure le menu principal de l'application.
    """

    application = 'drachar'
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
    }

    def main_tour_steps(self, context):
        return super().main_tour_steps(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs.update({'url_prefix': context.get('url_prefix', None)})
        return context


class TestWidget(BarChartWidget):
    _template_mapping_add = {}

    def _setup(self, **params):
        super()._setup(**params)
        self.params['qs'] = (
            PrevisionnelSmartView21(prefix='', view_params=self.params, appname='drachar')
            .get_base_queryset(self.params)
            .filter(expert=self.params['user'], solder_ligne=False)
            .order_by('-age_previsionnel')
            .annotate(the_state=Value('R'))
            .values('num_dmd__code', 'age_previsionnel', 'the_state')
        )
        self.params['category'] = 'the_state'
        self.params['x'] = {'field': 'num_dmd__code', 'type': 'ordinal', 'sort': '-y'}
        self.params['y'] = 'age_previsionnel:Q'


class DracharHome(DracharView):
    application = 'drachar'
    name = 'drachar-home'
    title = _("Demandes de Réalisation d'ACHAt Reloaded")
    permissions = '__LOGIN__'
    template_name = 'drachar/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_widget'] = TestWidget(params=self.view_params)
        # context['main_widget'] = VueGridWidget(**self.view_params)
        return context


# class GestionContactLiv22(GestionData):#TODO à continuer, marche dans common mais pas dans DRACHAR ...
#
#    url = "drachar/gestion_contact_liv.html/"
#    template_name = 'common/gestiondata.html'
#    titre_template = _("Gestion contacts livraison")
#    model = ContactLivraison  # model à utiliser
#    form = ContactLivForm  # formulaire à utiliser
#    item_message = "Contacts livraison"  # %s pour les messages automatisés
#    ordre_affichage = ['id','etablissement', 'code', 'nom', 'prenom', 'coordonnees']
#    template_col_title = ["ID","Etablissement","CODE","NOM","PRENOM","TELEPHONE"]
#    template_lig_var = ['id','etablissement', 'code', 'nom', 'prenom', 'coordonnees']
#    template_additional = None
#    formats = {"string": "", "string": "", "string": "", "string": "", "string": "", "string": ""}
#    nbcol = len(template_col_title)
#    q_query = []
#    def crit_unic_to_get(self, item):
#        return {
#            'nom__iexact': getattr(item, "nom"),
#            'code__iexact': getattr(item, "code"),
#        }
#
#    #def additional_def(self, request, item):
#    bdd = ''  # Base de données à utiliser
#    model_update = "ContactLivraison"
#    def parametre_connexion(self, kwargs):
#        self.lien = "OFF"
#        self.etabprefix = "DEFAUT"


class DraData:
    def get(self, request, *args, **kwargs):
        template_name = 'drachar/nouvelledra.html'
        data = {
            "four_list": Fournisseur.objects.filter(Q(cloture__isnull=True)),
            "contact_four_list": ContactFournisseur.objects.filter(Q(cloture__isnull=True)),
            "marche_list": Marche.objects.filter(Q(cloture__isnull=True)),
            "dossier_list": Dossier.objects.filter(Q(cloture__isnull=True)),
            "contact_liv_list": ContactLivraison.objects.filter(Q(cloture__isnull=True)),
            "expert_metier_list": User.objects.filter(Q(userufrole__role_code='EXP')).exclude(username='arbitre_biomed')
        }
        form_dra = self.formulaire_dra(request.user, request.GET, **data)
        self.message = _("""ajout d'une DRA""")
        self.template_name = template_name
        return form_dra


class Nouvelle_draView(DracharView, DraData):
    name = 'new-dra'
    template_name = 'drachar/nouvelledra.html'
    title = _("Nouvelle DRA")
    formulaire_dra = NouvelleDraForm
    dra = DraData
    dra_id = None

    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.message = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['message'] = self.message
        # context['ligne'] = self.ligne
        # kwargs.update({'url_prefix': context.get('url_prefix', None)})
        return context

    def get(self, request, **kwargs):
        # Appel du formulaire DRA
        context = self.get_context_data()
        self.dra_id = kwargs.get('dra_id')
        context['dra_id'] = self.dra_id
        # print(context['url_prefix'])
        if self.dra_id is not None:  # FORMULAIRE DEJA RENSEIGNE : Modifification ou demande en cours pré enregistrée
            context['title'] = "DRA N° " + str(self.dra_id)
            kwargs['dra_id'] = self.dra_id
            Instance_dra = Dra.objects.get(pk=self.dra_id)
            context['form_dra'] = Instance_dra
            # print("dra existante n° = " + str(Instance_dra))
            return render(request, self.template_name, context=context)
        # TODO : Instance à faire en fonction de l'endroit à partir duquel on genère la DRA
        #  (depuis une ligne, depuis un dossier...) pour préremplir certains champs
        else:  # NOUVEAU FORMULAIRE
            context['title'] = "Création d'une Demande de Réalisation d'Achat"
            form = self.dra.get(self, request)
            context['form_dra'] = form
            return render(request, self.template_name, context=context)

    
    def post(self, request, *args, **kwargs):
        self.form_dra = self.formulaire_dra(request.POST or None)
        context = self.get_context_data()
        submit = request.POST.get("submit")
        print("submit" + str(submit))
        if submit == "AJOUTER_UNE_LIGNE":
            if self.form_dra.is_valid():
                self.save(request)
            else:
                print(self.form_dra.errors)
            context['form_dra'] = self.form_dra
            return redirect("../nouvelleligne/%s" % self.dra_id, context=context)
        elif submit == "ENREGISTRER":
            if self.form_dra.is_valid():
                self.save(request)
            else:
                print(self.form_dra.errors)
            context['dra_id'] = self.dra_id
            context['form_dra'] = self.form_dra
            return render(request, self.template_name, context=context)
        else:
            self.message = _("Problème" + str(self.form_dra.errors))
            return render(request, self.template_name, context=context)

    def save(self, request, *args, **kwargs):
        if not self.dra_id:
            print("save new")
            print("valide")
            dra = self.form_dra.save(commit=False)
            dra.intitule = self.form_dra.cleaned_data["intitule"]
            dra.fournisseur = self.form_dra.cleaned_data["fournisseur"]
            dra.contact_fournisseur = self.form_dra.cleaned_data["contact_fournisseur"]
            dra.num_devis = self.form_dra.cleaned_data["num_devis"]
            dra.date_devis = self.form_dra.cleaned_data["date_devis"]
            dra.num_marche = self.form_dra.cleaned_data["num_marche"]
            dra.expert_metier = self.form_dra.cleaned_data["expert_metier"]
            dra.num_bon_commande = self.form_dra.cleaned_data["num_bon_commande"]
            dra.num_dossier = self.form_dra.cleaned_data["num_dossier"]
            # dra.documents = self.form_dra.cleaned_data["documents"] # TODO : fonction ajout documents
            dra.date_commande = self.form_dra.cleaned_data["date_commande"]
            dra.contact_livraison = self.form_dra.cleaned_data["contact_livraison"]
            # TODO : récupérer id DRA et N° ligne pour ajout ligne
            # self.dra_id = self.form_dra.id
            # self.ligne = 0
            print(dra.intitule)
            print(dra.fournisseur)
            print(dra.contact_fournisseur)
            print(dra.num_devis)
            print(dra.date_devis)
            print(dra.num_marche)
            print(dra.expert_metier)
            print(dra.num_bon_commande)
            print(dra.num_dossier)
            # print(dra.documents)
            print(dra.date_commande)
            print(dra.contact_livraison)
            # dra.save()
            # super().save(*args, **kwargs) => a garder ?
            # self.dra_id = dra.id
            # TODO : attention a supprimer : pour tests add ligne :
            self.dra_id = '2'
            print(self.dra_id)
            dra_id = self.dra_id
        else:
            print("save modif")
            # code de modification


class LigneClass:
    def get(self, request, *arg, **kwargs):
        template_name = 'drachar/nouvelleligne.html'
        data = {
            "num_previsionnel": Previsionnel.objects.filter(Q(solder_ligne=False)),
            # "num_compte": Compte.objects.filter(Q())
            # TODO : ligne a corriger à cause de ID dans le models : "num_previsionnel":
            #  Previsionnel.objects.filter(Q(solder_ligne=True,
            #                   expert=ExtensionUser.objects.get(user=self.request.user))),
            # TODO : faire le code pour l'importation depuis asset+ des comptes
        }
        form = self.form_ligne(request.user, request.GET, **data)
        self.message = _("""ajout d'une ligne""")
        self.template_name = template_name
        return form


class NouvelleLigneView(DracharView, LigneClass):

    form_ligne = LigneForm
    template_name = 'drachar/nouvelleligne.html'
    initial = {}
    ligneclass = LigneClass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajout d'une ligne de commande"
        context['message'] = self.message
        context['dra_id'] = self.dra_id
        return context

    def get(self, request, dra_id, *args, **kwargs):
        # Instance_dra = Dra.objects.get(pk=kwargs.dra_id)
        form = self.ligneclass.get(self, request)
        dra_id = dra_id  # TODO : renvoyer également le num de la DRA.
        return render(request, self.template_name, {'form_ligne': form, 'dra_id': dra_id})

    def post(self, request, *args, **kwargs):
        form = self.form_ligne(request.POST)

        if form.is_valid():
            ligne = form.save(commit=False)
            ligne.num_previsionnel = form.cleaned_data["num_previsionnel"]
            return redirect('/drachar/nouvelle_dra/%s' % ligne.num_previsionnel)  # TODO: ajouter le numero de la dra concernée
        else:
            self.message = _("Problème" + str(form.errors))
            return super().post(request, *args, **kwargs)


# TODO : envoie d'email exemple :
'''
from django.core.mail import send_mail

if form.is_valid():
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']

    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)

    send_mail(subject, message, sender, recipients)
    return HttpResponseRedirect('/thanks/')
    '''
# TODO : mise en pdf finale des documents et de la dra :
'''
pdf : reportlab bilio python
'''

'''class NouvelleDraClass():

    def __init__(self):
        self.extra_forms = 1
        print('exta_form')
        print(self.extra_forms)

    def nouvelle_dra(request):  # http://127.0.0.1:8000/DRACHAR/nouvelledra/
        """ Vue pour création d'une DRA
        METHODE GET :
            - chargement des différentes listes déroulantes avec recherche :
                    fournisseurs, contacts fournisseurs, marchés,
              contacts livraison.
            - chargement du formulaire principal
        """
        extra_forms = 1
        #form_dra1 = modelformset_factory(Dra, NouvelleDra)
        #form_dra = form_dra1(queryset=Dra.objects.none())
        if request.method == 'GET':
            print("GET")
            four_list = Fournisseur.objects.filter(Q(cloture__isnull=True))
            print(four_list)
            contact_four_list = ContactFournisseur.objects.filter(Q(cloture__isnull=True))
            print(contact_four_list)
            marche_list = Marche.objects.all()
            print(marche_list)
            contact_liv_list = ContactLivraison.objects.filter(Q(cloture__isnull=True))
            print(contact_liv_list)
            form_dra = NouvelleDra(request.user,
                                   request.GET,
                                   data_list1=four_list,
                                   data_list2=contact_four_list,
                                   data_list3=marche_list,
                                   data_list4=contact_liv_list,
                                   )
            #form_dra = NouvelleDra(request.user, request.POST or None)


            DocForm_model_formset = modelformset_factory(Document, DocForm, extra=extra_forms, max_num=5)
            formsetDoc = DocForm_model_formset(queryset=DocumentDracharLink.objects.none())
            # DocForm_model_formset = modelformset_factory(DocumentDracharLink,
                    DocFormliendra, extra=extra_forms, max_num=5)
            # formsetlien = DocForm_model_formset(queryset=DocumentDracharLink.objects.none())

            context = drachar_context(request, title=_("Nouvelle demande d'achat"))
            context.update(
                {
                    #"contact_livraison": ContactLivraison.objects.filter(Q(cloture__isnull=True)),
                    #"fournisseurs": fournisseurs,
                    #"contactsfournisseurs": contactsfournisseurs,
                })
            context.update(
                {
                    "form_dra": form_dra,
                    "formsetDoc": formsetDoc,
                })
        elif request.method == 'POST':
            print("POST")
            four_list = Fournisseur.objects.filter(Q(cloture__isnull=True))
            contact_four_list = ContactFournisseur.objects.filter(Q(cloture__isnull=True))
            marche_list = Marche.objects.filter(Q(cloture__isnull=True))
            contact_liv_list = ContactLivraison.objects.filter(Q(cloture__isnull=True))
            form_dra = NouvelleDra(request.user,
                                   request.POST or None,
                                   data_list1=four_list,
                                   data_list2=contact_four_list,
                                   data_list3=marche_list,
                                   data_list4=contact_liv_list,
                                   )
            # test pour voir s'il faut ajouter des documents :
            #if "additemsdoc" in request.POST and request.POST["additemsdoc"] == "True":
            #    formset_dictionary_copy = request.POST.copy()
            #    formset_dictionary_copy["form-TOTAL_FORMS"] = (
            #        int(formset_dictionary_copy["form-TOTAL_FORMS"]) + 1
            #    )
            #    formsetDoc = DocForm_model_formset(formset_dictionary_copy)
            #    print('additemdoc')
            #    context["formsetDoc"] = formsetDoc
            ##s'il ne faut pas ajouter de documents
            ## test pour s'il faut ajouter des lignes :
            ## elif "additemsligne" in request.POST and request.POST["additemsligne"] == "True":
            ## _____> ci-dessous ne semble plus nécessaire
            #else:
            #    formsetDoc = DocForm_model_formset(request.POST, prefix="doc")
            #    form_dra = NouvelleDra(request.user, request.POST or None)
            #    print("ici")
            #    if form_dra.is_valid() and formsetDoc.is_valid:
            #       print('is-valid pass')
            #       context.update(
            #            {
            #                "form_dra": form_dra,
            #            })
            #context["formsetDoc"] = formsetDoc
            #formsetDoc = DocForm_model_formset(request.POST, prefix="doc")
            context = drachar_context(request, title=_("Nouvelle demande d'achat"))
            context.update(
                {
                    "form_dra": form_dra,
                })
        if "submit" in request.POST:
            form_dra = NouvelleDra(request.user,
                                   request.POST or None,
                                   data_list1=four_list,
                                   data_list2=contact_four_list,
                                   data_list3=marche_list,
                                   data_list4=contact_liv_list,
                                   )
            print("submit")
            if form_dra.is_valid(): # and formsetDoc.is_valid:
                post = form_dra.save(commit=False)
                print('form_dra.is-valid pass :')
                post.intitule = form_dra.cleaned_data["intitule"]
                post.expert_metier = form_dra.cleaned_data["expert_metier"]
                post.fournisseur = form_dra.cleaned_data["fournisseur"]
                post.contact_fournisseur = form_dra.cleaned_data["contact_fournisseur"]
                post.num_devis = form_dra.cleaned_data["num_devis"]
                post.date_devis = form_dra.cleaned_data["date_devis"]
                post.num_marche = form_dra.cleaned_data["num_marche"]
                post.num_bon_commande = form_dra.cleaned_data["num_bon_commande"]
                post.date_commande = form_dra.cleaned_data["date_commande"]
                post.contact_livraison = form_dra.cleaned_data["contact_livraison"]

                print(post.intitule)
                print(post.expert_metier)
                print(post.fournisseur)
                print(post.contact_fournisseur)
                print(post.num_devis)
                print(post.date_devis)
                print(post.num_marche)
                print(post.num_bon_commande)
                print(post.date_commande)
                print(post.contact_livraison)

                context.update(
                    {
                    "form_dra": form_dra,
                    #"formsetDoc": formsetDoc,
                    })
            else:
                message = _(
                    "Erreur d'enregistrement ; certains champs obligatoires sont vides"
                )
                errors = form_dra.errors.get_json_data()
                print(form_dra.errors)
                #print(formsetDoc.errors)
                context.update(
                    {
                    "form_dra": form_dra,
                    #"formsetDoc": formsetDoc,
                    "message": message,
                    "errors": errors,
                    })
        return render(request, "drachar/nouvelledra.html", context)'''


class MesDossiersView(SmartPage):
    name = 'my-files'
    smart_view_class = PrevisionnelSmartView
    title = _("Mes dossiers")
    smart_modes = {
        None: {'view': 'list'},
    }


class SingleDemandeSmartView(DemandeSmartView):
    class Meta:
        columns = (
            'num_dmd',
            'roles',
            'state_code',
            'date_premiere_demande',
            'pole_nom',
            'uf_code',
            'uf_nom',
            'redacteur_nom',
            'priorite',
            'nom_projet',
            'libelle',
            'cause',
            'materiel_existant',
            'referent',
            'quantite',
            'prix_unitaire',
            # 'montant',
            'impact_travaux',
            'impact_informatique',
            'argumentaire_detaille',
            'documents_sf',
            'avis_cadre_sup',
            'commentaire_cadre_sup',
            'decision_validateur',
            'decision_soumission',
            'programme',
            'domaine',
            'expert_metier',
            'montant_unitaire_expert_metier',
            # 'montant_total_expert_metier',
            'commentaire_biomed',
            'avis_biomed',
            'montant_arbitrage',
            'arbitrage_commission',
            'commentaire_provisoire_commission',
            'commentaire_definitif_commission',
            # 'quantite_validee',
            'qte',  # Quantité validée OU quantité initiale
            'enveloppe_allouee',
            'gel',
        )
        current_row_manager = False

        # form_layout = (
        #     'form',
        #     {},
        #     (
        #         ('title', "Titre du formulaire"),
        #         ('row', ('$num_dmd$',)),
        #         (
        #             'section',
        #             {},
        #             (
        #                 ('title', "Titre de la section"),
        #                 ('row', ('$priorite$', '$quantite$')),
        #                 ('row', ('$libelle$', '$nom_projet$')),
        #                 ('sep',),
        #             ),
        #         ),
        #     ),
        # )
        views = ('table',)

    qte = (
        ComputedSmartField,
        {
            'title': 'Qté validée',
            'format': 'integer',
            'data': Case(
                When(quantite_validee__isnull=False, then=F('quantite_validee')),
                default=F('quantite'),
            ),
        },
    )


class PrevisionnelView(DoubleSmartViewMixin, BiomAidViewMixin, TemplateView):
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
    }
    main_smart_view_class = PrevisionnelSmartView21
    name = 'previsionnel'
    main_field_name = 'num_dmd'
    managed_field_name = 'num_dmd'
    field_smart_view_class = SingleDemandeSmartView
    title = _("Prévisionnel")


class SuiviAcquisitions(SmartPage):
    application = 'dem'
    name = 'suivi-acquisitions'
    permissions = (
        'RMA',
        'CAD',
        'RUN',
        'CHS',
        'CADS',
        'AMAR',
        'DRP',
        'CAP',
        'CSP',
        'ACHP',
        'CHP',
        'COP',
        'DIR',
        'EXP',
        'TECH',
    )
    smart_view_class = PrevisionnelUtilisateursSmartView
    title = "Suivi des demandes acceptées"
    smart_modes = {
        None: {'view': 'list'},
    }


class listedra(SmartPage):
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
    }
    smart_view_class = DraSmartView
    name = 'liste-dra'
    title = _("Liste DRA")
    smart_modes = {
        None: {'view': 'list'},
    }


class CockpitView(BiomAidViewMixin, TemplateView):
    permissions = {
        'EXP',
        'ACH',
        'DIS',
        'ARB',
        'ADM',
    }
    template_name = "drachar/cockpit.html"
    name = 'cockpit'
    title = _("Cockpit DRACHAR")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['programme_tous'] = {'programme': 'Tous'}
        return context
