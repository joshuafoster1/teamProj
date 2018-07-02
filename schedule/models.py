# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timers.models import Timer
from metrics.models import SendingLevel
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

    # general training plan goal ie. power, endurance, improve technique,
     # improve body strength, finger strength
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
    Metabolic system
    """

    intensity = models.CharField(max_length=30)
    def __str__(self):
        return self.intensity

class RoutineType(models.Model):
    """
    Boulder, Rope, hangboard, conditioning, warmup, technique
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class GradeLevel(models.Model):
    reference = models.CharField(max_length=20)
    relative_to_onsight = models.IntegerField()

    def __str__(self):
        return self.reference

class Protocol(models.Model):
    routine_type = models.ForeignKey(RoutineType, related_name='practice_sections')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True)
    goal = models.CharField(max_length=150, blank = True)
    intensity = models.ForeignKey(RefIntensity, null=True, blank=True, related_name='practice_sections')
    timer = models.ForeignKey(Timer, null=True, blank=True, related_name='practice_sections')
    form = models.ForeignKey(Form, null=True, blank=True, related_name='practice_sections')
    grade_level = models.ForeignKey(GradeLevel, related_name='practice_sessions')
    # length of time to complete?

    def __str__(self):
        return self.name

    def get_grade_level(self, athlete):
        if SendingLevel.objects.filter(test__session__athlete=athlete).exists():
            ### Need to pull most recent sending level eval###
            sendinglevel = SendingLevel.objects.filter(test__session__athlete=athlete)[0]#.latest('test')

            if self.routine_type.name == 'Rope Routine':
                grade_level = sendinglevel.route_onsight + self.grade_level.relative_to_onsight
                grades = dict(ROUTE_GRADES)

                if grade_level<= 0:
                    return grades['0']
                else:
                    return grades[grade_level]

            elif self.routine_type.name == 'Boulder Routine':
                grade_level = sendinglevel.boulder_onsight + self.grade_level.relative_to_onsight
                grades = dict(V_GRADES)

                if grade_level<= 0:
                    return grades['0']
                else:
                    return grades[grade_level]

        else:
            return 'Fill out the metric form for Sending Level'

class PracticeSection(models.Model):
    order = models.IntegerField()
    section= models.ForeignKey(Protocol, related_name='practice_sections')
    practice = models.ForeignKey(AssignedPractice, related_name='practice_sections')

    def __str__(self):
        return self.section.name

class Metrics(models.Model):
    session = models.ForeignKey(Session, related_name='metrics')
    routine = models.ForeignKey(Protocol, related_name='metrics')

    def __str__(self):
        return self.routine.name


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

    def __str__(self):
        return self.routine.name


class RopeRoutineMetrics(models.Model):
    session = models.ForeignKey(Session, related_name='route_metrics')
    routine = models.ForeignKey(Protocol, related_name='route_metrics')
    total_climbs = models.IntegerField()
    max = models.IntegerField(choices=ROUTE_GRADES)
    min = models.IntegerField(choices=ROUTE_GRADES)

    def __str__(self):
        return self.routine.name


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
