# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

metricModels = [FingerPower, FingerEndurance, FingerMuscularEndurance, PullAndSlap,
    MaxWeightPullUp, MaxPullUps, LateralCore, CampusPowerEndurance, MetricDescription]

for model in metricModels:
    admin.site.register(model)

@admin.register(MetricDescription)
class MetricDesciptionAdmin(ImportExportModelAdmin):
    pass
