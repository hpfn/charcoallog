# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-01 17:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('investments', '0017_abs_to_mti'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newinvestment',
            options={'ordering': ['-date'], 'verbose_name': 'investments',
                     'verbose_name_plural': 'investments'},
        ),
        migrations.AlterModelOptions(
            name='newinvestmentdetails',
            options={'verbose_name': 'investment details',
                     'verbose_name_plural': 'investment details'},
        ),
    ]