from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Lot, Traitement, Aliment
from clients.models import Fournisseur

class JournalisationQuotidienne(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    date_journalisation = models.DateField()
    nombre_vivants = models.IntegerField(default=0)
    nombre_deces = models.IntegerField(default=0)
    nombre_malades = models.IntegerField(default=0)
    autres_informations = models.TextField(blank=True)

    def __str__(self):
        return f"Journalisation quotidienne de {self.lot.nom} le {self.date_journalisation}"

    def clean(self):
        super().clean()
        if self.nombre_deces > self.nombre_vivants:
            raise ValidationError({'nombre_deces': 'Le nombre de décès ne peut pas être supérieur au nombre de vivants.'})
        if self.nombre_malades > self.nombre_vivants:
            raise ValidationError({'nombre_malades': 'Le nombre de malades ne peut pas être supérieur au nombre de vivants.'})
        if self.date_journalisation > timezone.now().date():
            raise ValidationError({'date_journalisation': 'La date de journalisation ne peut pas être une date future.'})

class Alimentation(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    date_alimentation = models.DateField()
    quantite = models.FloatField()
    type_aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"Alimentation de {self.lot.nom} le {self.date_alimentation}"

    def clean(self):
        super().clean()
        if self.quantite <= 0:
            raise ValidationError({'quantite': 'La quantité doit être supérieure à zéro.'})
        if self.date_alimentation > timezone.now().date():
            raise ValidationError({'date_alimentation': 'La date d\'alimentation ne peut pas être une date future.'})

class RamassageOeufs(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    date_ramassage = models.DateField()
    quantite_premier_ramassage = models.IntegerField(default=0)
    quantite_deuxieme_ramassage = models.IntegerField(default=0)
    quantite_troisieme_ramassage = models.IntegerField(default=0)
    quantite_quatrieme_ramassage = models.IntegerField(default=0)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"Ramassage d'œufs de {self.lot.nom} le {self.date_ramassage}"

    def clean(self):
        super().clean()
        if self.date_ramassage > timezone.now().date():
            raise ValidationError({'date_ramassage': 'La date de ramassage ne peut pas être une date future.'})
        if (self.quantite_premier_ramassage < 0 or
            self.quantite_deuxieme_ramassage < 0 or
            self.quantite_troisieme_ramassage < 0 or
            self.quantite_quatrieme_ramassage < 0):
            raise ValidationError({'quantites': 'Les quantités doivent être positives.'})

    def total_ramasse(self):
        return (self.quantite_premier_ramassage +
                self.quantite_deuxieme_ramassage +
                self.quantite_troisieme_ramassage +
                self.quantite_quatrieme_ramassage)

class HistoriqueTraitement(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    traitement = models.ForeignKey(Traitement, on_delete=models.CASCADE)
    date_traitement = models.DateField()
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"{self.traitement.nom} pour {self.lot.nom} le {self.date_traitement}"

    def clean(self):
        super().clean()
        if self.date_traitement > timezone.now().date():
            raise ValidationError({'date_traitement': 'La date de traitement ne peut pas être une date future.'})

class Provision(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    quantite = models.FloatField()
    date_provision = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Provision de {self.quantite} {self.aliment.unite_mesure} de {self.aliment.nom} le {self.date_provision}"

    def clean(self):
        super().clean()
        if self.quantite <= 0:
            raise ValidationError({'quantite': 'La quantité doit être supérieure à zéro.'})
        if self.date_provision > timezone.now().date():
            raise ValidationError({'date_provision': 'La date de provision ne peut pas être une date future.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Assure que la validation est effectuée avant la sauvegarde
        self.aliment.save()
        super().save(*args, **kwargs)
