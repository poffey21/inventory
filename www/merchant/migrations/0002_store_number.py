# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
