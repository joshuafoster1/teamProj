# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    guardian1 = models.CharField(max_length=50, blank=True)
    guardian1_email = models.EmailField(max_length=75, blank=True)
    guardian2 = models.CharField(max_length=50, blank=True)
    guardian2_email = models.EmailField(max_length=75, blank=True)
    # catergory = birthday related value

    def __str__(self):
        return self.user.username

class Session(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='sessions')
    sessionDate = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('athlete', 'sessionDate')

    def get_first_set(self):
        '''returns multiple objects'''
        return Conditioning.objects.filter(session=self, setnum=1)

    def __str__(self):
        return str(self.sessionDate)

class RefCategory(models.Model):
    description = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=40)

    def __str__(self):
        return self.category

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
        (1, '1'),
        (2, '2'),
        (3, '3'),
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
    BLOCK = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    session = models.ForeignKey(Session, related_name='pinch_blocks')
    block = models.IntegerField(choices=BLOCK, default=1)
    seconds = models.IntegerField()

class WeightedHangs(models.Model):
    RUNG = (
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Large'),
    )
    session = models.ForeignKey(Session, related_name='weighted_hangs')
    rung = models.IntegerField(choices=RUNG, default=1)
    seconds = models.IntegerField()
