# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Hangboard)

@admin.register(Timer)
class TimerAdmin(ImportExportModelAdmin):
    pass

@admin.register(Interval)
class IntervalAdmin(ImportExportModelAdmin):
    pass
