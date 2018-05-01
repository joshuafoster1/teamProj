# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from training.views import get_user, DATE
from django.shortcuts import render, redirect
from .models import *
from timers.models import Timer
from django.utils.safestring import mark_safe
from .forms import *# Create your views here.
forms ={'BoulderingRoutineMetrics': BoulderingRoutineMetricsForm, 'RopeRoutineMetrics': RopeRoutineMetricsForm}
def practice_home(request):
    athlete = get_user(request)
    sessions = AssignedPractice.objects.filter(athlete=athlete)[:3]
    test = 1
    return render(request, 'schedule/home.html', {'athlete':athlete, 'sessions':sessions, 'date':DATE})
def practice_form(request, id):
    """
    need athlete, practice id,
    """
    # session = PracticeSection.objects.filter(practice__id=id).order_by('order')
    session_elements = list(PracticeSection.objects.values('form__name', 'timer__id', 'section__name', 'section__description', 'id').filter(practice__id=id).order_by('order'))
    athlete = get_user(request)
    print(request.session.get('practice_session'))
    if request.session.get('practice_session')== None:
        print('reset')
        request.session['practice_session'] = session_elements
        session_attributes = request.session.get('practice_session')[0]
    elif len(request.session['practice_session']) >=1:
        print('set')
        session_attributes= request.session.get('practice_session')[0]
    else:
        print('redirect')
        request.session['practice_session'] = None
        return redirect('practice_home')

    if request.method == 'POST':
        form = Form.objects.get(name=session_attributes['form__name']).get_form(forms)(request.POST)
        if form.is_valid():
            practice_section = form.save(commit=False)
            practice_section.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            practice_section.routine = PracticeSection.objects.get(id =session_attributes['id'])
            practice_section.save()
            eval_form = []
            request.session['practice_session']= list(request.session['practice_session'][1:])
            print("form", request.session['practice_session'])
            return redirect('practice', '1')
            # return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form, 'description': description,
            #         'timer':mark_safe(timer.get_timer()), 'section':section})

    else:
        form = Form.objects.get(name=session_attributes['form__name']).get_form(forms)()
        description = session_attributes['section__description']
        timer = Timer.objects.get(id=session_attributes['timer__id'])
        section = session_attributes['section__name']
    return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form, 'description': description,
            'timer':mark_safe(timer.get_timer()), 'section':section})

def practice_overview(request, id):
    pass
