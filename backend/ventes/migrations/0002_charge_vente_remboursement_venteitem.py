# Generated by Django 5.0.4 on 2024-07-19 00:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_client_name'),
        ('ventes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montant_paye', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date_charge', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.chargecategory')),
                ('fournisseur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.fournisseur')),
            ],
            options={
                'verbose_name_plural': 'Charges',
            },
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_vente', models.DateField(auto_now_add=True)),
                ('remise', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montant_dette', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Remboursement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_remboursement', models.DateField(auto_now_add=True)),
                ('remarque', models.TextField(blank=True)),
                ('vente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.vente')),
            ],
        ),
        migrations.CreateModel(
            name='VenteItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prix_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produit_oeuf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ventes.oeuf')),
                ('produit_poule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ventes.poule')),
                ('vente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ventes.vente')),
            ],
        ),
    ]