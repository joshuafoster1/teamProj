# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-21 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
