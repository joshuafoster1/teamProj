# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-03 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hangboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_intervals', models.CharField(blank=True, max_length=250)),
                ('activity_intervals', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=30)),
                ('time', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='interval',
            name='timer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='timers.Timer'),
        ),
    ]
