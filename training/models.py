# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    guardian1 = models.CharField(max_length=50, blank=True)
    guardian1_email = models.EmailField(max_length=75, blank=True)
    guardian2 = models.CharField(max_length=50, blank=True)
    guardian2_email = models.EmailField(max_length=75, blank=True)

    def __str__(self):
        return self.user.username


    ### Clean up the query to populate conditioning, categorize into dictionary.
    def get_pinch_training(self):

        last_session = PinchBlocks.objects.filter(session__athlete=self).last()
        last_pinches = PinchBlocks.objects.filter(session=last_session.session)
        return last_pinches

    def get_weighted_hangs(self):

        last_session = WeightedHangs.objects.filter(session__athlete=self).last()
        last_hangs = WeightedHangs.objects.filter(session=last_session.session)
        print "HERE", last_hangs
        return last_hangs


    def get_conditioning(self, category_id, average=False):
        '''return object'''

        conditionings = Conditioning.objects.filter(session__athlete=self,
                exercise__category__id=category_id).last()
        if average:
            exercise_instances = Conditioning.objects.filter(session__athlete=self, exercise=conditionings.exercise)
            instance_total = len(exercise_instances)
            rep_total = 0
            for instance in exercise_instances:
                rep_total += int(instance.repetitions)

            return {'object': conditionings, 'average':rep_total / instance_total}


        return {'object': conditionings}

    def can_do_weigthed_exercise(self):
        try:
            return date.today().year - self.birthdate.year > 13
        except:
            return False

    def get_category(self):
        '''Returns athlete category based on year of birth.'''
        try:
            athlete_years = date.today().year - self.birthdate.year

            if athlete_years < 11:
                return "Youth D"
            elif athlete_years < 13:
                return "Youth C"
            elif athlete_years < 15:
                return "Youth B"
            elif athlete_years < 17:
                return "Youth A"
            elif athlete_years < 19:
                return "Junior"

        except:
            return "Need Date of Birth"

    def get_user_info(self):
        """User information: Username, First Name, Last Name, email, Birthdate, Category"""

        user_info = []

        user_info.append(('User Name',self.user.username))
        user_info.append(('First Name', self.user.first_name))
        user_info.append(('Last Name', self.user.last_name))
        user_info.append(('Email', self.user.email))
        user_info.append(('Birthdate',self.birthdate))
        user_info.append(('Category', self.get_category()))

        return user_info


class Session(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='sessions')
    sessionDate = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('athlete', 'sessionDate')

    def get_first_set(self):
        '''returns multiple objects'''
        return Conditioning.objects.filter(session=self, setnum=1)

    def __str__(self):
        return str(self.sessionDate) + str(self.athlete.user.username)

class RefCategory(models.Model):
    description = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=40)

    def __str__(self):
        return self.category

    def get_last_exercise(self, athlete):
        try:
            last_exercise = Conditioning.objects.filter(session__athlete = athlete, exercise__category=self).last()
            return last_exercise.exercise
        except:
            return None

class RefExercise(models.Model):
    exercise = models.CharField(max_length=40)
    description = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(RefCategory, related_name='exercises')

    def get_avg(self):
        exercise_instances = Conditioning.objects.filter(exercise=self)
        instance_total = len(exercise_instances)
        rep_total = 0
        for instance in exercise_instances:
            rep_total += int(instance.repetitions)

        return rep_total / instance_total

    def __str__(self):
        return self.exercise

class Conditioning(models.Model):
    SETS = (
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
    )
    session = models.ForeignKey(Session, related_name='conditioning_sets')
    exercise = models.ForeignKey(RefExercise, related_name='conditioning_sets')
    repetitions = models.IntegerField()
    setNum = models.IntegerField(choices=SETS, default=1)

    class Meta:
        unique_together = ('session', 'exercise', 'setNum')

    def __str__(self):
        return self.session.athlete.user.username+ self.exercise.exercise +str(self.setNum)

class PinchBlocks(models.Model):

    session = models.ForeignKey(Session, related_name='pinch_blocks')
    pinch = models.ForeignKey(RefExercise, related_name='pinch_blocks') #, related_name='pinch_blocks')
    weight = models.IntegerField()
    seconds = models.IntegerField()

    def increase_weight(self):
        return self.seconds >=10

class WeightedHangs(models.Model):
    session = models.ForeignKey(Session, related_name='weighted_hangs')
    hang = models.ForeignKey(RefExercise, related_name="weighted_hangs")
    weight = models.IntegerField()
    seconds = models.IntegerField()

    def increase_weight(self):
        return self.seconds >=10

class Calendar(models.Model):
    post_date = models.DateField()
    event_date = models.DateField()
    event_title = models.CharField(max_length=100)
    event_description = models.CharField(max_length=300, blank=True)
    event_location = models.CharField(max_length=200, blank=True)
    event_format = models.CharField(max_length=100, blank=True)
