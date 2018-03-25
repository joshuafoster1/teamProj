# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from .models import * #Athlete, Session, Conditioning, RefCategory, RefExercise, PinchBlocks, WeightedHangs, Calendar, Practice, AssignedPractice
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Athlete)
class AthleteTable(ImportExportModelAdmin):
    model = Athlete
    list_display = ('user', 'birthdate', 'get_category', 'guardian2')
    list_filter = ['birthdate']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']

@admin.register(Conditioning)
class ConditioningAdmin(ImportExportModelAdmin):
    model = Conditioning
    list_display = ('session', 'exercise', 'repetitions', 'setNum')
    list_filter = ['session__sessionDate', 'session__athlete', 'exercise']
    search_fields = ['session__athlete__user__first_name', 'session__athlete__user__last_name', 'session__athlete__user__username']

@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    list_display = ('athlete',)
    list_filter = ['athlete']

@admin.register(RefCategory)
class RefCategoryAdmin(ImportExportModelAdmin):
    list_display = ['category']

@admin.register(RefExercise)
class RefExerciseAdmin(ImportExportModelAdmin):
    list_display = ['exercise', 'category', 'goal', 'order']
    list_filter = ['category__category']

@admin.register(Practice)
class PracticeAdmin(ImportExportModelAdmin):
    list_display = ['warmup', 'technique', 'routine_1', 'routine_2', 'conditioning_1',
        'conditioning_2']

@admin.register(AssignedPractice)
class AssignedPracticeAdmin(ImportExportModelAdmin):
    list_display = ['athlete', 'practice', 'comment']

@admin.register(ClimbingQuotes)
class ClimbingQuotesAdmin(ImportExportModelAdmin):
    pass

@admin.register(RefTechniqueDrill)
class RefTechniqueDrillAdmin(ImportExportModelAdmin):
    pass

@admin.register(RefTechnique)
class RefTechniqueAdmin(ImportExportModelAdmin):
    pass

@admin.register(RefFingerTraining)
class RefFingerTrainingAdmin(ImportExportModelAdmin):
    pass

@admin.register(RefConditioning)
class RefConditioningAdmin(ImportExportModelAdmin):
    pass

# admin.site.register(Athlete, AthleteTable)
# admin.site.register(Session, SessionAdmin)
# admin.site.register(Conditioning, ConditioningAdmin)
# admin.site.register(RefCategory)
# admin.site.register(RefExercise)
admin.site.register(PinchBlocks)
admin.site.register(WeightedHangs)
admin.site.register(Calendar)
# admin.site.register(Practice)
# admin.site.register(AssignedPractice)
# admin.site.register(RefConditioning)
# admin.site.register(RefTechnique)
# admin.site.register(RefTechniqueDrill)
admin.site.register(RefWarmup)
# admin.site.register(RefFingerTraining)
admin.site.register(RefRoutine)
admin.site.register(MaxConditioning)
