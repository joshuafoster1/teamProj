# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from metrics.models import MetricTest
from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from timers.models import Timer
# Create your models here.
DATE = date.today()
ROUTE_GRADES = (
        (0, '5.8'),
        (1, '5.9'),
        (2, '5.10a'),
        (3, '5.10b'),
        (4, '5.10c'),
        (5, '5.10d'),
        (6, '5.11a'),
        (7, '5.11b'),
        (8, '5.11c'),
        (9, '5.11d'),
        (10, '5.12a'),
        (11, '5.12b'),
        (12, '5.12c'),
        (13, '5.12d'),
        (14, '5.13a'),
        (15, '5.13b'),
        (16, '5.13c'),
        (17, '5.13d'),
        (18, '5.14a'),

)
V_GRADES = (
        (0, 'V0'),
        (1, 'V1'),
        (2, 'V2'),
        (3, 'V3'),
        (4, 'V4'),
        (5, 'V5'),
        (6, 'V6'),
        (7, 'V7'),
        (8, 'V8'),
        (9, 'V9'),
        (10, 'V10'),
        (11, 'V11')
)


class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    wingspan = models.IntegerField(null=True, blank=True)
    ape_index = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    guardian1 = models.CharField(max_length=50, blank=True)
    guardian1_email = models.EmailField(max_length=75, blank=True)
    guardian2 = models.CharField(max_length=50, blank=True)
    guardian2_email = models.EmailField(max_length=75, blank=True)
    eval_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def needs_eval(self):
        if self.eval_date == None:
            return True
        elif self.eval_date + timedelta(days=42) < DATE:
            return True
        else:
            return False

    def get_most_recent_metric_test(self):
        try:
            test = Session.objects.filter(athlete=self).latest('metric_tests__session__sessionDate')

            return test
        except:
            return None
    def get_ape_index(self):
        if self.ape_index:
            return self.ape_index
        else:
            self.ape_index = self.wingspan - self.height
            self.save()
            return self.ape_index

    def get_assigned_practice(self):
        assigned_practice = AssignedPractice.objects.filter(athlete=self)
        calendar = []
        for item in assigned_practice:
            if item.practice.is_valid(DATE):
                calendar.append(item)

        return calendar

    def get_weighted_training(self, training, max_weight=False):
        '''Returns completed hangs from precious session containing hangs.'''

        last_session = training.objects.filter(session__athlete=self).last()
        try:
            if max_weight:
                last_hangs = max(training.objects.filter(session=last_session.session).values('weight'))
            else:
                last_hangs = training.objects.filter(session=last_session.session)

            return last_hangs
        except:
            return None

    def get_conditioning(self, category_id, average=False):
        '''return dictionary object {object:"", average:int}.'''

        conditionings = Conditioning.objects.filter(session__athlete=self,
                exercise__category__id=category_id).last()

        if average:
            try:
                exercise_instances = Conditioning.objects.filter(session__athlete=self, exercise=conditionings.exercise)
                instance_total = len(exercise_instances)
                rep_total = 0
                for instance in exercise_instances:
                    rep_total += int(instance.repetitions)

                return {'object': conditionings, 'average':rep_total / instance_total}
            except:
                return None

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
            else:
                return "Too old!!!"

        except:
            return "Need Date of Birth"

    def get_user_info(self):
        """User information in a list of tuples: Username, First Name, Last Name, email, Birthdate, Category"""

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


    def __str__(self):
        return str(self.athlete.user.username) + ' '+str(self.sessionDate) 


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
    order = models.IntegerField()
    goal = models.IntegerField()

    # class Meta:
    #     unique_together = ('category', 'order')

    def __str__(self):
        return self.exercise

class MaxConditioning(models.Model):
    session = models.ForeignKey(Session, related_name='max_conditioning_sets')
    exercise = models.ForeignKey(RefExercise, related_name='max_conditioning_sets')
    repetitions = models.IntegerField()

    class Meta:
        unique_together = ('session', 'exercise')

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

    def __str__(self):
        return self.session.athlete.user.username + str(self.session.sessionDate) + self.pinch.exercise

    def increase_weight(self):
        return self.seconds >=10


class WeightedHangs(models.Model):
    session = models.ForeignKey(Session, related_name='weighted_hangs')
    hang = models.ForeignKey(RefExercise, related_name="weighted_hangs")
    weight = models.IntegerField()
    seconds = models.IntegerField()

    def __str__(self):
        return self.session.athlete.user.username + str(self.session.sessionDate) + self.hang.exercise

    def increase_weight(self):
        return self.seconds >=10


class Calendar(models.Model):
    post_date = models.DateField()
    event_date = models.DateField()
    event_title = models.CharField(max_length=100)
    event_description = models.CharField(max_length=300, blank=True)
    event_location = models.CharField(max_length=200, blank=True)
    event_format = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.event_title + str(self.event_date)

    def is_valid(self, date):
        if date < self.event_date:
            return True
        else:
            return False



class RefRoutine(models.Model):
    routine = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.routine



class RefConditioning(models.Model):
    conditioning = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.conditioning

class RefFingerTraining(models.Model):
    finger_training = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)
    def __str__(self):
        return self.finger_training

class RefTechnique(models.Model):
    technique = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.technique

class RefTechniqueDrill(models.Model):
    primary_technique = models.ForeignKey(RefTechnique, related_name='technique_drill1')
    secondary_technique = models.ForeignKey(RefTechnique, blank=True, null=True, related_name='technique_drill2')
    drill = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.drill

class RefWarmup(models.Model):
    warmup = models.CharField(max_length=100)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.warmup

class Practice(models.Model):
    warmup = models.ForeignKey(RefWarmup, related_name='practice1')
    technique = models.ForeignKey(RefTechniqueDrill, related_name='practice2')
    routine_1 = models.ForeignKey(RefRoutine, related_name='practice3')
    routine_2 = models.ForeignKey(RefRoutine, blank=True, null=True, related_name='practice4')
    conditioning_1 = models.ForeignKey(RefConditioning, related_name='practice5')
    conditioning_2 = models.ForeignKey(RefConditioning, blank=True, null=True, related_name='practice6')
    finger_training = models.ForeignKey(RefFingerTraining, blank=True, null=True, related_name='practice7')
    date = models.DateField()

    def __str__(self):
        return "practice: " + str(self.date)

    def is_valid(self, date):
        if date < self.date:
            return True
        else:
            return False

class AssignedPractice(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='assigned_practices')
    practice = models.ForeignKey(Practice, related_name='assigned_practices')
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.athlete) + " " + str(self.practice.date)


class ClimbingQuotes(models.Model):
    author = models.CharField(max_length=30)
    quote = models.CharField(max_length=200)
