# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
# Create your models here.
class Hangboard(models.Model):
    time_intervals = models.CharField(max_length=250, blank=True)
    activity_intervals = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
