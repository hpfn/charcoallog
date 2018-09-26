from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import (
    BasicData, Investment, InvestmentDetails
)

# for two 'def' about Extract - bank app
# populate_investments
# delete_transfer_from_bank
kind = '---'
# which_target = '---'


@receiver(post_save, sender=Extract)
def populate_investments(sender, created, instance, **kwargs):
    # falta o update_fields
    if created and instance.category == 'investments':
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            kind=kind,
            # which_target=which_target,
        )
        b_data = BasicData.objects.create(**data)

        data = dict(
            tx_op=00.00,
            brokerage=instance.description,
            basic_data=b_data
        )

        Investment.objects.create(**data)


@receiver(post_delete, sender=Extract)
def delete_transfer_from_bank(sender, instance, using, **kwargs):
    if instance.category == 'investments':
        user_name = instance.user_name
        date = instance.date
        money = instance.money
        brokerage = instance.description

        qs = Investment.objects.user_logged(user_name).filter(
            brokerage=brokerage,
            basic_data__date=date,
            basic_data__money=money * -1,
            basic_data__kind=kind,
            # basic_data__which_target=which_target
        )

        if qs.exists():
            # make sure to delete one record
            qs.first().delete()


# two 'def' about Investment
# populate investments details
# delete_transfer_from_investment
which_target = '---'
segment = '---'
tx_or_price = 00.00
quant = 00.00


@receiver(post_save, sender=Investment)
def populate_investments_details(sender, created, instance, **kwargs):
    # update_fields ?
    if created and instance.basic_data.kind != '---':
        b_data = dict(
            user_name=instance.basic_data.user_name,
            date=instance.basic_data.date,
            money=instance.basic_data.money * -1,
            kind=instance.basic_data.kind,
            # which_target=instance.basic_data.which_target
        )
        basic_data = BasicData.objects.create(**b_data)

        data = dict(
            which_target=which_target,
            segment=segment,
            tx_or_price=tx_or_price,
            quant=quant,
            basic_data=basic_data
        )
        InvestmentDetails.objects.create(**data)


@receiver(post_delete, sender=Investment)
def delete_transfer_from_investment(sender, instance, using, **kwargs):
    data = dict(
        basic_data__user_name=instance.basic_data.user_name,
        basic_data__date=instance.basic_data.date,
        basic_data__money=instance.basic_data.money * -1,
        basic_data__kind=instance.basic_data.kind,
        # which_target=which_target,
        # segment=segment,
        # tx_or_price=tx_or_price,
        # quant=quant
    )
    qs = InvestmentDetails.objects.filter(**data)
    if qs.exists():
        # make sure to delete one record
        qs.first().delete()
