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
    list_filter = ['routine_type', 'intensity__intensity']

@admin.register(RoutineType)
class RoutineTypeAdmin(ImportExportModelAdmin):
    list_display = ['name']

@admin.register(AssignedPractice)
class AssignedPracticeAdmin(ImportExportModelAdmin):
    pass

@admin.register(RefIntensity)
class RefIntensityAdmin(ImportExportModelAdmin):
    pass

@admin.register(GradeLevel)
class GradeLevelAdmin(ImportExportModelAdmin):
    pass

@admin.register(Metrics)
class MetricsAdmin(ImportExportModelAdmin):
    pass

@admin.register(HangboardMetrics)
class HangboardMetricsAdmin(ImportExportModelAdmin):
    pass

@admin.register(RouteProjectMetrics)
class RouteProjectMetricsAdmin(ImportExportModelAdmin):
    pass

@admin.register(BoulderProjectMetrics)
class BoulderProjectMetricsAdmin(ImportExportModelAdmin):
    pass

@admin.register(Top3BoulderSends)
class Top3BoulderSendsAdmin(ImportExportModelAdmin):
    pass

@admin.register(Top3RopeSends)
class Top3RopeSendsAdmin(ImportExportModelAdmin):
    pass

@admin.register(BoulderRedpoint)
class BoulderRedpointAdmin(ImportExportModelAdmin):
    pass

@admin.register(RouteRedpoint)
class RouteRedpointAdmin(ImportExportModelAdmin):
    pass
