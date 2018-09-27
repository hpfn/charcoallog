from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import NewInvestment, NewInvestmentDetails

# for two 'def' about Extract - bank app
# populate_investments
# delete_transfer_from_bank
kind = '---'


@receiver(post_save, sender=Extract)
def populate_investments(sender, created, instance, **kwargs):
    # falta o update_fields
    if created and instance.category == 'investments':
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            kind=kind,
            tx_op=00.00,
            brokerage=instance.description,
        )

        NewInvestment.objects.create(**data)


@receiver(post_delete, sender=Extract)
def delete_transfer_from_bank(sender, instance, using, **kwargs):
    if instance.category == 'investments':
        user_name = instance.user_name
        date = instance.date
        money = instance.money
        brokerage = instance.description

        qs = NewInvestment.objects.user_logged(user_name).filter(
            brokerage=brokerage,
            date=date,
            money=money * -1,
            kind=kind,
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


@receiver(post_save, sender=NewInvestment)
def populate_investments_details(sender, created, instance, **kwargs):
    # update_fields ?
    if created and instance.kind != '---':
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            kind=instance.kind,
            which_target=which_target,
            segment=segment,
            tx_or_price=tx_or_price,
            quant=quant,
        )
        NewInvestmentDetails.objects.create(**data)


@receiver(post_delete, sender=NewInvestment)
def delete_transfer_from_investment(sender, instance, using, **kwargs):
    data = dict(
        user_name=instance.user_name,
        date=instance.date,
        money=instance.money * -1,
        kind=instance.kind,
    )
    qs = NewInvestmentDetails.objects.filter(**data)
    if qs.exists():
        # make sure to delete one record
        qs.first().delete()
