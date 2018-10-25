from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from charcoallog.bank.models import Extract
from charcoallog.investments.models import NewInvestment


@receiver(post_save, sender=NewInvestment)
def populate_bank(sender, created, instance, **kwargs):
    # update_fields ?
    if created and 'transfer to' in instance.kind:
        invest, bank = instance.kind.split('transfer to')
        data = dict(
            user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            description='credit from ' + invest.strip(),
            category='---',
            payment=bank.strip(),
        )
        Extract.objects.create(**data)


@receiver(post_delete, sender=NewInvestment)
def delete_bank(sender, instance, using, **kwargs):
    # update_fields ?
    if 'transfer to' in instance.kind:
        invest, bank = instance.kind.split('transfer to')
        data = dict(
            # user_name=instance.user_name,
            date=instance.date,
            money=instance.money * -1,
            description='credit from ' + invest.strip(),
            category='---',
            payment=bank.strip(),
        )

        qs_to_del = Extract.objects.user_logged(instance.user_name).filter(**data)

        if qs_to_del.exists():
            # make sure to delete one record
            qs_to_del.first().delete()
