# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-27 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0008_auto_20180927_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewInvestment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa

                ('user_name', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('money', models.DecimalField(decimal_places=2, max_digits=8)),
                ('kind', models.CharField(max_length=20)),
                ('tx_op', models.DecimalField(decimal_places=2, max_digits=4)),
                ('brokerage', models.CharField(max_length=15)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewInvestmentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa
                ('user_name', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('money', models.DecimalField(decimal_places=2, max_digits=8)),
                ('kind', models.CharField(max_length=20)),
                ('which_target', models.CharField(default='---', max_length=20)),
                ('segment', models.CharField(max_length=20)),
                ('tx_or_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quant', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
            },
        ),
    ]