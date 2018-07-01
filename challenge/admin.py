# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name']

@admin.register(Challenge)
class ChallengeAdmin(ImportExportModelAdmin):
    list_display = ['name']
    list_filter = ['category']

@admin.register(AthleteChallenge)
class AthleteChallengeAdmin(ImportExportModelAdmin):
    list_display = ['athlete']
    list_filter = ['athlete', 'date']
