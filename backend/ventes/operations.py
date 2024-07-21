from django.db import models
from clients.models import Client, Fournisseur
from .models import Oeuf, Poule, ChargeCategory
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_vente = models.DateField()
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_dette = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.pk:  # Check if instance already exists
            self.update_montant_total()
        super().save(*args, **kwargs)

    def update_montant_total(self):
        if self.pk:
            self.montant_total = sum(item.prix_total for item in self.items.all()) - self.remise
            if self.montant_total < 0:
                self.montant_total = 0
            self.montant_dette = self.montant_total - self.montant_dette
            if self.montant_dette < 0:
                self.montant_dette = 0
            super().save(update_fields=['montant_total', 'montant_dette'])

    def __str__(self):
        return f"Vente à {self.client.nom} le {self.date_vente}"


class VenteItem(models.Model):
    vente = models.ForeignKey(Vente, related_name='items', on_delete=models.CASCADE)
    produit_poule = models.ForeignKey(Poule, on_delete=models.CASCADE, null=True, blank=True)
    produit_oeuf = models.ForeignKey(Oeuf, on_delete=models.CASCADE, null=True, blank=True)
    quantite = models.IntegerField()
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.produit_poule and not self.produit_oeuf:
            raise ValueError("Either produit_poule or produit_oeuf must be set.")

        if self.produit_poule:
            prix_unitaire = self.produit_poule.prix_unitaire
        else:
            prix_unitaire = self.produit_oeuf.prix_unitaire

        if self.quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        self.prix_total = prix_unitaire * self.quantite
        super().save(*args, **kwargs)

        # Update the associated vente
        self.vente.update_montant_total()

    def __str__(self):
        if self.produit_poule:
            return f"Vente Item: Poule - {self.produit_poule.nom} - Quantité: {self.quantite} - Prix Total: {self.prix_total}"
        elif self.produit_oeuf:
            return f"Vente Item: Œuf - {self.produit_oeuf.nom} - Quantité: {self.quantite} - Prix Total: {self.prix_total}"
        else:
            return "Vente Item: Produit non défini"


class Remboursement(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_remboursement = models.DateField(auto_now_add=True)
    remarque = models.TextField(blank=True)

    def clean(self):
        if self.montant > self.vente.montant_total:
            raise ValidationError(
                "Le montant du remboursement ne peut pas être supérieur au montant total de la vente.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Remboursement de {self.montant} € le {self.date_remboursement} pour vente {self.vente}'


class Charge(models.Model):
    category = models.ForeignKey(ChargeCategory, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_charge = models.DateField(auto_now_add=True)

    @property
    def montant_dette(self):
        return self.montant - self.montant_paye

    def clean(self):
        if self.montant_paye > self.montant:
            raise ValidationError("Le montant payé ne peut pas être supérieur au montant total de la charge.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        fournisseur_str = f" - Fournisseur: {self.fournisseur.nom}" if self.fournisseur else ""
        return f"{self.category} - {self.montant} € le {self.date_charge}{fournisseur_str}"

    class Meta:
        verbose_name_plural = "Charges"

    @staticmethod
    def get_totals():
        charges = Charge.objects.all()
        total_charge = sum(charge.montant for charge in charges)
        total_paid = sum(charge.montant_paye for charge in charges)
        total_debt = sum(charge.montant_dette for charge in charges)
        return total_charge, total_paid, total_debt
