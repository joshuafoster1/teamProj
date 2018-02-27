# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

metricModels = [FingerPower, FingerEndurance, FingerMuscularEndurance, PullAndSlap,
    MaxWeightPullUp, MaxPullUps, LateralCore, CampusPowerEndurance, MetricDescription]

for model in metricModels:
    admin.site.register(model)
