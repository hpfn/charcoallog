# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-27 17:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0010_data_from_oto_to_abs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oldinvestment',
            name='basic_data',
        ),
        migrations.RemoveField(
            model_name='oldinvestmentdetails',
            name='basic_data',
        ),
        migrations.DeleteModel(
            name='BasicData',
        ),
        migrations.DeleteModel(
            name='OldInvestment',
        ),
        migrations.DeleteModel(
            name='OldInvestmentDetails',
        ),
    ]
