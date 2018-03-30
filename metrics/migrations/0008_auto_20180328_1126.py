# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-28 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0007_auto_20180327_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fingerendurance',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='fingermuscularendurance',
            name='weight',
        ),
        migrations.AddField(
            model_name='fingerendurance',
            name='feet_on',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fingerendurance',
            name='rung',
            field=models.IntegerField(choices=[(1, 'Small'), (2, 'Medium'), (3, 'Large')], default=1),
            preserve_default=False,
        ),
    ]
