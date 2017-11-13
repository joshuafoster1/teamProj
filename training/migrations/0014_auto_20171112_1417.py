# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-12 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_auto_20171106_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedPractice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_practice', to='training.Athlete')),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RefConditioning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conditioning', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RefFingerTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finger_training', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RefRoutine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routine', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RefTechnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technique', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RefTechniqueDrill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drill', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150)),
                ('primary_technique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technique_drill1', to='training.RefTechnique')),
                ('secondary_technique', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='technique_drill2', to='training.RefTechnique')),
            ],
        ),
        migrations.CreateModel(
            name='RefWarmup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warmup', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='refexercise',
            name='goal',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='refexercise',
            name='order',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        # migrations.AlterUniqueTogether(
        #     name='refexercise',
        #     unique_together=set([('category', 'order')]),
        # ),
        migrations.AddField(
            model_name='practice',
            name='Conditioning_2',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice6', to='training.RefConditioning'),
        ),
        migrations.AddField(
            model_name='practice',
            name='conditioning_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice5', to='training.RefConditioning'),
        ),
        migrations.AddField(
            model_name='practice',
            name='finger_training',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice7', to='training.RefFingerTraining'),
        ),
        migrations.AddField(
            model_name='practice',
            name='routine_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice3', to='training.RefWarmup'),
        ),
        migrations.AddField(
            model_name='practice',
            name='routine_2',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice4', to='training.RefWarmup'),
        ),
        migrations.AddField(
            model_name='practice',
            name='technique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice2', to='training.RefTechniqueDrill'),
        ),
        migrations.AddField(
            model_name='practice',
            name='warmup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice1', to='training.RefWarmup'),
        ),
        migrations.AddField(
            model_name='assignedpractice',
            name='practice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_practice', to='training.Practice'),
        ),
    ]
