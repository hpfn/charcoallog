# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170318_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extract',
            name='money',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Money'),
        ),
    ]