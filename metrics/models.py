# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from training.models import Session, Athlete, V_GRADES, ROUTE_GRADES
from django.db import models, connection
from django.apps import apps
# Create your models here.
# class MetricTestInformation(model.Models):
#     test = models.CharField

RUNG = (
    (1, "Small"),
    (2, "Medium"),
    (3, "Large"),
)


class MetricTest(models.Model):
    session = models.ForeignKey(Session, related_name='metric_tests')

    def __str__(self):
        return str(self.session.sessionDate)

class SendingLevel(models.Model):
    test = models.ForeignKey(MetricTest, related_name='sending_level')
    boulder_onsight = models.IntegerField(choices=V_GRADES, blank=True, null=True)
    boulder_redpoint = models.IntegerField(choices=V_GRADES, blank=True, null=True)
    route_onsight = models.IntegerField(choices=ROUTE_GRADES, blank=True, null=True)
    route_redpoint = models.IntegerField(choices=ROUTE_GRADES, blank=True, null=True)

class FingerPower(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_power_tests')
    weight = models.IntegerField()
    time = models.IntegerField()

    def __str__(self):
        return str(self.weight) + " " + str(self.time)


class FingerMuscularEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_muscular_endurance_tests')
    time = models.IntegerField()

    def __str__(self):
        return str(self.weight) + " " + str(self.time)


class FingerEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='finger_endurance_tests')
    time = models.IntegerField()
    rung = models.IntegerField(choices=RUNG)
    feet_on = models.BooleanField()

    def __str__(self):
        return str(self.weight) + " " + str(self.time)


class PullAndSlap(models.Model):
    test = models.ForeignKey(MetricTest, related_name='pull_and_slaps')
    height_right_hand = models.IntegerField()
    height_left_hand = models.IntegerField()

    def __str__(self):
        return str(self.height_left_hand) + " " + str(self.height_right_hand)


class MaxWeightPullUp(models.Model):
    test = models.ForeignKey(MetricTest, related_name='max_weight_pull_ups')
    weight = models.IntegerField()
    lateral = models.BooleanField()

    def __str__(self):
        return str(self.weight) + " " + str(self.lateral)


class MaxPullUps(models.Model):
    test = models.ForeignKey(MetricTest, related_name='max_pull_ups')
    repetitions = models.IntegerField()
    lateral = models.BooleanField()

    def __str__(self):
        return str(self.repetitions) + " " + str(self.lateral)


class CampusPowerEndurance(models.Model):
    test = models.ForeignKey(MetricTest, related_name='campus_power_endurance')
    moves = models.IntegerField()
    time = models.IntegerField()
    rung = models.IntegerField(choices=RUNG)
    feet_on = models.BooleanField()

    def __str__(self):
        return str(self.moves) + " " + str(self.time)


class LateralCore(models.Model):
    test = models.ForeignKey(MetricTest, related_name='lateral_core')
    distance_left_side = models.IntegerField()
    distance_right_side = models.IntegerField()

    def __str__(self):
        return str(self.distance_left_side) + " " + str(self.distance_right_side)


class MetricDescription(models.Model):
    metric = models.CharField(max_length=100)# key for
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.metric

    def query(self, athleteID):
        model = 'metrics_' + ''.join(self.metric.split()).lower()
        with connection.cursor() as cursor:
            string = '''
                    join metrics_metrictest
                    on (test_id=metrics_metrictest.id)
                    join training_session
                    on (session_id=training_session.id)
                    where (athlete_id = 1) '''
            cursor.execute('select * from '+model+string)#, str(athleteID)])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row))for row in cursor.fetchall()]

        #     rows = cursor.fetchall()
        # return rows
    def retrieve_model(self):
        model = ''.join(self.metric.split())
        return  apps.get_model('metrics', model)
