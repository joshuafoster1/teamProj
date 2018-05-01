# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timers.models import Timer
from training.models import Athlete, Session, V_GRADES, ROUTE_GRADES
from django.db import models



class AssignedPractice(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='assigned_practice_sessions')
    date = models.DateField()
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.athlete.user.username) + ' ' + str(self.date)


class Form(models.Model):
    """Form objects must match the metric form class"""
    name = models.CharField(max_length=30)
    instance = models.CharField(null=True, blank=True, max_length=40)
    def __str__(self):
        return self.name

    def get_form(self, forms):
        '''
        from dictionary of available forms return the call to form
        '''

        return forms[self.name]


class RefSectionType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class RefSection(models.Model):
    type = models.ForeignKey(RefSectionType, related_name='practice_sections')#warmup, climb routine, technique, hangboard, etc
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

class PracticeSection(models.Model):
    order = models.IntegerField()
    section= models.ForeignKey(RefSection, related_name='practice_sections')
    practice = models.ForeignKey(AssignedPractice, related_name='practice_sections')
    timer = models.ForeignKey(Timer, related_name='practice_sections')
    form = models.ForeignKey(Form, related_name='practice_sections')

    def __str__(self):
        return self.section.name


class BoulderingRoutineMetrics(models.Model):
    """
    metrics that apply to all bouldering routines? average points, total points,...
    """
    session = models.ForeignKey(Session, related_name='boulder_metrics')
    routine = models.ForeignKey(PracticeSection, related_name='boulder_metrics')
    total_points = models.IntegerField()
    total_climbs = models.IntegerField()
    max = models.IntegerField(choices=V_GRADES)
    min = models.IntegerField(choices=V_GRADES)

class RopeRoutineMetrics(models.Model):
    session = models.ForeignKey(Session, related_name='route_metrics')
    routine = models.ForeignKey(PracticeSection, related_name='route_metrics')
    total_climbs = models.IntegerField()
    max = models.IntegerField(choices=ROUTE_GRADES)
    min = models.IntegerField(choices=ROUTE_GRADES)

# class WeightedMetrics
