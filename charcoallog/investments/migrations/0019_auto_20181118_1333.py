# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-18 13:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0018_auto_20181101_1752'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OldNewInvestment',
        ),
        migrations.DeleteModel(
            name='OldNewInvestmentDetails',
        ),
    ]