# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timers.models import Timer
from training.models import Athlete, Session, V_GRADES, ROUTE_GRADES
from django.db import models

class TrainingPlan(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='assigned_practice_sessions')
    focus = models.CharField(max_length=30)
    Weeks = models.IntegerField()
    days = models.IntegerField()
    start = models.DateField(blank=True, null = True)
    end = models.DateField(blank=True, null=True)

    # def create_training_plan(self):
    #     if Metrics.objects.filter(athlete = self.athlete, date__gt=date-2weeks).exists():

class AssignedPractice(models.Model):
    complete = models.DateField(blank=True, null = True)
    comment = models.CharField(max_length=200, blank=True)
    week = models.IntegerField()

    def __str__(self):
        return str(self.athlete.user.username) + ' ' + str(self.week)


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

class RefIntensity(models.Model):
    """
    Project = 1 above Redpoint, Redpoint = Hardest grade sent, Onsight = hardest send first try >%60,
    1 below Onsight, 2 below Onsight
    """
    hi = models.CharField(max_length=30)
    metabolic_focus = models.CharField(max_length=30)

class RoutineType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Protocol(models.Model):
    routine_type = models.ForeignKey(RoutineType, related_name='practice_sections')#warmup, climb routine, technique, hangboard, etc
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True)
    goal = models.CharField(max_length=150, blank = True)
    intensity = models.ForeignKey(RefIntensity, null=True, blank=True, related_name='practice_sections')
    timer = models.ForeignKey(Timer, null=True, blank=True, related_name='practice_sections')
    form = models.ForeignKey(Form, null=True, blank=True, related_name='practice_sections')

    def __str__(self):
        return self.name

class PracticeSection(models.Model):
    order = models.IntegerField()
    section= models.ForeignKey(Protocol, related_name='practice_sections')
    practice = models.ForeignKey(AssignedPractice, related_name='practice_sections')

    def __str__(self):
        return self.section.name

class IsolatedProtocol(models.Model):
    protocol = models.ForeignKey(Protocol, related_name='isolated_protocols')
    session = models.ForeignKey(Session, related_name='isolated_protocols')

class Metrics(models.Model):
    session = models.ForeignKey(Session, related_name='metrics')
    routine = models.ForeignKey(Protocol, related_name='metrics')

class BoulderingRoutineMetrics(models.Model):
    """
    metrics that apply to all bouldering routines? average points, total points,...
    """
    session = models.ForeignKey(Session, related_name='boulder_metrics')
    routine = models.ForeignKey(Protocol, related_name='boulder_metrics')
    total_points = models.IntegerField()
    total_climbs = models.IntegerField()
    max = models.IntegerField(choices=V_GRADES)
    min = models.IntegerField(choices=V_GRADES)

class RopeRoutineMetrics(models.Model):
    session = models.ForeignKey(Session, related_name='route_metrics')
    routine = models.ForeignKey(Protocol, related_name='route_metrics')
    total_climbs = models.IntegerField()
    max = models.IntegerField(choices=ROUTE_GRADES)
    min = models.IntegerField(choices=ROUTE_GRADES)

class HangboardMetrics(Metrics):
    complete = models.BooleanField()

# class WeightedMetrics
