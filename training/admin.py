# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from .models import Athlete, Session, Conditioning, RefCategory, RefExercise, PinchBlocks, WeightedHangs
# Register your models here.

# class adminTable(admin.ModelAdmin):
#     model = Athlete
#     list_display = ('user', 'birthdate', 'guardian1', 'guardian2')
#     list_filter = ['birthdate']
#     search_fields = ['guardian1']

admin.site.register(Athlete)
# admin.site.register(Conditioning)
# admin.site.register(RefCategory)
# admin.site.register(RefExercise)
# admin.site.register(Session)
class ConditionInline2(forms.ModelForm):
    class Meta:
        model = Conditioning
        fields = ['exercise', 'repetitions', 'setNum']
    def __init__(self, *args, **kwargs):
        super(ConditionInline2, self).__init__(*args, **kwargs)
        self.fields['exercise'].queryset =RefExercise.objects.filter(category__id=2)
        # self.fields['repetitions'].queryset =RefExercise.objects.filter(category__id=3)
class ConditionInline1(forms.ModelForm):
    class Meta:
        model = Conditioning
        fields = ['exercise', 'repetitions', 'setNum']
    def __init__(self, *args, **kwargs):
        super(ConditionInline1, self).__init__(*args, **kwargs)
        self.fields['exercise'].queryset =RefExercise.objects.filter(category__id=1)
class ChoiceInline1(admin.TabularInline):
    form = ConditionInline1
    model = Conditioning
    # fields = ['exercise', 'repetitions']

    extra = 1

class ChoiceInline2(admin.TabularInline):
    form = ConditionInline2
    model = Conditioning
    # fields = ['exercise', 'repetitions']

    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    # registered to the session model
    fields = ['athlete']

    inlines = [ChoiceInline1, ChoiceInline2]

admin.site.register(Session, QuestionAdmin)
admin.site.register(Conditioning)
admin.site.register(RefCategory)
admin.site.register(RefExercise)
admin.site.register(PinchBlocks)
admin.site.register(WeightedHangs)
