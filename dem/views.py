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
import logging

import pandas as pd

from django.db.models import (
    F,
    ExpressionWrapper,
    When,
    Case,
    Value,
)
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.shortcuts import render

from common.base_views import BiomAidViewMixin
from common.models import Programme, Domaine
from common.models import Uf, Pole

from dem.models import Arbitrage
from dem.models import Demande

logger = logging.getLogger(__name__)


def debug(*args, **kwargs):
    logger.debug(" ".join(map(str, args)))


def highlight_ten(val):
    color = "red" if val > 10000 else "black"
    return "color: %s" % color


class CommissionSynthese(BiomAidViewMixin, TemplateView):
    permissions = {'EXP', 'ARB'}
    template_name = 'dem/commission_synthese.html'

    def get_context_data(self, programme_code, validation_cp, **kwargs):
        context = super().get_context_data(**kwargs)
        if programme_code == "Tout" or programme_code == "Tous" or programme_code == "Toutes":
            filtre_programme = "ATTENTION PAS DE FILTRE SUR LE PROGRAMME"
            qs = Demande.objects.all()
        else:
            filtre_programme = Programme.objects.get(code=programme_code)
            qs = Demande.objects.filter(programme=filtre_programme)

        def format(x):
            return "{0:,.2f} €".format(x)

        qs = qs.annotate(
            montant_final=ExpressionWrapper(
                Case(
                    When(
                        enveloppe_allouee__isnull=False,
                        then=F("enveloppe_allouee"),
                    ),
                    When(
                        enveloppe_allouee__isnull=True,
                        then=Coalesce(F('quantite_validee'), F('quantite'))
                        * Coalesce(F('montant_unitaire_expert_metier'), F('prix_unitaire')),
                    ),
                    # montant_final=ExpressionWrapper(
                    #    Case(
                    #     When(
                    #         prix_unitaire__isnull=False,
                    #         then=F("quantite") * F("prix_unitaire"),
                    #     ),
                    #     When(
                    #         montant_unitaire_expert_metier__isnull=False,
                    #         then=F("quantite") * F("montant_unitaire_expert_metier"),
                    #     ),
                    #     When(
                    #         quantite_validee__isnull=False,
                    #         then=F("quantite_validee") * F("prix_unitaire"),
                    #     ),
                    #     When(
                    #         Q(quantite_validee__isnull =False, montant_unitaire_expert_metier__isnull=False),#TODO : ajouter condition and montant_unitaire_expert_metier__isnull=False,
                    #         then=F("quantite_validee") * F("montant_unitaire_expert_metier"),
                    #     ),
                    #     When(
                    #         enveloppe_allouee__isnull=False,
                    #         then=F("enveloppe_allouee"),
                    #     ),
                    # ),
                    # output_field=DecimalField(),
                    # ),
                ),
                output_field=DecimalField(),
            ),
            code_arbitrage=Coalesce(F('arbitrage_commission__code'), Value('0')),
        )

        # Création du Dataframe avec les champs dont les données à utiliser
        df = qs.to_dataframe(
            fieldnames=[
                "uf__pole__nom",
                "uf__nom",
                'montant_final',
                'code_arbitrage',
            ],
            verbose=False,
        ).fillna(0)
        # dfb = qsb.to_dataframe(fieldnames=['code'])
        # Renommage des colonnes pour un affichage propre
        df.columns = ["Pole", "UF", "Enveloppe", "Arbitrage"]
        # debug(df)
        # pivot = df.groupby(['Pole', 'Arbitrage'])['montant'].aggregate('sum').apply(format).unstack().fillna('0.00 €')
        # debug(pivot)

        # ADD Grand Total Ligne :
        gdtl = df.groupby("Arbitrage")[["Enveloppe"]].sum()
        # création du dictionnaire des totaux par arbitrage
        data = []
        # data2 = []
        columns = []
        for i in gdtl.itertuples():
            data.append(float(i.Enveloppe))
            columns.append(int(i[0]))
            df = df.append(
                pd.DataFrame(
                    [("_TOTAL", "", float(i.Enveloppe), str(i[0]))],
                    columns=["Pole", "UF", "Enveloppe", "Arbitrage"],
                )
            )
        pivot2 = df.groupby(["Pole", "Arbitrage"])["Enveloppe"].aggregate("sum").apply(format).unstack().fillna("0.00 €")
        # val = 'TOTAL'
        # idx = [val] + pivot2.index.drop(val).tolist()
        # debug(idx)
        # p = pivot2.index.get_loc('TOTAL') ### Donne l'index de la ligne TOTAL
        # pivot2.reindex(index=pivot2.index[::-1])
        # pivot2.iloc[[p] + [i for i in range(len(pivot2)) if i != p]]
        # debug(pivot2)

        # ADD Grand Total Colonne :
        gdtc = df.groupby("Pole")[["Enveloppe"]].sum()
        gdtc["Enveloppe"] = gdtc["Enveloppe"].apply(format)
        pivotcol = pivot2.join([gdtc], how="outer")
        # debug(pivotcol)

        # création du code html en texte pour affichage en tableau appelé dans le template : {{ tb | safe }}
        tbfinal = pivotcol.to_html

        context.update(
            title=("Commission"),
            qs=qs,
            df=df,
            tbfinal=tbfinal,
            filtre_programme=filtre_programme,
        )
        return context


class ExpertSynthese(BiomAidViewMixin, TemplateView):
    template_name = 'dem/commission_synthese2.html'

    def get_context_data(self, programme_code, pole_code, validation_cp, code_uf, domaines, **kwargs):
        context = super().get_context_data(**kwargs)

        dict_filtre = {}
        # récupération du filtre code pôle
        dict_filtre["code_pole"] = pole_code
        # dict_filtre['decision_validateur'] = validation_cp
        dict_filtre["code_uf"] = code_uf
        if Programme.objects.filter(code=programme_code).exists():
            dict_filtre["programme"] = Programme.objects.get(code=programme_code)
        else:
            dict_filtre["programme"] = "Null"
        # récupération du filtre code domaine
        if Domaine.objects.filter(code=domaines).exists():
            dict_filtre["domaine"] = Domaine.objects.get(code=domaines)
        else:
            dict_filtre["domaine"] = "Null"

        liste_filtre = str(dict_filtre)

        for cle in list(dict_filtre):
            # liste_filtre.append(dict_filtre[cle])
            if (
                dict_filtre[cle] == "Tout"
                or dict_filtre[cle] == "Tous"
                or dict_filtre[cle] == "Toutes"
                or dict_filtre[cle] == "Null"
            ):
                del dict_filtre[cle]

        if not dict_filtre:
            qs = Demande.objects.all()
        else:
            qs = Demande.objects.filter(**dict_filtre)
        if not qs:
            tbfinal = "pas de demandes avec ces critères"
        else:

            def format(x):
                return "{0:,.2f} €".format(x)

            # Création du Dataframe avec les champs dont les données à utiliser
            df = qs.to_dataframe(
                fieldnames=[
                    "nom_pole_court",
                    "nom_uf_court",
                    "enveloppe_allouee",
                    "arbitrage_commission__code",
                ]
            ).fillna(0)
            # dfb = qsb.to_dataframe(fieldnames=['code'])
            # Renommage des colonnes pour un affichage propre
            df.columns = ["Pole", "UF", "montant", "Arbitrage"]
            # debug(df)
            # pivot = df.groupby(['Pole', 'Arbitrage'])['montant']
            #          .aggregate('sum').apply(format).unstack().fillna('0.00 €')
            # debug(pivot)

            # ADD Grand Total Ligne :
            gdtl = df.groupby("Arbitrage")[["montant"]].sum()
            # création du dictionnaire des totaux par arbitrage
            data = []
            # data2 = []
            columns = []
            for i in gdtl.itertuples():
                data.append(float(i.montant))
                columns.append(int(i[0]))
                df = df.append(
                    pd.DataFrame(
                        [("_TOTAL", "", float(i.montant), int(i[0]))],
                        columns=["Pole", "UF", "montant", "Arbitrage"],
                    )
                )
            pivot2 = df.groupby(["Pole", "Arbitrage"])["montant"].aggregate("sum").apply(format).unstack().fillna("0.00 €")
            # val = 'TOTAL'
            # idx = [val] + pivot2.index.drop(val).tolist()
            # debug(idx)
            # p = pivot2.index.get_loc('TOTAL') ### Donne l'index de la ligne TOTAL
            # pivot2.reindex(index=pivot2.index[::-1])
            # pivot2.iloc[[p] + [i for i in range(len(pivot2)) if i != p]]
            # debug(pivot2)

            # ADD Grand Total Colonne :
            gdtc = df.groupby("Pole")[["montant"]].sum()
            gdtc["montant"] = gdtc["montant"].apply(format)
            pivotcol = pivot2.join([gdtc], how="outer")
            # debug(pivotcol)

            # création du code html en texte pour affichage en tableau appelé dans le template : {{ tb | safe }}
            tbfinal = pivotcol.to_html

        context.update(title=("Expertise"), qs=qs, tbfinal=tbfinal, liste_filtre=liste_filtre)

        return context


class DemAide(BiomAidViewMixin, TemplateView):
    permissions = '__LOGIN__'
    template_name = "dem/aide.html"


# ///////////////////////////////////partie commission et expert///////////////////////////////////////


class VueFiltreSynthese(BiomAidViewMixin, TemplateView):
    application = "demande"
    template_name = 'dem/vue_filtre_synthese.html'
    permissions = {'EXP', 'ARB'}
    name = 'filtre_synthèse'
    raise_exception = True  # Refuse l'accès par défaut (pas de demande de login)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programmes = [
            {"id": str(prog.id), "code": str(prog.code), "nom": str(prog.nom)}
            for prog in set(Programme.objects.filter().order_by('code'))
        ]
        programmes_recs = dict({rec.pk: str(rec) for rec in Programme.objects.all().order_by('code')})
        programmes_recs[None] = "--------"
        context['programmes'] = programmes

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context=context)


class VueFiltreSynthese2(BiomAidViewMixin, TemplateView):
    template_name = 'dem/vue_filtre_synthese2.html'
    permissions = {'EXP', 'ARB'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programmes = [
            {"id": str(prog.id), "code": str(prog.code), "nom": str(prog.nom)} for prog in set(Programme.objects.filter())
        ]
        programmes_recs = dict({rec.pk: str(rec) for rec in Programme.objects.all()})
        programmes_recs[None] = "--------"
        pole_all = [{"code": str(pole.code), "nom": str(pole.code) + " - " + pole.nom} for pole in set(Pole.objects.filter())]
        uf_all = [{"code": str(uf.code), "nom": str(uf.code) + " - " + uf.nom} for uf in set(Uf.objects.filter().order_by("code"))]
        arbitrage = [{"id": str(arbi.id), "code": str(arbi.code), "nom": str(arbi.nom)} for arbi in set(Arbitrage.objects.filter())]
        domaines = [{"id": str(dom.id), "code": str(dom.code), "nom": str(dom.nom)} for dom in set(Domaine.objects.filter())]

        context["programmes"] = programmes
        context["poles"] = pole_all
        context["ufs"] = uf_all
        context["arbitrages"] = arbitrage
        context["domaines"] = domaines

        return context
