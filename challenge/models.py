# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from training.models import Athlete, DATE
# Create your models here.

class AthChallManager(models.Manager):
    def add_challenge(self, athlete, challenge):
        challenge = self.create(athlete=athlete, challenge=challenge, date = DATE)

        return challenge

### MODELS ###
class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=150, blank = True, null = True)
    category = models.ForeignKey(Category, related_name='challenges')

    def __str__(self):
        return self.name


class AthleteChallenge(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='completed_challenges')
    date = models.DateField()
    challenge = models.ForeignKey(Challenge, related_name='ahtlete_challenges')

    objects = AthChallManager()

    def __str__(self):
        return self.athlete.user.username + ' ' + str(self.date) + ' ' + self.challenge.name
