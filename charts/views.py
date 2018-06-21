# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django_pandas.io import read_frame
from pandas_highcharts.core import serialize
from django.http import JsonResponse
from django.utils.safestring import mark_safe

# Create your views here.
def create_chart(df, title):
    categories = list(df['session__sessionDate'])
    df = df.drop(columns = ['session__sessionDate'])
    columns = df.columns
    lst=[]
    for item in columns:

        lst.append({'name':item,'data':df.loc[:,item].tolist()})
    print(lst)
    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': title},
        'yAxis': {'categories': categories},
        'series': lst,
        'plotOptions':{}
    }

    return chart


def rope_routine(request):
    athlete = get_user(request)

    dataset = RopeRoutineMetrics.objects \
        .values('session__sessionDate', 'min','max', 'total_climbs') \
        .filter(session__athlete = athlete).order_by('session__sessionDate').reverse()[:5]
    df = read_frame(dataset, verbose=False)

    chart = create_chart(df, 'Rope Metrics')


def
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

def bouldering_routine(request):
    """
    Uses Ajax call for dynamic rendering and allows access to all highchart features.
    Appears to be more challenging to apply multiple charts to one page
    """
    athlete = get_user(request)

    dataset = BoulderingRoutineMetrics.objects \
        .values('session__sessionDate', 'min','max', 'total_points', 'total_climbs') \
        .filter(session__athlete = athlete)


    chart = create_chart(dataset, 'Bouldering Points')

    return JsonResponse(chart)
