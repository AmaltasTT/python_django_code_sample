# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-17 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vipapi', '0015_vipwinner_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipwinner',
            name='slogan',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
