# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-06 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Date')),
                ('money', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Money')),
                ('description', models.CharField(max_length=70, verbose_name='Description')),
                ('category', models.CharField(max_length=70, verbose_name='Category')),
                ('payment', models.CharField(max_length=70, verbose_name='Payment')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
