# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .models import Athlete, Session, Conditioning, RefCategory, RefExercise
from .forms import FullConditioningForm, ConditioningForm, AthleteConditioningForm
# Create your views here.
def get_user(request):
    pk = request.user.pk
    athlete = get_object_or_404(Athlete, user__pk=pk)
    return athlete

# splash page should present Team info link to schedule, usaclimbing, login
@login_required
def home(request):
    athlete = get_user(request)
    # pk = request.user.pk
    # athlete = get_object_or_404(Athlete, user__pk=pk)

    return render(request, 'home.html', {'athlete': athlete})

# Athlete home page. present recent conditioning, goals, sends, button to add conditioning
@login_required
def athletePage(request):
    athlete = get_user(request)
    sessions = Session.objects.filter(athlete=athlete).order_by('sessionDate') #.last()
    conditioning_set=[]
    for session in sessions:
        conditioning = Conditioning.objects.filter(setNum=1, session__athlete=athlete, session__sessionDate=session.sessionDate)#.order_by('session__sessionDate')
        conditioning_set.append(conditioning)
    conditioning_set =conditioning_set[-2:]
    conditioning_set.reverse()

    for item in conditioning_set:
        for thing in item:
            print thing
            avg = thing.exercise.get_avg()
            print avg
    date = datetime.date.today()
    return render(request, 'athlete_page.html', {'athlete': athlete, 'date': date, 'conditioning': conditioning_set})

# display athletes current information and provide links to change information if incorrect
@login_required
def athleteInfo(request):
    athlete = get_user(request)
    return render(request, 'athleteInfo.html', {'athlete': athlete})

# currently a universal form. should restrict view to coach and create another page for athlete add conditioning.
@login_required
def newConditioning(request):
    athlete = get_user(request)

    # modelform code below. saving for modelform exploration
    # CoreCategory = get_object_or_404(RefCategory, pk=3)
    # PushCategory = get_object_or_404(RefCategory, pk=1)
    # PullCategory = get_object_or_404(RefCategory, pk=2)
    # TriCategory = get_object_or_404(RefCategory, pk=4)

    date = datetime.date.today()

    if request.method == 'POST':
        form = AthleteConditioningForm(request.POST)
        # form = ConditioningForm(request.POST, categoryInit=category)
        if form.is_valid():
            conditioning = form #save(commit=False)
            # athlete = conditioning.cleaned_data['Athlete']
            coreObject = Conditioning()
            coreObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            coreObject.exercise = conditioning.cleaned_data['Core']
            coreObject.repetitions = conditioning.cleaned_data['Core_Reps']
            coreObject.setNum = conditioning.cleaned_data['Set']

            pullObject = Conditioning()
            pullObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            pullObject.exercise = conditioning.cleaned_data['Pulls']
            pullObject.repetitions = conditioning.cleaned_data['Pull_Reps']
            pullObject.setNum = conditioning.cleaned_data['Set']

            pushObject = Conditioning()
            pushObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            pushObject.exercise = conditioning.cleaned_data['Push']
            pushObject.repetitions = conditioning.cleaned_data['Push_Reps']
            pushObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject = Conditioning()
            TricepsObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            TricepsObject.exercise = conditioning.cleaned_data['Triceps']
            TricepsObject.repetitions = conditioning.cleaned_data['Tricep_Reps']
            TricepsObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject.save()
            pushObject.save()
            pullObject.save()
            coreObject.save()


            return redirect('athletePage')
    else:
        form = AthleteConditioningForm()
        # form = ConditioningForm(categoryInit=CoreCategory)
    return render(request, 'new_conditioning.html', {'athlete': athlete, 'form': form, 'date': date})

# def is_coach(user):
#     return user.group == 'Coach'
#
# @login_required
# @user_passes_test(is_coach)
def coachNewConditioning(request):
    athlete = get_object_or_404(Athlete, pk=1)

    # modelform code below. saving for modelform exploration
    # CoreCategory = get_object_or_404(RefCategory, pk=3)
    # PushCategory = get_object_or_404(RefCategory, pk=1)
    # PullCategory = get_object_or_404(RefCategory, pk=2)
    # TriCategory = get_object_or_404(RefCategory, pk=4)

    date = datetime.date.today()

    if request.method == 'POST':
        form = FullConditioningForm(request.POST)
        # form = ConditioningForm(request.POST, categoryInit=category)
        if form.is_valid():
            conditioning = form #save(commit=False)
            athlete = conditioning.cleaned_data['Athlete']
            coreObject = Conditioning()
            coreObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            coreObject.exercise = conditioning.cleaned_data['Core']
            coreObject.repetitions = conditioning.cleaned_data['Core_Reps']
            coreObject.setNum = conditioning.cleaned_data['Set']

            pullObject = Conditioning()
            pullObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            pullObject.exercise = conditioning.cleaned_data['Pulls']
            pullObject.repetitions = conditioning.cleaned_data['Pull_Reps']
            pullObject.setNum = conditioning.cleaned_data['Set']

            pushObject = Conditioning()
            pushObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            pushObject.exercise = conditioning.cleaned_data['Push']
            pushObject.repetitions = conditioning.cleaned_data['Push_Reps']
            pushObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject = Conditioning()
            TricepsObject.session, created = Session.objects.get_or_create(sessionDate=date,
                athlete=athlete)
            TricepsObject.exercise = conditioning.cleaned_data['Triceps']
            TricepsObject.repetitions = conditioning.cleaned_data['Tricep_Reps']
            TricepsObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject.save()
            pushObject.save()
            pullObject.save()
            coreObject.save()


            return redirect('ccform')
    else:
        form = FullConditioningForm()
        # form = ConditioningForm(categoryInit=CoreCategory)
    return render(request, 'coach_conditioning_entry.html', {'athlete': athlete, 'form': form, 'date': date})
@login_required
def new_pinch(request):
    athlete = get_user()
