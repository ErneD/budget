# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-17 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depenses', '0008_auto_20161217_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametre',
            name='parametre_montant',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_montant',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
