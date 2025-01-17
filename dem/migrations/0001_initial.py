# Generated by Django 3.0.7 on 2020-08-17 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acheteur',
            fields=[
                ('code', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('nom', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('prenom', models.CharField(max_length=30)),
                ('dect', models.CharField(max_length=30)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'code',
                    models.DecimalField(
                        choices=[
                            (0, 'Non défini'),
                            (1, 'Déjà livré, Cdé'),
                            (2, 'Validé'),
                            (3, 'Non validé'),
                            (4, 'Refusé'),
                            (5, 'Classe 6 - petit matériel'),
                            (6, 'Doublon - programme antérieur'),
                        ],
                        decimal_places=0,
                        default=1,
                        max_digits=5,
                    ),
                ),
                ('nom', models.CharField(max_length=30)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
        ),
        migrations.CreateModel(
            name='Calendrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(default='2020', verbose_name='Annee du Recensement')),
                ('debut_recensement', models.DateTimeField(verbose_name='date début des demandes')),
                ('fin_recensement', models.DateTimeField(verbose_name='date de fin des demandes')),
            ],
            options={
                'verbose_name': 'calendrier gestion demandes',
                'verbose_name_plural': 'calendriers gestion demandes',
            },
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('num_dmd', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, default='2020-01-01', null=True, verbose_name='Année de la demande')),
                (
                    'nom_projet',
                    models.CharField(
                        default=None,
                        help_text="Si plusieurs demandes concernent un même projet,"
                        " donner le même nom de projet. Sinon, le projet est la demande en elle-même"
                        " (rempli automatiquement). Sauf exception, toutes les demandes d'un même"
                        " projet seront validées (ou pas) simultanément.",
                        max_length=120,
                        verbose_name='Nom du Projet',
                    ),
                ),
                ('validateur', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('decision_validateur', models.BooleanField(default=False, verbose_name='Décision')),
                ('decision_soumission', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('date_decision', models.DateField(blank=True, default=None, null=True, verbose_name='date décision')),
                ('nom_organisation', models.CharField(max_length=50)),
                ('code_pole', models.DecimalField(decimal_places=0, default=0, max_digits=5, verbose_name='N° pôle')),
                ('nom_pole_court', models.CharField(max_length=50)),
                (
                    'code_uf',
                    models.DecimalField(
                        decimal_places=0,
                        default=0,
                        help_text="Numéro de l'UF qui va bénéficier de ce matériel",
                        max_digits=5,
                        verbose_name='N° UF',
                    ),
                ),
                ('nom_uf_court', models.CharField(max_length=50)),
                (
                    'referent',
                    models.CharField(
                        default=None,
                        help_text="Personne du service à l'origine  de la demande, qui peut être contactée pendant l'instruction pour avoir des précisions.",
                        max_length=30,
                        null=True,
                        verbose_name='Référent',
                    ),
                ),
                (
                    'contact',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="Nom de la personne qui sera contactée pour gérer l'acquisition et/ou représenter"
                        " les utilisateurs lors de l'opération d'acquisition. Le référent est utilisé par défaut.",
                        max_length=30,
                        null=True,
                        verbose_name='Contact',
                    ),
                ),
                (
                    'dect_contact',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text='Coordonnées téléphoniques de la personne à contacter (si possible un numéro de DECT)',
                        max_length=30,
                        null=True,
                        verbose_name='Téléphone / DECT',
                    ),
                ),
                (
                    'date_premiere_demande',
                    models.DateField(
                        blank=True,
                        default='2020-01-01',
                        help_text="Année où la demande a été présentée la première fois à la Commission d'arbitrage",
                        null=True,
                        verbose_name='Première demande',
                    ),
                ),
                (
                    'priorite',
                    models.CharField(
                        choices=[('1', 'Haute'), ('2', 'Normale'), ('3', 'Basse')], default=2, max_length=3, verbose_name='Priorité'
                    ),
                ),
                (
                    'libelle',
                    models.CharField(
                        default=None,
                        help_text='Indiquez le nom (commun) du matériel demandé',
                        max_length=120,
                        verbose_name='Objet de la demande',
                    ),
                ),
                (
                    'cause',
                    models.CharField(
                        choices=[
                            ('RE', 'Remplacement'),
                            ('AQ', 'Augmentation de Quantité'),
                            ('EV', 'Evolution'),
                            ('TN', 'Technique Nouvelle'),
                        ],
                        default='AQ',
                        help_text="C'est la raison pour laquelle cette demande est faite.",
                        max_length=3,
                        verbose_name='Raison',
                    ),
                ),
                (
                    'materiel_existant',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="Matériel existant concerné par la demande de remplacement ou d'évolution.",
                        max_length=64,
                        null=True,
                        verbose_name='Matériel concerné',
                    ),
                ),
                (
                    'quantite',
                    models.DecimalField(
                        decimal_places=0,
                        default=1,
                        help_text="Quantité d'équipements souhaités",
                        max_digits=3,
                        verbose_name='Quantité',
                    ),
                ),
                (
                    'prix_unitaire',
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=None,
                        help_text="Indiquer ici une estimation du prix unitaire de l'équipement,"
                        " en euros TTC, de l'équipement demandé. S'il s'agit d'une technique  nouvelle,"
                        " il est indispensable de joindre un devis à la demande.",
                        max_digits=9,
                        null=True,
                        verbose_name='P.Unit. (TTC)',
                    ),
                ),
                (
                    'couts_complementaires',
                    models.BooleanField(
                        blank=True,
                        default=None,
                        help_text="Existe-t-il des coûts de consommables, de maintenance, de travaux ou d'autres coûts"
                        " lié à l'achat ou l'utilisation de ce matériel ?",
                        verbose_name='Coûts de fonctionnement',
                    ),
                ),
                (
                    'autre_argumentaire',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text='Autre raison pour laquelle vous demandez ce matériel',
                        max_length=3000,
                        verbose_name='Autre justification',
                    ),
                ),
                (
                    'montant',
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=None,
                        help_text='Par défaut, le montant est calculé à partir de la quantité et du prix unitaire.',
                        max_digits=9,
                        null=True,
                        verbose_name='Montant de la demande (TTC)',
                    ),
                ),
                (
                    'consommables_eventuels',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="Consommables éventuels (stériles ou non) associé à l'équipement demandé :"
                        " Types, description, quantités annuelles...",
                        max_length=3000,
                        null=True,
                        verbose_name='Consommables',
                    ),
                ),
                (
                    'impact_travaux',
                    models.BooleanField(
                        blank=True,
                        default=None,
                        help_text='Ce projet nécessite-t-il de réaliser des travaux ?',
                        null=True,
                        verbose_name='Impact travaux',
                    ),
                ),
                (
                    'impact_informatique',
                    models.BooleanField(
                        blank=True,
                        default=None,
                        help_text='Ce projet nécessite-t-il des ressources informatiques (logiciel, matériel, réseau...) ?',
                        null=True,
                        verbose_name='Impact informatique',
                    ),
                ),
                (
                    'montant_unitaire_acheteur',
                    models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=9, null=True),
                ),
                (
                    'montant_acheteur_total',
                    models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=9, null=True),
                ),
                (
                    'acquisition_possible',
                    models.BooleanField(blank=True, null=True, verbose_name='Acquisition possible en année N'),
                ),
                (
                    'quantite_validee',
                    models.DecimalField(
                        decimal_places=0,
                        default=1,
                        help_text="quantité d'équipements validée par commission",
                        max_digits=3,
                        null=True,
                        verbose_name='Quantité validée',
                    ),
                ),
                (
                    'enveloppe_allouee',
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=None,
                        max_digits=9,
                        null=True,
                        verbose_name="montant de l'enveloppe allouée",
                    ),
                ),
                (
                    'avis_biomed',
                    models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name="Avis de l'acheteur"),
                ),
                ('commentaire_biomed', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('soumis_a_avis', models.BooleanField(blank=True, null=True)),
                (
                    'commentaire_provisoire_commission',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text='Commentaires de la commission lors des auditions',
                        max_length=60,
                        null=True,
                    ),
                ),
                (
                    'commentaire_definitif_commission',
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text='Commentaires définitifs de la commission concernant la demande',
                        max_length=60,
                        null=True,
                    ),
                ),
                ('gel', models.BooleanField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, null=True, verbose_name='date de modification')),
                (
                    'avis_commission',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='dem.Avis',
                        verbose_name='Avis de la commission',
                    ),
                ),
                (
                    'code_acheteur',
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dem.Acheteur'),
                ),
            ],
            options={
                'ordering': ['num_dmd'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'code',
                    models.CharField(
                        blank=True,
                        choices=[
                            ('DE', 'Devis'),
                            ('CO', 'Doc commerciale'),
                            ('CR', 'Email, courrier'),
                            ('IM', 'Photo'),
                            ('AS', 'Article scientifique'),
                            ('TR', 'Texte réglementaire'),
                            ('RE', 'Recommandations'),
                            ('RC', 'Compte-rendu'),
                            ('PM', 'Planning de mutualisation'),
                            ('BP', 'Business Plan'),
                            ('ME', 'Etude médico-économique'),
                            ('TE', 'Doc technique'),
                            ('DI', 'Autre'),
                        ],
                        help_text='Choisissez le type du document à joindre',
                        max_length=3,
                        verbose_name='Type',
                    ),
                ),
                (
                    'UNCpath',
                    models.FileField(
                        blank=True,
                        help_text='Sélectionnez dans vos dossiers le fichier à ajouter',
                        max_length=255,
                        upload_to='',
                        verbose_name='Fichier',
                    ),
                ),
                (
                    'commentaire',
                    models.CharField(
                        blank=True,
                        help_text='Vous pouvez y intégrer un commentaire pour décrire le document',
                        max_length=255,
                        verbose_name='Note',
                    ),
                ),
                ('status', models.BooleanField(default=False)),
                ('createur', models.CharField(blank=True, max_length=255, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
            options={
                'verbose_name': 'document joint',
                'verbose_name_plural': 'documents joints',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'code',
                    models.CharField(
                        choices=[
                            ('BIO', 'Biomédical'),
                            ('EQT', 'Equipement'),
                            ('ST', 'Service Technique'),
                            ('DSN', 'Informatique'),
                            ('DIV', 'Divers'),
                        ],
                        default='B',
                        max_length=3,
                    ),
                ),
                ('nom', models.CharField(max_length=30)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, null=True, verbose_name='date de modification')),
            ],
        ),
        migrations.CreateModel(
            name='Domaine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('nom', models.CharField(max_length=30)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('acheteur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dem.Acheteur')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dem.Plan')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demande', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dem.Demande')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dem.Document')),
            ],
        ),
        migrations.AddField(
            model_name='demande',
            name='documents',
            field=models.ManyToManyField(blank=True, through='dem.DocumentLink', to='dem.Document'),
        ),
        migrations.AddField(
            model_name='demande',
            name='domaine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dem.Domaine'),
        ),
        migrations.AddField(
            model_name='demande',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dem.Plan'),
        ),
        migrations.AddField(
            model_name='demande',
            name='redacteur',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Rédacteur'
            ),
        ),
        migrations.AddField(
            model_name='demande',
            name='uf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Uf'),
        ),
        migrations.CreateModel(
            name='CoutComplementaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'type_surcout',
                    models.DecimalField(
                        blank=True,
                        choices=[(1, 'Consommable'), (2, 'Maintenance'), (3, 'Informatique'), (4, 'Travaux'), (5, 'Autre')],
                        decimal_places=0,
                        max_digits=5,
                        null=True,
                    ),
                ),
                ('nom_surcout', models.CharField(blank=True, max_length=50, null=True)),
                ('reference_surcout', models.CharField(blank=True, max_length=50, null=True)),
                (
                    'cout_unitaire_surcout',
                    models.DecimalField(blank=True, decimal_places=0, max_digits=5, verbose_name='cout unitaire'),
                ),
                (
                    'qt_annuelle_surcout',
                    models.DecimalField(blank=True, decimal_places=0, max_digits=5, verbose_name='quantité annuelle'),
                ),
                ('num_dmd', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='dem.Demande')),
            ],
        ),
        migrations.CreateModel(
            name='ArgumentaireDetaille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'interet_medical',
                    models.BooleanField(
                        default=False, help_text='Cette demande apporte-t-elle un intérêt médical ?', verbose_name='Intérêt médical'
                    ),
                ),
                (
                    'commentaire_im',
                    models.TextField(
                        blank=True,
                        help_text="Indiquez ici quel bénéfice ce matériel pourrait apporter à la prise en charge.\n\n"
                        "N'hésitez pas à joindre des documents (publications, références, expériences, ...)"
                        " à la demande pour appuyer votre argumentation.",
                        verbose_name="Précisions sur l'intérêt médical",
                    ),
                ),
                (
                    'oblig_reglementaire',
                    models.BooleanField(
                        default=False,
                        help_text='Existe-t-il une obligation réglementaire liée à cette demande ?',
                        verbose_name='Obligation réglementaire',
                    ),
                ),
                (
                    'commentaire_or',
                    models.TextField(
                        blank=True,
                        help_text="Indiquez ici quelle est l'obligation réglementaire (référence du texte)"
                        " et en quoi cela participe à l'argumentation.\n\n"
                        "N'hésitez pas à joindre des documents (textes, analyse...)"
                        " à la demande pour appuyer votre argumentation.",
                        verbose_name="Précisions sur l'obligation réglementaire",
                    ),
                ),
                (
                    'recommandations',
                    models.BooleanField(
                        default=False,
                        help_text='Y a-t-il des recommandations liées à cette demande ?',
                        verbose_name='Recommandations',
                    ),
                ),
                (
                    'commentaire_r',
                    models.TextField(
                        blank=True,
                        help_text="Indiquez quelles sont les recommandations (références, organisme) et comment elles sont en faveur de la demande.            \n\nN'hésitez pas à joindre des documents (recommandations) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions recommandations',
                    ),
                ),
                (
                    'projet_chu_pole',
                    models.BooleanField(
                        default=False,
                        help_text="La demande est-elle liée à un projet de pôle ou au projet d'établissement ?",
                        verbose_name='Projet institutionnel',
                    ),
                ),
                (
                    'commentaire_pcp',
                    models.TextField(
                        blank=True,
                        help_text="Préciser si la demande est liée à un projet du pôle ou de l'établissement et le niveau de validation du projet en question.            \n\nN'hésitez pas à joindre des documents (descriptif du projet, validation...) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions projet institutionnel',
                    ),
                ),
                (
                    'confort_patient',
                    models.BooleanField(
                        default=False,
                        help_text="La demande a-t-elle en vue d'améliorer le confort patient ?",
                        verbose_name='Confort patient',
                    ),
                ),
                (
                    'commentaire_cp',
                    models.TextField(
                        blank=True,
                        help_text="Précisez comment l'objet de la demande pourra améliorer le confort ou l'expérience des patients.            \n\nN'hésitez pas à joindre des documents (articles, essais...) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions confort patient',
                    ),
                ),
                (
                    'confort_perso_ergo',
                    models.BooleanField(
                        default=False,
                        help_text="La demande améliore-t-elle l'ergonomie ou le confort du personnel ?",
                        verbose_name='Ergonomie du travail',
                    ),
                ),
                (
                    'commentaire_pe',
                    models.TextField(
                        blank=True,
                        help_text="Détaillez quel impact sur l'ergonomie ou le confort du personnel pourrait avoir la demande            \n\nN'hésitez pas à joindre des documents (étude de poste, etc.) à la demande pour appuyer votre argumentation.",
                        verbose_name="Précisions sur l'ergonomie",
                    ),
                ),
                (
                    'notoriete',
                    models.BooleanField(
                        default=False,
                        help_text="La demande permettrait-elle d'améliorer la notoriété de l'établissement ?",
                        verbose_name='Notoriété, Attractivité',
                    ),
                ),
                (
                    'commentaire_n',
                    models.TextField(
                        blank=True,
                        help_text="Indiquez ici comment l'accord de la demande participerait à la notoriété de l'établissement au sein du territoire et avec quelle ampleur            \n\nN'hésitez pas à joindre des documents (rapport de consultant, etc.) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions sur la notoriété',
                    ),
                ),
                (
                    'innovation_recherche',
                    models.BooleanField(
                        default=False,
                        help_text='La demande concerne-t-elle un projet innovant ou de recherche ?',
                        verbose_name='Innovation / Recherche',
                    ),
                ),
                (
                    'commentaire_ir',
                    models.TextField(
                        blank=True,
                        help_text="Indiquez ici en quoi cette demande participerait à l'innovation, les éventuels liens avec la commission innovation pour le financement du fonctionnement. Vous pouvez aussi préciser le nom du projet du reherche associé.            \n\nN'hésitez pas à joindre des documents (article scientifique, projet de recherche, etc.) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions innovation/recherche',
                    ),
                ),
                (
                    'mutualisation',
                    models.BooleanField(
                        default=False,
                        help_text="L'équipement demandé sera-il mutualisé avec d'autres services ?",
                        verbose_name='Mutualisation',
                    ),
                ),
                (
                    'commentaire_m',
                    models.TextField(
                        blank=True,
                        help_text="Préciser avec quel(s) autre(s) service(s) la mutualisation est envisagée, selon quelles modalités (répartition des plages horaires, vacations, etc.)            \n\nN'hésitez pas à joindre des documents (planning de partage, accord autre service, CR de réunion...) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions sur la mutualisation',
                    ),
                ),
                (
                    'gain_financier',
                    models.BooleanField(
                        default=False,
                        help_text='La demande permettrait-elle de réaliser des gains économiques ?',
                        verbose_name='Gains économiques',
                    ),
                ),
                (
                    'commentaire_gf',
                    models.TextField(
                        blank=True,
                        help_text="Précisez ici comment la demande pourrait entrainer une économie ou une recette pour l'établissement.            \n\nN'hésitez pas à joindre des documents (étude médico-économique, business plan...) à la demande pour appuyer votre argumentation.",
                        verbose_name='Précisions gains économiques',
                    ),
                ),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, null=True, verbose_name='date de modification')),
                ('demande', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dem.Demande')),
            ],
        ),
    ]
