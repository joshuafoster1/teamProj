# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-26 18:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedPractice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('guardian1', models.CharField(blank=True, max_length=50)),
                ('guardian1_email', models.EmailField(blank=True, max_length=75)),
                ('guardian2', models.CharField(blank=True, max_length=50)),
                ('guardian2_email', models.EmailField(blank=True, max_length=75)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateField()),
                ('event_date', models.DateField()),
                ('event_title', models.CharField(max_length=100)),
                ('event_description', models.CharField(blank=True, max_length=300)),
                ('event_location', models.CharField(blank=True, max_length=200)),
                ('event_format', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ClimbingQuotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30)),
                ('quote', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Conditioning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repetitions', models.IntegerField()),
                ('setNum', models.IntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='MaxConditioning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repetitions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PinchBlocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('seconds', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RefCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('category', models.CharField(max_length=40)),
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
            name='RefExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=40)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('order', models.IntegerField()),
                ('goal', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='training.RefCategory')),
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
                ('secondary_technique', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technique_drill2', to='training.RefTechnique')),
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
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionDate', models.DateField(auto_now=True)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='training.Athlete')),
            ],
        ),
        migrations.CreateModel(
            name='Top3Sends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.IntegerField(choices=[(0, 'V0'), (1, 'V1'), (2, 'V2'), (3, 'V3'), (4, 'V4'), (5, 'V5'), (6, 'V6'), (7, 'V7'), (8, 'V8'), (9, 'V9'), (10, 'V10'), (11, 'V11')])),
                ('second', models.IntegerField(choices=[(0, 'V0'), (1, 'V1'), (2, 'V2'), (3, 'V3'), (4, 'V4'), (5, 'V5'), (6, 'V6'), (7, 'V7'), (8, 'V8'), (9, 'V9'), (10, 'V10'), (11, 'V11')])),
                ('third', models.IntegerField(choices=[(0, 'V0'), (1, 'V1'), (2, 'V2'), (3, 'V3'), (4, 'V4'), (5, 'V5'), (6, 'V6'), (7, 'V7'), (8, 'V8'), (9, 'V9'), (10, 'V10'), (11, 'V11')])),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='top_3_sends', to='training.Session')),
            ],
        ),
        migrations.CreateModel(
            name='WeightedHangs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('seconds', models.IntegerField()),
                ('hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weighted_hangs', to='training.RefExercise')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weighted_hangs', to='training.Session')),
            ],
        ),
        migrations.AddField(
            model_name='practice',
            name='conditioning_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice5', to='training.RefConditioning'),
        ),
        migrations.AddField(
            model_name='practice',
            name='conditioning_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice6', to='training.RefConditioning'),
        ),
        migrations.AddField(
            model_name='practice',
            name='finger_training',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice7', to='training.RefFingerTraining'),
        ),
        migrations.AddField(
            model_name='practice',
            name='routine_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice3', to='training.RefRoutine'),
        ),
        migrations.AddField(
            model_name='practice',
            name='routine_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='practice4', to='training.RefRoutine'),
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
            model_name='pinchblocks',
            name='pinch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinch_blocks', to='training.RefExercise'),
        ),
        migrations.AddField(
            model_name='pinchblocks',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pinch_blocks', to='training.Session'),
        ),
        migrations.AddField(
            model_name='maxconditioning',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='max_conditioning_sets', to='training.RefExercise'),
        ),
        migrations.AddField(
            model_name='maxconditioning',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='max_conditioning_sets', to='training.Session'),
        ),
        migrations.AddField(
            model_name='conditioning',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditioning_sets', to='training.RefExercise'),
        ),
        migrations.AddField(
            model_name='conditioning',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditioning_sets', to='training.Session'),
        ),
        migrations.AddField(
            model_name='assignedpractice',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_practice', to='training.Athlete'),
        ),
        migrations.AddField(
            model_name='assignedpractice',
            name='practice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_practice', to='training.Practice'),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('athlete', 'sessionDate')]),
        ),
        migrations.AlterUniqueTogether(
            name='maxconditioning',
            unique_together=set([('session', 'exercise')]),
        ),
        migrations.AlterUniqueTogether(
            name='conditioning',
            unique_together=set([('session', 'exercise', 'setNum')]),
        ),
    ]
