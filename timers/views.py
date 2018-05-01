# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.safestring import mark_safe

from django.shortcuts import render, get_object_or_404, redirect
from models import Hangboard, Timer, Interval
import json
# Create your views here.
def timer(request, timer):
    live_timer = Timer.objects.get(name=timer)

    return render(request, 'timers/timer_page.html', {'timer':mark_safe(live_timer.get_timer())})
def timer_home(request):
    timers = Timer.objects.filter(workout='hangboard')
    return render(request, 'timers/timer_home.html', {'timers': timers})
