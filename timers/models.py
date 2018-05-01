# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json
# Create your models here.
class Hangboard(models.Model):
    time_intervals = models.CharField(max_length=250, blank=True)
    activity_intervals = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Timer(models.Model):
    CHOICES = (
        ("climb routine", "climb routine"),
        ("hangboard", "hangboard"),
        ("conditioning", "conditioning"),
        ("climb routine*2", "climb routine*2"),
        ("hangboard*2", "hangboard*2"),
        ("conditioning*2", "conditioning*2"),

    )
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)
    workout = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return self.name

    def get_timer(self):
        intervals = Interval.objects.values('activity', 'time').filter(timer=self).order_by('order')
        json_intervals = json.dumps(list(intervals), cls=DjangoJSONEncoder)
        return json_intervals

class Interval(models.Model):
    activity = models.CharField(max_length=30)
    time = models.IntegerField()
    order = models.IntegerField()
    timer = models.ForeignKey(Timer, related_name='intervals')

    def __str__(self):
        return self.activity
