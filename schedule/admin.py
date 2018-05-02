# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.
@admin.register(Form)
class FormAdmin(ImportExportModelAdmin):
    list_display = ['name', 'instance']

@admin.register(BoulderingRoutineMetrics)
class BoulderingRoutineMetricsAdmin(ImportExportModelAdmin):
    pass

@admin.register(RopeRoutineMetrics)
class RopeRoutineMetricsAdmin(ImportExportModelAdmin):
    pass

@admin.register(PracticeSection)
class PracticeSectionAdmin(ImportExportModelAdmin):
    pass

@admin.register(Protocol)
class ProtocolAdmin(ImportExportModelAdmin):
    list_display = ['routine_type', 'name', 'goal']
    list_filter = ['routine_type', 'intensity__metabolic_focus']

@admin.register(RoutineType)
class RoutineTypeAdmin(ImportExportModelAdmin):
    list_display = ['name']

@admin.register(AssignedPractice)
class AssignedPracticeAdmin(ImportExportModelAdmin):
    pass

@admin.register(RefIntensity)
class RefIntensityAdmin(ImportExportModelAdmin):
    pass
