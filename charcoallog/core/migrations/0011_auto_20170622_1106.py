# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-22 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170622_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extract',
            name='payment',
            field=models.CharField(max_length=70, verbose_name='Payment'),
        ),
    ]
