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

class Timer(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_timer(self):
        intervals = Interval.objects.values('activity', 'time').filter(timer=self).order_by('order')
        json_intervals = json.dumps(list(intervals), cls=DjangoJSONEncoder)
        print(json_intervals)
        return json_intervals

class Interval(models.Model):
    activity = models.CharField(max_length=30)
    time = models.IntegerField()
    order = models.IntegerField()
    timer = models.ForeignKey(Timer, related_name='intervals')

    def __str__(self):
        return self.activity
