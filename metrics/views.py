# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
import datetime

DATE = datetime.date.today()
FORM_DICT = {'fingerpower': FingerPowerForm, 'fingerendurance': FingerEnduranceForm,
    'fingerpowerendurance': FingerMuscularEnduranceForm, 'pullandslap': PullAndSlapForm, 'maxweightpullup': MaxWeightPullUpForm,
    'maxpullups': MaxPullUpsForm, 'campuspowerendurance': CampusPowerEnduranceForm,
    'lateralcore': LateralCoreForm}

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
            print(metrictest)
            metric_test.test = metrictest
            metric_test.save()
            return redirect('athleteMetrics')
    else:
        form = FORM_DICT[metricform]()
        metric_description = MetricDescription.objects.get(metric=metricform)
        print(metric_description.description)

    return render(request, 'metrics/metrics.html', {'athlete': athlete, 'date': DATE, 'form': form, 'metricdescription': metric_description})
