# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from .models import * #Athlete, Session, Conditioning, RefCategory, RefExercise, PinchBlocks, WeightedHangs, Calendar, Practice, AssignedPractice
# Register your models here.

class AthleteTable(admin.ModelAdmin):
    model = Athlete
    list_display = ('user', 'birthdate', 'get_category', 'guardian2')
    list_filter = ['birthdate']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']

class ConditioningAdmin(admin.ModelAdmin):
    model = Conditioning
    list_display = ('session', 'exercise', 'repetitions', 'setNum')
    list_filter = ['session__sessionDate', 'session__athlete', 'exercise']
    search_fields = ['session__athlete__user__first_name', 'session__athlete__user__last_name', 'session__athlete__user__username']


class SessionAdmin(admin.ModelAdmin):
    list_display = ('athlete',)
    list_filter = ['athlete']


admin.site.register(Athlete, AthleteTable)
admin.site.register(Session, SessionAdmin)
admin.site.register(Conditioning, ConditioningAdmin)
admin.site.register(RefCategory)
admin.site.register(RefExercise)
admin.site.register(PinchBlocks)
admin.site.register(WeightedHangs)
admin.site.register(Calendar)
admin.site.register(Practice)
admin.site.register(AssignedPractice)
admin.site.register(RefConditioning)
admin.site.register(RefTechnique)
admin.site.register(RefTechniqueDrill)
admin.site.register(RefWarmup)
admin.site.register(RefFingerTraining)
admin.site.register(RefRoutine)
