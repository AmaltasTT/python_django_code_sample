# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-01-04 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vipapi', '0006_delete_personalinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fullname', models.CharField(max_length=100)),
                ('petname', models.CharField(max_length=100)),
                ('fathername', models.CharField(max_length=100)),
                ('mothername', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('pincode', models.IntegerField()),
                ('mobilenumber', models.IntegerField()),
                ('alternatenumber', models.IntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('dateofbirth', models.DateField()),
                ('weight', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
        ),
    ]
