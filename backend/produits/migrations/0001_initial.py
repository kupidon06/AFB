# Generated by Django 5.0.4 on 2024-07-18 23:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('batiments', '0001_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aliment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unite_mesure', models.CharField(choices=[('kg', 'Kilogrammes'), ('g', 'Grammes'), ('L', 'Litres'), ('ml', 'Millilitres'), ('unité', 'Unité')], default='kg', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='type_poulet_photos/')),
            ],
        ),
        migrations.CreateModel(
            name='Traitement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duree_jours', models.IntegerField(help_text='Durée normale du traitement en jours')),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('date_arrivee', models.DateField()),
                ('age_arrivee', models.IntegerField(default=0)),
                ('nombre_arrivee', models.IntegerField(default=0)),
                ('nombre_actuel', models.IntegerField(default=0)),
                ('nombre_deces', models.IntegerField(default=0)),
                ('nombre_malade', models.IntegerField(default=0)),
                ('traitement_imminent', models.IntegerField(default=0)),
                ('total_oeuf', models.IntegerField(default=0)),
                ('details', models.TextField(blank=True, null=True)),
                ('batiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batiments.batiment')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.race')),
            ],
        ),
        migrations.CreateModel(
            name='JournalisationQuotidienne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_journalisation', models.DateField()),
                ('nombre_vivants', models.IntegerField(default=0)),
                ('nombre_deces', models.IntegerField(default=0)),
                ('nombre_malades', models.IntegerField(default=0)),
                ('autres_informations', models.TextField(blank=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.lot')),
            ],
        ),
        migrations.CreateModel(
            name='Alimentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_alimentation', models.DateField()),
                ('quantite', models.FloatField()),
                ('commentaire', models.TextField(blank=True)),
                ('type_aliment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.aliment')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.lot')),
            ],
        ),
        migrations.CreateModel(
            name='Provision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.FloatField()),
                ('date_provision', models.DateField(default=django.utils.timezone.now)),
                ('aliment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.aliment')),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='RamassageOeufs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ramassage', models.DateField()),
                ('quantite_premier_ramassage', models.IntegerField(default=0)),
                ('quantite_deuxieme_ramassage', models.IntegerField(default=0)),
                ('quantite_troisieme_ramassage', models.IntegerField(default=0)),
                ('quantite_quatrieme_ramassage', models.IntegerField(default=0)),
                ('commentaire', models.TextField(blank=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.lot')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueTraitement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_traitement', models.DateField()),
                ('commentaire', models.TextField(blank=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.lot')),
                ('traitement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.traitement')),
            ],
        ),
    ]
