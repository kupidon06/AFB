from django.db import models
from produits.models import Race

class Poule(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='produit_photos/', null=True, blank=True)

    def __str__(self):
        return f"Poule: {self.race.nom} - {self.race} - {self.prix_unitaire} €"

    class Meta:
        verbose_name_plural = "Produits Poules"


class Oeuf(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='produit_photos/', null=True, blank=True)

    def __str__(self):
        return f"Œuf: {self.nom} - {self.prix_unitaire} €"

    class Meta:
        verbose_name_plural = "Produits Œufs"



class ChargeCategory(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

