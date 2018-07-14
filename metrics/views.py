# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
import datetime
from .tables import *
from django_tables2 import RequestConfig
from django_pandas.io import read_frame

import logging

logger = logging.getLogger('poop')
def debugging(date, athlete):
    logger.debug("%s, %s", date, athlete)

logging.basicConfig(format='%(asctime)s %(message)s', filename= 'debug.log', filemode='a', level=logging.DEBUG)


DATE = datetime.date.today()

FORM_DICT = {'Finger Power': FingerPowerForm, 'Finger Endurance': FingerEnduranceForm,
    'Finger Muscular Endurance': FingerMuscularEnduranceForm, 'Pull and Slap': PullAndSlapForm, 'Max Weight Pull Up': MaxWeightPullUpForm,
    'Max Pull Ups': MaxPullUpsForm, 'Campus Power Endurance': CampusPowerEnduranceForm,
    'Lateral Core': LateralCoreForm, 'Sending Level': CurrentSendForm}

STANDARD_EVAL = ['Sending Level', 'Pull and Slap', 'Lateral Core', 'Campus Power Endurance',
                 'Finger Endurance']

def get_user(request):
    pk = request.user.pk
    athlete = get_object_or_404(Athlete, user__pk=pk)
    return athlete

def create_metric_data_table(metric, athlete):
    alt = read_frame(metric.retrieve_model().objects.filter(test__session__athlete=athlete).order_by('-test__session__sessionDate')[:5]).drop(['id'], axis=1).rename(columns={'test':'date'}).to_dict('records')
    if len(alt) >= 1:
        table = EvalTable(alt, extra_columns=[(str(key), tables.Column()) for key in alt[0].keys()])
    else:
        table = EvalTable([{'date':DATE}])
    RequestConfig(table)

    return table

def create_eval_summary_table(metric, athlete):
    data = read_frame(metric.retrieve_model().objects.filter(test__session__athlete=athlete).order_by('-test__session__sessionDate')[:2]).drop(['id'], axis=1).rename(columns={'test':'date'})
    # data['diff'] = data[0]-data[1]
    data = data.to_dict('records')

    if len(data) >= 1:
        table = EvalTable(data, extra_columns=[(str(key), tables.Column()) for key in data[0].keys()])
    else:
        table = EvalTable([{'date':DATE}])
    RequestConfig(table)

    return table


# Create your views here.
def metric_test(request, metricform):
    athlete = get_user(request)
    if request.method == 'POST':
        form = FORM_DICT[metricform](request.POST)
        if form.is_valid():
            metric_test = form.save(commit=False)
            debugging(DATE, athlete)
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            metrictest, created = MetricTest.objects.get_or_create(session=session)
            metric_test.test = metrictest
            metric_test.save()
            return redirect('athleteMetrics')
    else:
        form = FORM_DICT[metricform]()
    metric = MetricDescription.objects.get(metric=metricform)
    metric_data = metric.query(athlete.id)
    table = create_metric_data_table(metric, athlete)
    return render(request, 'metrics/metrics.html', {'athlete': athlete, 'date': DATE, 'form': form, 'metricdescription': metric, 'table': table})


def evaluation(request):
    athlete = get_user(request)
    if request.session.get('standard_eval')== None:
        request.session['standard_eval'] = STANDARD_EVAL
        eval_form = request.session.get('standard_eval')[0]
    elif len(request.session['standard_eval']) >=1:
        eval_form = request.session.get('standard_eval')[0]
    else:
        request.session['standard_eval'] = None
        return redirect('eval_summary')

    if request.method == 'POST':

        form =FORM_DICT[eval_form](request.POST)
        if form.is_valid():
            metric_test = form.save(commit=False)
            debugging(DATE, athlete)
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            metrictest, created = MetricTest.objects.get_or_create(session=session)
            metric_test.test = metrictest
            metric_test.save()
            eval_form = []
            request.session['standard_eval']= list(request.session['standard_eval'][1:])

            return redirect('evaluation')
    else:
        form = FORM_DICT[eval_form]()

    metric = MetricDescription.objects.get(metric=eval_form)
    metric_data = metric.query(athlete.id)
    table = create_metric_data_table(metric, athlete)

    return render(request, 'metrics/metrics.html', {'athlete': athlete, 'date': DATE, 'form': form, 'metricdescription': metric, 'table':table})


def eval_summary(request):
    athlete = get_user(request)
    athlete.eval_date = DATE
    athlete.save()
    metrics = []
    for evaluation in STANDARD_EVAL:
        metric = MetricDescription.objects.get(metric=evaluation)
        table = create_eval_summary_table(metric, athlete)
        metrics.append({'name': metric.metric, 'table':table})
    return render(request, 'metrics/eval_summary.html', {'athlete': athlete, 'date':DATE, 'metrics': metrics})
