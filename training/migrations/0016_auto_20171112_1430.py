# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-12 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0015_auto_20171112_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='routine_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice3', to='training.RefRoutine'),
        ),
        migrations.AlterField(
            model_name='practice',
            name='routine_2',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice4', to='training.RefRoutine'),
        ),
    ]
