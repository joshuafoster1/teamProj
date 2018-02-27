# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from training.models import Session, Athlete
from django.db import models

# Create your models here.
# class MetricTestInformation(model.Models):
#     test = models.CharField
class MetricTest(models.Model):
    session = models.ForeignKey(Session, related_name='metric_tests')

class FingerPower(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_power_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

class FingerMuscularEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_muscular_endurance_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

class FingerEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_endurance_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

class PullAndSlap(models.Model):
    test = models.ForeignKey(MetricTest, related_name='pull_and_slaps')
    height_right_hand = models.IntegerField()
    height_left_hand = models.IntegerField()

class MaxWeightPullUp(models.Model):
    test = models.ForeignKey(MetricTest, related_name='max_weight_pull_ups')
    weight = models.IntegerField()
    lateral = models.BooleanField()

class MaxPullUps(models.Model):
    test = models.ForeignKey(MetricTest, related_name='max_pull_ups')
    repetitions = models.IntegerField()
    lateral = models.BooleanField()

class CampusPowerEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='campus_power_endurance')
    moves = models.IntegerField()
    time = models.IntegerField()

class LateralCore(models.Model):
    test = models.ForeignKey(MetricTest, related_name='lateral_core')
    distance_left_side = models.IntegerField()
    distance_right_side = models.IntegerField()

class MetricDescription(models.Model):
    metric = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
