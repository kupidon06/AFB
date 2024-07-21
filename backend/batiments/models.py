from django.db import models

class Batiment(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    capacite = models.IntegerField()
    photo = models.ImageField(upload_to='batiment_photos/', null=True, blank=True)

    def __str__(self):
        return self.nom
