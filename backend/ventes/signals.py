from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .operations import Vente, VenteItem, Remboursement, Charge

@receiver(post_save, sender=VenteItem)
def update_vente_on_venteitem_save(sender, instance, **kwargs):
    """Update the related `Vente` total and debt when a `VenteItem` is saved."""
    if instance.vente:
        instance.vente.update_montant_total()

@receiver(post_delete, sender=VenteItem)
def update_vente_on_venteitem_delete(sender, instance, **kwargs):
    """Update the related `Vente` total and debt when a `VenteItem` is deleted."""
    if instance.vente:
        instance.vente.update_montant_total()

@receiver(post_save, sender=Remboursement)
def validate_remboursement(sender, instance, **kwargs):
    """Validate `Remboursement` and log if needed."""
    instance.clean()  # Ensure validation is called

@receiver(post_save, sender=Charge)
def validate_charge(sender, instance, **kwargs):
    """Validate `Charge` and log if needed."""
    instance.clean()  # Ensure validation is called
