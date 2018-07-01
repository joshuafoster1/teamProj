# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timers.models import Timer
from training.models import Athlete, Session, V_GRADES, ROUTE_GRADES
from django.db import models
from django.apps import apps

class TrainingPlan(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='assigned_practice_sessions')
    focus = models.CharField(max_length=30)
    Weeks = models.IntegerField()
    days = models.IntegerField()
    start = models.DateField(blank=True, null = True)
    end = models.DateField(blank=True, null=True)

    # general training plan goal ie. power, endurance, improve technique, improve body strength, finger strength
    ## can use general goal to format training plan
    # def create_training_plan(self):
    #     if self.athlete.eval_date > two weeks old

class AssignedPractice(models.Model):
    complete = models.DateField(blank=True, null = True)
    comment = models.CharField(max_length=200, blank=True)
    week = models.IntegerField()

    def __str__(self):
        return str(self.athlete.user.username) + ' ' + str(self.week)

    def practice_length(self):
        length = 0
        sections = PracticeSection.objects.filter(practice = self)
        length += section.length
        return length

class Form(models.Model):
    """Form objects must match the metric form class"""
    name = models.CharField(max_length=30)
    instance = models.CharField(null=True, blank=True, max_length=40)
    formset = models.BooleanField()

    def __str__(self):
        return self.name

    def get_form(self, forms):
        '''
        from dictionary of available forms return the call to form
        '''

        return forms[self.name]

    def retrieve_model(self):
        if self.formset:
            if self.name == 'BoulderingFormset':
                model = 'BoulderingRoutineMetrics'
            elif self.name =='RouteRedpointFormset':
                model = 'RouteRedpoint'
            elif self.name == 'BoulderRedpointFormset':
                model = 'BoulderRedpoint'
        else:
            model = self.name

        return apps.get_model('schedule', model)

class RefIntensity(models.Model):
    """
    Project = 1 above Redpoint, Redpoint = Hardest grade sent, Onsight = hardest send first try >%60,
    1 below Onsight, 2 below Onsight
    """
    CHOICES = (
        (1, '2 above redpoint'),
        (2, '1 above redpoint'),
        (3, 'Redpoint'),
        (4, 'Between Onsight and Redpoint'),
        (5, 'Onsight'),
        (6, '1 below onsight'),
        (7, '2 below onsight'),
        (8, 'Warmup'),
        (9, 'Resting on Wall'),
        (10, 'Rest')
    )
    # intensity = models.IntegerField(choices = CHOICES)
    intensity = models.CharField(max_length=30) # one above redpoint, redpoint, onsight, one below onsight, 2 below onsight
    def __str__(self):
        return self.intensity

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
    # length of time to complete?

    def __str__(self):
        return self.name

class PracticeSection(models.Model):
    order = models.IntegerField()
    section= models.ForeignKey(Protocol, related_name='practice_sections')
    practice = models.ForeignKey(AssignedPractice, related_name='practice_sections')

    def __str__(self):
        return self.section.name

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

class RouteProjectMetrics(Metrics):
    name = models.CharField(max_length=30)
    grade =  models.IntegerField(choices=ROUTE_GRADES)
    hangs = models.IntegerField()
    top = models.BooleanField()
    sent = models.BooleanField()

class BoulderProjectMetrics(Metrics):
    name = models.CharField(max_length=30)
    grade =  models.IntegerField(choices=V_GRADES)
    number_of_moves = models.IntegerField()
    moves_completed = models.IntegerField()
    sent = models.BooleanField()

class Top3BoulderSends(Metrics):
    send_1 =  models.IntegerField(choices=V_GRADES)
    send_2 =  models.IntegerField(choices=V_GRADES)
    send_3 =  models.IntegerField(choices=V_GRADES)

class Top3RopeSends(Metrics):
    send_1 =  models.IntegerField(choices=ROUTE_GRADES)
    send_2 =  models.IntegerField(choices=ROUTE_GRADES)
    send_3 =  models.IntegerField(choices=ROUTE_GRADES)

class Completion(Metrics):
    complete = models.BooleanField()

class BoulderRedpoint(Metrics):
    grade = models.IntegerField(choices=V_GRADES)
    sent = models.BooleanField()

class RouteRedpoint(Metrics):
    grade = models.IntegerField(choices=ROUTE_GRADES)
    sent = models.BooleanField()
