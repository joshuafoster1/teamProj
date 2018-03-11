# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from training.models import Session, Athlete
from django.db import models

# Create your models here.
# class MetricTestInformation(model.Models):
#     test = models.CharField

RUNG = (
    (1, "Small"),
    (2, "Medium"),
    (3, "Large"),
)

class MetricTest(models.Model):
    session = models.ForeignKey(Session, related_name='metric_tests')

    def __str__(self):
        return self.session

class FingerPower(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_power_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

    def __str__(self):
        return str(self.weight) + " " + str(self.time)


class FingerMuscularEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_muscular_endurance_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

    def __str__(self):
        return str(self.weight) + " " + str(self.time)


class FingerEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_endurance_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

    def __str__(self):
        return str(self.weight) + " " + str(self.time)


class PullAndSlap(models.Model):
    test = models.ForeignKey(MetricTest, related_name='pull_and_slaps')
    height_right_hand = models.IntegerField()
    height_left_hand = models.IntegerField()

    def __str__(self):
        return str(self.height_left_hand) + " " + str(self.height_right_hand)


class MaxWeightPullUp(models.Model):
    test = models.ForeignKey(MetricTest, related_name='max_weight_pull_ups')
    weight = models.IntegerField()
    lateral = models.BooleanField()

    def __str__(self):
        return str(self.weight) + " " + str(self.lateral)


class MaxPullUps(models.Model):
    test = models.ForeignKey(MetricTest, related_name='max_pull_ups')
    repetitions = models.IntegerField()
    lateral = models.BooleanField()

    def __str__(self):
        return str(self.repetitions) + " " + str(self.lateral)


class CampusPowerEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='campus_power_endurance')
    moves = models.IntegerField()
    time = models.IntegerField()
    rung = models.IntegerField(choices=RUNG)
    feet_on = models.BooleanField()

    def __str__(self):
        return str(self.moves) + " " + str(self.time)


class LateralCore(models.Model):
    test = models.ForeignKey(MetricTest, related_name='lateral_core')
    distance_left_side = models.IntegerField()
    distance_right_side = models.IntegerField()

    def __str__(self):
        return str(self.distance_left_side) + " " + str(self.distance_right_side)


class MetricDescription(models.Model):
    metric = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.metric


'''
class Metric(models.Model):
    metric = models.CharField(max_length=20)
    descrition = models.CharField(max_length=500)

class Parameter(models.Model):
    parameter =

class TestParameter(models.Model):
    parameter

class Test(models.Model):
    metric = models.ForeignKey(Metric)
    parameter = models.ManyToManyField(Parameter, through='TestParameter') #for each, we want draw and ac_dc


'''
