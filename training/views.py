# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .models import * #Athlete, Session, Conditioning, RefCategory, RefExercise, WeightedHangs, PinchBlocks
from .forms import FullConditioningForm, ConditioningForm, AthleteConditioningForm, PinchBlockForm, WeightedHangsForm, FullPinchBlockForm, FullWeightedHangsForm

#view globals
CATEGORY_ID = {'pulls':1, 'core':3, 'push':2, 'triceps':4}
DATE = datetime.date.today()

#view helper function(s)
def get_user(request):
    pk = request.user.pk
    athlete = get_object_or_404(Athlete, user__pk=pk)
    return athlete


###Views
# splash page should present Team info link to schedule, usaclimbing, login
@login_required
def home(request):
    athlete = get_user(request)

    return render(request, 'home.html', {'athlete': athlete})

# Athlete home page. present recent conditioning, goals, sends, button to add conditioning
@login_required
def athletePage(request):
    athlete = get_user(request)

    conditioning_set = athlete.return_recent_conditioning()

    hangs = ['No']
    str_hangs = ['this']
    lock_hangs = ['that']
    offset_hangs = ['those']
    return render(request, 'athlete_page.html', {'athlete': athlete, 'date': DATE, 'conditioning': conditioning_set, 'str_hangs': str_hangs, 'lock_hangs': lock_hangs, 'offset_hangs': offset_hangs, 'hangs': hangs})

# display athletes current information and provide links to change information if incorrect
@login_required
def athleteInfo(request):
    athlete = get_user(request)
    info = athlete.get_user_info()

    return render(request, 'athleteInfo.html', {'athlete': athlete, 'info': info})

# currently a universal form. should restrict view to coach and create another page for athlete add conditioning.
@login_required
def newConditioning(request):
    athlete = get_user(request)

    # retrive last exercise from prior session to prepopulate form
    pulls = RefCategory.objects.get(pk=CATEGORY_ID['pulls']).get_last_exercise(athlete)
    core = RefCategory.objects.get(pk=CATEGORY_ID['core']).get_last_exercise(athlete)
    push = RefCategory.objects.get(pk=CATEGORY_ID['push']).get_last_exercise(athlete)
    triceps = RefCategory.objects.get(pk=CATEGORY_ID['triceps']).get_last_exercise(athlete)

    # date = datetime.date.today()

    if request.method == 'POST':
        form = AthleteConditioningForm(request.POST)
        if form.is_valid():
            conditioning = form
            coreObject = Conditioning()
            coreObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            coreObject.exercise = conditioning.cleaned_data['Core']
            coreObject.repetitions = conditioning.cleaned_data['Core_Reps']
            coreObject.setNum = conditioning.cleaned_data['Set']

            pullObject = Conditioning()
            pullObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pullObject.exercise = conditioning.cleaned_data['Pulls']
            pullObject.repetitions = conditioning.cleaned_data['Pull_Reps']
            pullObject.setNum = conditioning.cleaned_data['Set']

            pushObject = Conditioning()
            pushObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pushObject.exercise = conditioning.cleaned_data['Push']
            pushObject.repetitions = conditioning.cleaned_data['Push_Reps']
            pushObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject = Conditioning()
            TricepsObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
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
        form = AthleteConditioningForm(initial={'Pulls': pulls, 'Core': core, 'Push': push, 'Triceps': triceps })
        # form = ConditioningForm(categoryInit=CoreCategory)
    return render(request, 'new_conditioning.html', {'athlete': athlete, 'form': form, 'date': DATE})

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

    # date = datetime.date.today()

    if request.method == 'POST':
        form = FullConditioningForm(request.POST)
        # form = ConditioningForm(request.POST, categoryInit=category)
        if form.is_valid():
            conditioning = form #save(commit=False)
            athlete = conditioning.cleaned_data['Athlete']
            coreObject = Conditioning()
            coreObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            coreObject.exercise = conditioning.cleaned_data['Core']
            coreObject.repetitions = conditioning.cleaned_data['Core_Reps']
            coreObject.setNum = conditioning.cleaned_data['Set']

            pullObject = Conditioning()
            pullObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pullObject.exercise = conditioning.cleaned_data['Pulls']
            pullObject.repetitions = conditioning.cleaned_data['Pull_Reps']
            pullObject.setNum = conditioning.cleaned_data['Set']

            pushObject = Conditioning()
            pushObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pushObject.exercise = conditioning.cleaned_data['Push']
            pushObject.repetitions = conditioning.cleaned_data['Push_Reps']
            pushObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject = Conditioning()
            TricepsObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
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
    return render(request, 'coach_conditioning_entry.html', {'athlete': athlete, 'form': form, 'date': DATE})

@login_required
def pinch_blocks(request):
    athlete = get_user(request)
    if request.method == 'POST':
        form = PinchBlockForm(request.POST)
        if form.is_valid():
            pinch_training = form.save(commit=False)
            pinch_training.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pinch_training.save()
            return redirect('pinch_blocks')
    else:
        form = PinchBlockForm()
    return render(request, 'add_pinch_blocks.html', {'athlete':athlete, 'form': form, 'date': DATE})


def coach_pinch_blocks(request):

    if request.method == 'POST':
        form = FullPinchBlockForm(request.POST)
        if form.is_valid():
            pinch_training = form
            athlete = pinch_training.cleaned_data['Athlete']
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            today = PinchBlocks()
            today.pinch = pinch_training.cleaned_data['pinch']
            today.seconds = pinch_training.cleaned_data['seconds']
            today.weight = pinch_training.cleaned_data['weight']
            today.session = session
            today.save()
            return redirect('coach_pinch_blocks')
    else:
        form = FullPinchBlockForm()
    return render(request, 'add_pinch_blocks.html', {'form': form, 'date':DATE})

@login_required
def weighted_hangs(request):
    athlete = get_user(request)
    if request.method == 'POST':
        form = WeightedHangsForm(request.POST)
        if form.is_valid():
            weighted_hang = form.save(commit=False)
            weighted_hang.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            weighted_hang.save()
            return redirect('weighted_hangs')
    else:
        form = WeightedHangsForm()
    return render(request, 'add_weighted_hangs.html', {'athlete':athlete, 'form': form, 'date': DATE})

def coach_weighted_hangs(request):

    if request.method == 'POST':
        form = FullWeightedHangsForm(request.POST)
        if form.is_valid():
            hang_form = form#.save(commit=False)
            athlete = hang_form.cleaned_data['Athlete']
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            today = WeightedHangs()
            today.hang = hang_form.cleaned_data['hang']
            today.seconds = hang_form.cleaned_data['seconds']
            today.weight = hang_form.cleaned_data['weight']
            today.session = session
            today.save()
            return redirect('coach_weighted_hangs')
    else:
        form = FullWeightedHangsForm()
    return render(request, 'add_weighted_hangs.html', {'form': form, 'date':DATE})

def coach_max_conditioning(request):
    if request.method == 'POST':
        form = FullMaxConditioningForm(request.POST)
        if form.is_valid():
            max_form = form#.save(commit=False)
            athlete = max_form.cleaned_data['Athlete']
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            today = MaxConditioning()
            today.hang = hang_form.cleaned_data['hang']
            today.seconds = hang_form.cleaned_data['seconds']
            today.weight = hang_form.cleaned_data['weight']
            today.session = session
            today.save()
            return redirect('coach_weighted_hangs')
    else:
        form = FullWeightedHangsForm()
    return render(request, 'add_weighted_hangs.html', {'form': form, 'date': DATE})
