# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from training.views import get_user, DATE
from django.shortcuts import render, redirect
from .models import *
from timers.models import Timer
from django.utils.safestring import mark_safe
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from pandas_highcharts.core import serialize
from django.http import JsonResponse
from metrics.tables import EvalTable
from django_tables2 import RequestConfig, Column
from django_pandas.io import read_frame


# Create your views here.

forms ={'BoulderingRoutineMetrics': BoulderingRoutineMetricsForm, 'RopeRoutineMetrics': RopeRoutineMetricsForm,
        'HangboardMetrics':HangboardMetrics, 'RouteRedpointFormset':RouteRedpointFormset, 'BoulderRedpointFormset': BoulderRedpointFormset,
        'BoulderingFormset':BoulderingFormset, 'Top3RopeSendsForm': Top3RopeSendsForm, 'Top3BoulderSendsForm':Top3RopeSendsForm}

def create_metric_data_table(protocal, athlete, routine):
    alt = read_frame(protocal.form.retrieve_model().objects.filter(session__athlete=athlete, routine__name = routine)
            .order_by('-session__sessionDate')[:2]) \
            .rename(columns={'session':'date'}) \
            .drop(['id', 'routine'], axis=1).to_dict('records')
    if len(alt) >= 1:
        table = EvalTable(alt, extra_columns=[(str(key), Column()) for key in alt[0].keys()])
    else:
        table = EvalTable([{'date':DATE}])
    RequestConfig(table)

    return table
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
    table = create_metric_data_table(protocol_object, athlete, protocol_object.name)
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
                    try:
                        protocol_data.save()
                    except:
                        continue
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
    goal = protocol_object.goal
    if timer:
        return render(request, 'schedule/practice.html', {'athlete': athlete, 'date': DATE, 'form': form,'formset':formset, 'description': description,
                'timer':mark_safe(timer.get_timer()), 'section':protocol_object, 'table':table})

    return render(request, 'schedule/practice.html',
        {'athlete': athlete, 'date': DATE, 'form': form, 'formset':formset, 'goal': goal, 'description': description,
             'section':protocol_object, "table": table})


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
    return render(request, 'schedule/practice.html',
        {'athlete': athlete, 'date': DATE, 'form': form, 'description': description,
            'timer':mark_safe(timer.get_timer()), 'section':section})


def protocol_summary(request):
    '''Relies on django_highcharts for serializing data. Makes multiple chart
    rendering on a page more simple, however it doesn't appear to allow much
    in they way of customization.
    '''
    '''define a range, avg, diplay max and min'''

    athlete = get_user(request)
    data = BoulderingRoutineMetrics.objects.filter(session__athlete = athlete)
    test = BoulderingRoutineMetrics.objects.values('min', 'max').filter(session__athlete = athlete)
    df = read_frame(data, verbose=False)
    df['avg'] = df['total_points']/df['total_climbs']
    df['range'] = df['max']-df['min']
    df = df.drop(['id','total_climbs', 'total_points'], axis=1).set_index('session')
    dataset = BoulderingRoutineMetrics.objects \
        .values('session__sessionDate', 'min','max', 'total_points', 'total_climbs') \
        .filter(session__athlete = athlete)
    df2 = read_frame(dataset, verbose=False).rename(columns={'session__sessionDate':'session date','min':'min value','max':'max value'})
    df3 = read_frame(dataset, fieldnames=['min','max'])\
                   .rename(columns={'session__sessionDate':'Session Date'})
                   # .drop(['total_points', 'total_climbs'])

    df4 = df2.merge(df3, how='left', left_index=True, right_index=True)
    print(df4)
    df4['avg']=df4['total_points']/df4['total_climbs']
    df4['range']=df4['max value']-df4['min value']
    chart = serialize(df4, render_to='my-chart', kind="bar", output_type='json')

    return render(request, 'schedule/protocol_summary.html', {'chart':chart})

def practice_overview(request, id):
    pass

def json_example(request):
    return render(request, 'schedule/json_example.html')

def chart_data(request):
    """
    Uses Ajax call for dynamic rendering and allows access to all highchart features.
    Appears to be more challenging to apply multiple charts to one page
    """
    ############ some day put in the time for asynchronous drilldown: https://www.highcharts.com/docs/chart-concepts/drilldown
    athlete = get_user(request)

    dataset = BoulderingRoutineMetrics.objects \
        .values('session__sessionDate', 'min','max', 'total_points', 'total_climbs') \
        .filter(session__athlete = athlete).order_by('session__sessionDate').reverse()[:5]
    df = read_frame(dataset, verbose=False)

    df['avg'] = (df['total_points']/df['total_climbs']).round(1)
    df['range'] = df['max']-df['min']
    categories = list(df['session__sessionDate'])
    df = df.drop(columns = ['session__sessionDate'])
    columns = df.columns
    lst=[]
    for item in columns:
        lst.append({'name':item,'data':df.loc[:,item].tolist()})

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Super Sick Chart'},
        # 'xAxis': {'categories': categories},
        'series': [{
            'name': 'Things',
            'colorByPoint': 'true',
            'data': [{
                'name': 'Animals',
                'y': 5,
                'drilldown': 'animals'
            }, {
                'name': 'Fruits',
                'y': 2,
                'drilldown': 'fruits'
            }, {
                'name': 'Cars',
                'y': 4,
                'drilldown': 'cars'
            }]
        }],
        'drilldown': {
            'series': [{
                'id': 'animals',
                'data': [
                    ['Cats', 4],
                    ['Dogs', 2],
                    ['Cows', 1],
                    ['Sheep', 2],
                    ['Pigs', 1]
                ]
            }, {
                'id': 'fruits',
                'data': [
                    ['Apples', 4],
                    ['Oranges', 2]
                ]
            }, {
                'id': 'cars',
                'data': [
                    ['Toyota', 4],
                    ['Opel', 2],
                    ['Volkswagen', 2]
                ]
            }]
        },
        # 'series': lst,
        'plotOptions':{'column':{'dataLabels': {'enabled':'true'}}}
    }
    return JsonResponse(chart)
