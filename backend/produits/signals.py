from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Lot
from .rapport import JournalisationQuotidienne,RamassageOeufs
from django.db import transaction
import logging
from django.db.models import Sum

logger = logging.getLogger(__name__)



@receiver(post_save, sender=RamassageOeufs)
@receiver(post_delete, sender=RamassageOeufs)
def update_total_oeuf(sender, instance, **kwargs):
    lot = instance.lot
    total_oeuf = RamassageOeufs.objects.filter(lot=lot).aggregate(
        total=Sum(
            'quantite_premier_ramassage') +
            Sum('quantite_deuxieme_ramassage') +
            Sum('quantite_troisieme_ramassage') +
            Sum('quantite_quatrieme_ramassage')
    )['total'] or 0
    lot.total_oeuf = total_oeuf
    lot.save()

@receiver(post_save, sender=JournalisationQuotidienne)
def update_lot_after_journalisation_save(sender, instance, **kwargs):
    """Update the `nombre_actuel` in Lot based on the number of deaths recorded in JournalisationQuotidienne."""
    with transaction.atomic():
        lot = instance.lot
        initial_nombre_actuel = lot.nombre_actuel
        print(f"Initial nombre_actuel before save: {initial_nombre_actuel}")
        if instance.nombre_deces > 0:
            lot.nombre_actuel -= instance.nombre_deces
            if lot.nombre_actuel < 0:
                lot.nombre_actuel = 0
            lot.save()
            updated_nombre_actuel = lot.nombre_actuel
            print(f"Updated nombre_actuel after save: {updated_nombre_actuel}")
            logger.info(f"Updated lot {lot.nom} after saving journalisation: nombre_actuel = {updated_nombre_actuel}")

@receiver(post_delete, sender=JournalisationQuotidienne)
def update_lot_after_journalisation_delete(sender, instance, **kwargs):
    """Update the `nombre_actuel` in Lot when a JournalisationQuotidienne instance is deleted."""
    with transaction.atomic():
        lot = instance.lot
        initial_nombre_actuel = lot.nombre_actuel
        print(f"Initial nombre_actuel before delete: {initial_nombre_actuel}")
        if instance.nombre_deces > 0:
            lot.nombre_actuel += instance.nombre_deces
            lot.save()
            updated_nombre_actuel = lot.nombre_actuel
            print(f"Updated nombre_actuel after delete: {updated_nombre_actuel}")
            logger.info(f"Updated lot {lot.nom} after deleting journalisation: nombre_actuel = {updated_nombre_actuel}")