# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
import datetime

DATE = datetime.date.today()

FORM_DICT = {'Finger Power': FingerPowerForm, 'Finger Endurance': FingerEnduranceForm,
    'Finger Power Endurance': FingerMuscularEnduranceForm, 'Pull and Slap': PullAndSlapForm, 'Max Weight Pull Up': MaxWeightPullUpForm,
    'Max Pull Ups': MaxPullUpsForm, 'Campus Power Endurance': CampusPowerEnduranceForm,
    'Lateral Core': LateralCoreForm, 'Sending Ability': CurrentSendForm}

STANDARD_EVAL = ['Sending Ability', 'Pull and Slap', 'Lateral Core', 'Campus Power Endurance',
                 'Finger Endurance']

def get_user(request):
    pk = request.user.pk
    athlete = get_object_or_404(Athlete, user__pk=pk)
    return athlete


# Create your views here.
def metric_test(request, metricform):
    # process_metric_form(FORM_DICT[form])
    athlete = get_user(request)
    if request.method == 'POST':
        form = FORM_DICT[metricform](request.POST)
        if form.is_valid():
            metric_test = form.save(commit=False)
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            metrictest, created = MetricTest.objects.get_or_create(session=session)
            metric_test.test = metrictest
            metric_test.save()
            return redirect('athleteMetrics')
    else:
        form = FORM_DICT[metricform]()
    metric_description = MetricDescription.objects.get(metric=metricform)

    return render(request, 'metrics/metrics.html', {'athlete': athlete, 'date': DATE, 'form': form, 'metricdescription': metric_description})
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
        metric_description = MetricDescription.objects.get(metric=eval_form)

    return render(request, 'metrics/metrics.html', {'athlete': athlete, 'date': DATE, 'form': form, 'metricdescription': metric_description})

def eval_summary(request):
    athlete = get_user(request)
    athlete.eval_date = DATE
    athlete.save()
    return render(request, 'metrics/eval_summary.html', {'athlete': athlete, 'date':DATE})
