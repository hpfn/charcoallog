from django.db.models.signals import post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import (
    BasicData, Investment, InvestmentDetails
)


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
        )
        b_data = BasicData.objects.create(**data)

        data = dict(
            tx_op=00.00,
            brokerage=instance.description,
            basic_data=b_data
        )

        Investment.objects.create(**data)


@receiver(post_save, sender=Investment)
def populate_investments_details(sender, created, instance, **kwargs):
    # update_fields ?
    if created and instance.basic_data.kind != '---':
        b_data = {
            'user_name': instance.basic_data.user_name,
            'date': instance.basic_data.date,
            'money': instance.basic_data.money * -1,
            'kind': instance.basic_data.kind,
            'which_target': instance.basic_data.which_target,
            # 'segment': '---',
            # 'tx_or_price': 00.00,
            # 'quant': 00.00
        }
        basic_data = BasicData.objects.create(**b_data)

        data = {
            'segment': '---',
            'tx_or_price': 00.00,
            'quant': 00.00,
            'basic_data': basic_data
        }
        InvestmentDetails.objects.create(**data)
