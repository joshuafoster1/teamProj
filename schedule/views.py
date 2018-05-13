# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from training.views import get_user, DATE
from django.shortcuts import render, redirect
from .models import *
from timers.models import Timer
from django.utils.safestring import mark_safe
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.

forms ={'BoulderingRoutineMetrics': BoulderingRoutineMetricsForm, 'RopeRoutineMetrics': RopeRoutineMetricsForm,
        'HangboardMetrics':HangboardMetrics, 'RouteRedpointFormset':RouteRedpointFormset, 'BoulderRedpointFormset': BoulderRedpointFormset,
        'BoulderingFormset':BoulderingFormset, 'Top3RopeSendsForm': Top3RopeSendsForm, 'Top3BoulderSendsForm':Top3RopeSendsForm}

def protocol_home(request, protocol_type):
    """
    Display either conditioning, hangboard, routine or other type of workouts
    """
    power_protocols = Protocol.objects.values('name', 'description').filter(intensity__intensity= "Power", routine_type__name = protocol_type)
    power_endurance_protocols = Protocol.objects.values('name', 'description').filter(intensity__intensity = "Power Endurance", routine_type__name = protocol_type)
    endurance_protocols = Protocol.objects.values('name', 'description').filter(intensity__intensity = "Endurance", routine_type__name = protocol_type)
    print(protocol_type)
    return render(request, 'schedule/protocol_display.html', {'power_protocols': power_protocols,'power_endurance_protocols': power_endurance_protocols,'endurance_protocols': endurance_protocols, 'protocol_type': protocol_type})

@login_required
def protocol(request, protocol):
    athlete = get_user(request)
    protocol_object = Protocol.objects.get(name=protocol)
    formset = protocol_object.form.formset
    print(formset)
    if request.method == "POST":
        print("POST")
        form = protocol_object.form.get_form(forms)(request.POST)
        if formset:
            if form.is_valid():
                for set in form:
                    protocol_data = set.save(commit=False)
                    protocol_data.session, created = Session.objects.get_or_create(sessionDate=DATE,
                        athlete=athlete)
                    protocol_data.routine = protocol_object
                    protocol_data.save()
                    return redirect('home')

        elif form.is_valid():
            print("VALID")
            protocol_data = form.save(commit=False)
            protocol_data.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            protocol_data.routine = protocol_object
            protocol_data.save()
            return redirect('home')
    else:
        if formset:
            form = protocol_object.form.get_form(forms)()#queryset = BoulderingRoutineMetrics.objects.none())
        else:
            form = protocol_object.form.get_form(forms)()
    timer = protocol_object.timer
    description = protocol_object.description
    if timer:
        return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form,'formset':formset, 'description': description,
                'timer':mark_safe(timer.get_timer()), 'section':protocol_object})

    return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form, 'formset':formset, 'description': description,
             'section':protocol_object})


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
    session_elements = list(PracticeSection.objects.values('section__form__name', 'section__timer__id', 'section__name', 'section__description', 'id').filter(practice__id=id).order_by('order'))
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
        form = Form.objects.get(name=session_attributes['section__form__name']).get_form(forms)(request.POST)
        if form.is_valid():
            practice_section = form.save(commit=False)
            practice_section.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            practice_section.routine = Protocol.objects.get(id =session_attributes['id'])
            practice_section.save()
            eval_form = []
            request.session['practice_session']= list(request.session['practice_session'][1:])
            print("form", request.session['practice_session'])
            return redirect('practice', '1')
            # return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form, 'description': description,
            #         'timer':mark_safe(timer.get_timer()), 'section':section})

    else:
        form = Form.objects.get(name=session_attributes['section__form__name']).get_form(forms)()
        description = session_attributes['section__description']
        timer = Timer.objects.get(id=session_attributes['section__timer__id'])
        section = session_attributes['section__name']
    return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form, 'description': description,
            'timer':mark_safe(timer.get_timer()), 'section':section})

def practice_overview(request, id):
    pass
