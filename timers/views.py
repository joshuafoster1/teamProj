# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from models import Hangboard, Timer, Interval
import json
# Create your views here.
def timer(request, timer):
    live_timer = Timer.objects.get(name=timer).get_timer()

    return render(request, 'timers/timer_page.html', {'timer':live_timer})
def timer_home(request):

    return render(request, 'timers/timer_home.html')
