# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-01 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vipapi', '0011_describeyourself'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('registeredon', models.DateField(null=True)),
                ('profilepercent', models.CharField(default=b'1%', max_length=100)),
                ('profilecompleted', models.CharField(default=b'No', max_length=50)),
                ('checkedbyadmin', models.CharField(default=b'No', max_length=50)),
                ('checkedondate', models.DateField(null=True)),
                ('applicantid', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'ApplicantStatus',
            },
        ),
    ]
