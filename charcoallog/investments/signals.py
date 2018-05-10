from django.db.models.signals import post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import Investment, InvestmentDetails


@receiver(post_save, sender=Extract)
def populate_investments(sender, created, instance, **kwargs):
    # falta o update_fields
    if created and instance.category == 'investments':
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            kind='---',
            which_target='----',
            tx_op=00.00,
            brokerage=instance.description
        )
        Investment.objects.create(**data)


@receiver(post_save, sender=Investment)
def populate_investments_details(sender, created, instance, **kwargs):
    # update_fields ?
    if created and instance.kind != '---':
        data = {
            'user_name': instance.user_name,
            'date': instance.date,
            'money': instance.money * -1,
            'kind': instance.kind,
            'which_target': instance.which_target,
            'segment': '---',
            'tx_or_price': 00.00,
            'quant': 00.00
        }
        InvestmentDetails.objects.create(**data)
