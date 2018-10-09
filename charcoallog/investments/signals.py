from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import NewInvestment


@receiver(post_save, sender=Extract)
def populate_investments(sender, created, instance, **kwargs):
    # falta o update_fields
    if created and instance.category == 'investments':
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            # kind=kind,  # has default value
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
            # kind=kind,  # has default value
        )

        if qs.exists():
            # make sure to delete one record
            qs.first().delete()

# @receiver(post_save, sender=OldNewInvestment)
# def populate_investments_details(sender, created, instance, **kwargs):
#     # update_fields ?
#     if created and instance.kind != '---':
#         kind = instance.kind.partition('transfer to')
#         if kind[1] != 'transfer to':
#             instance.money = instance.money * -1
#
#         data = dict(
#             user_name=instance.user_name,
#             date=instance.date,
#             money=instance.money,
#             kind=kind[0].strip(),
#             tx_op=instance.tx_op,
#             brokerage=instance.brokerage
#             # which_target=which_target,  # has default value
#             # segment=segment,  # has default value
#             # tx_or_price=tx_or_price,  # has default value
#             # quant=quant,  # has default value
#         )
#         OldNewInvestmentDetails.objects.create(**data)
#
#
# @receiver(post_delete, sender=OldNewInvestment)
# def delete_transfer_from_investment_to_detail(sender, instance, using, **kwargs):
#     kind = instance.kind.partition('transfer to')
#     if kind[1] != 'transfer to':
#         instance.money = instance.money * -1
#
#     data = dict(
#         user_name=instance.user_name,
#         date=instance.date,
#         money=instance.money,
#         kind=kind[0].strip(),
#     )
#     qs = OldNewInvestmentDetails.objects.filter(**data)
#     if qs.exists():
#         # make sure to delete one record
#         qs.first().delete()
#
