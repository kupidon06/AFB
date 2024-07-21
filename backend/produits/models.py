from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from batiments.models import Batiment

class Race(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='type_poulet_photos/', null=True, blank=True)

    def __str__(self):
        return self.nom

    def clean(self):
        super().clean()
        if not self.nom:
            raise ValidationError({'nom': 'Le nom ne peut pas être vide.'})
        if len(self.description) > 500:
            raise ValidationError({'description': 'La description ne peut pas dépasser 500 caractères.'})

class Lot(models.Model):
    nom = models.CharField(max_length=100)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)
    date_arrivee = models.DateField()
    age_arrivee = models.IntegerField(default=0)
    nombre_arrivee = models.IntegerField(default=0)
    nombre_actuel = models.IntegerField(default=0)
    nombre_deces = models.IntegerField(default=0)
    nombre_malade = models.IntegerField(default=0)
    traitement_imminent = models.IntegerField(default=0)
    total_oeuf = models.IntegerField(default=0)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

    def clean(self):
        super().clean()
        if self.nombre_deces > self.nombre_arrivee:
            raise ValidationError({'nombre_deces': 'Le nombre de décès ne peut pas être supérieur au nombre d\'arrivée.'})
        if self.nombre_malade > self.nombre_arrivee:
            raise ValidationError({'nombre_malade': 'Le nombre de malades ne peut pas être supérieur au nombre d\'arrivée.'})
        if self.date_arrivee > timezone.now().date():
            raise ValidationError({'date_arrivee': 'La date d\'arrivée ne peut pas être une date future.'})

    def save(self, *args, **kwargs):
        if self.pk:  # Vérifie si l'instance existe déjà (mise à jour)
            old_lot = Lot.objects.get(pk=self.pk)
            if old_lot.nombre_deces != self.nombre_deces:
                self.nombre_actuel = old_lot.nombre_actuel - (self.nombre_deces - old_lot.nombre_deces)
                if self.nombre_actuel < 0:
                    self.nombre_actuel = 0
        super().save(*args, **kwargs)

class Aliment(models.Model):
    UNITE_CHOICES = (
        ('kg', 'Kilogrammes'),
        ('g', 'Grammes'),
        ('L', 'Litres'),
        ('ml', 'Millilitres'),
        ('unité', 'Unité'),
    )

    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    unite_mesure = models.CharField(max_length=10, choices=UNITE_CHOICES, default='kg')

    def __str__(self):
        return f"{self.nom} ( {self.unite_mesure})"

    def clean(self):
        super().clean()
        if self.prix_unitaire <= 0:
            raise ValidationError({'prix_unitaire': 'Le prix unitaire doit être supérieur à zéro.'})
        if self.unite_mesure not in dict(self.UNITE_CHOICES):
            raise ValidationError({'unite_mesure': 'L\'unité de mesure est invalide.'})

class Traitement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    duree_jours = models.IntegerField(help_text="Durée normale du traitement en jours")

    def __str__(self):
        return self.nom

    def clean(self):
        super().clean()
        if self.duree_jours <= 0:
            raise ValidationError({'duree_jours': 'La durée du traitement doit être supérieure à zéro.'})
