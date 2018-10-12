from __future__ import unicode_literals

from django.db import migrations


def copy_src_to_dst(source, destination):
    for src in source.objects.all():
        dst = destination(
            user_name=src.basic_data.user_name,
            date=src.basic_data.date,
            money=src.basic_data.money,
            kind=src.basic_data.kind,
            tx_op=src.tx_op,
            brokerage=src.brokerage
        )

        dst.save()


def forward_oldinvest_to_newinvest(apps, schema_editor):
    copy_src_to_dst(
        apps.get_model('investments', 'OldInvestment'),
        apps.get_model('investments', 'NewInvestment')
    )


def copy_dsrc_to_ddst(source, destination):
    for src in source.objects.all():
        dst = destination(
            user_name=src.basic_data.user_name,
            date=src.basic_data.date,
            money=src.basic_data.money,
            kind=src.basic_data.kind,
            which_target=src.which_target,
            segment=src.segment,
            tx_or_price=src.tx_or_price,
            quant=src.quant
        )

        dst.save()


def forward_oldinvestd_to_newinvestd(apps, schema_editor):
    copy_dsrc_to_ddst(
        apps.get_model('investments', 'OldInvestmentDetails'),
        apps.get_model('investments', 'NewInvestmentDetails')
    )


class Migration(migrations.Migration):
    dependencies = [
        ('investments', '0009_newinvestment_newinvestmentdetails'),
    ]

    operations = [
        migrations.RunPython(forward_oldinvest_to_newinvest, ),
        migrations.RunPython(forward_oldinvestd_to_newinvestd, )
    ]
