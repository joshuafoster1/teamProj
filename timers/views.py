# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from models import Hangboard
import json
# Create your views here.
def timer(request):

    hangboard = get_object_or_404(Hangboard, name='Punch')
    print(hangboard.time_intervals)
    time = hangboard.time_intervals
    print(time)
    activity = hangboard.activity_intervals
    print(activity)
    return render(request, 'timers/timer_page.html', {'time':time, 'activity':activity})
def timer_home(request):
    return render(request, 'timers/timer_home.html')
