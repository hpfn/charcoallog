from django.db.models.signals import post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import Investment


@receiver(post_save, sender=Extract)
def populate_investments(sender, created, instance, **kwargs):
    # falta o update_fields
    if created and instance.category == 'investments':
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money,
            kind='---',
            which_target='----',
            tx_op=00.00,
            brokerage=instance.description
        )
        Investment.objects.create(**data)
