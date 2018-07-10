# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime, random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .models import * #Athlete, Session, Conditioning, RefCategory, RefExercise, WeightedHangs, PinchBlocks
from .forms import CoachMaxConditioningForm, MaxConditioningForm, FullConditioningForm, AthleteConditioningForm, PinchBlockForm, WeightedHangsForm, FullPinchBlockForm, FullWeightedHangsForm
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

import logging

def debugging(date, athlete):
    logging.debug('; Date: %s, Athlete: %s', date, athlete)

logging.basicConfig(format='%(asctime)s %(message)s', filename= 'debug.log', filemode='a', level=logging.DEBUG)


#view globals
CATEGORY_ID = {'pulls':1, 'core':3, 'push':2, 'triceps':4}
DATE = datetime.date.today()
quote_num = ClimbingQuotes.objects.count()

#view helper function(s)
def get_user(request):
    user = request.user
    athlete = get_object_or_404(Athlete, user=user)
    return athlete

def is_coach(user):
    return user.groups.filter(name='Coach').exists()

def standard_content(request):
    '''base contents: date, athlete, quote'''

    return {'date': DATE, 'athlete': get_user(request), 'quote': ClimbingQuotes.objects.get(id=random.randint(1, quote_num))}

###Views
@login_required
def home(request):
    """# home page link to schedule, usaclimbing, show events"""
    content = standard_content(request)
    calendar_objs = Calendar.objects.all()

    # populate upcoming events
    calendar = []
    for item in calendar_objs:
        if item.is_valid(DATE):
            calendar.append(item)

    content['calendar'] = calendar

    return render(request, 'home.html', content)


@login_required
def athletePage(request):
    """ Page for conditioning, pinch blocks and weighted hangs"""

    content = standard_content(request)
    athlete = content['athlete']

    # compile conditioning
    conditioning = []
    for key in CATEGORY_ID:
        exercise_obj = athlete.get_conditioning(CATEGORY_ID[key], True)

        if exercise_obj is not None:
            conditioning.append(exercise_obj)

    content['weighted_hangs'] = athlete.get_weighted_training(WeightedHangs)
    content['pinch_training'] = athlete.get_weighted_training(PinchBlocks)
    content['max_weighted_hangs'] = athlete.get_weighted_training(WeightedHangs, max_weight=True)
    content['max_weighted_pinch'] = athlete.get_weighted_training(PinchBlocks, max_weight=True)
    content['conditioning'] = conditioning

    return render(request, 'athlete_page.html', content)

# display athletes current information and provide links to change information if incorrect
@login_required
def athleteInfo(request):
    """ Content for athlete information page (template links to update for birthdate and info)"""

    content = standard_content(request)
    content['info'] = content['athlete'].get_user_info()

    return render(request, 'athleteInfo.html', content)

class UpdateAthleteBday(UpdateView):
    model = Athlete
    fields = ['birthdate']
    template_name = 'update_athlete.html'
    success_url = reverse_lazy('athleteInfo')

class UpdateAthlete(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'update_athlete.html'
    success_url = reverse_lazy('athleteInfo')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def newConditioning(request):
    content = standard_content(request)
    athlete = content['athlete']

    # retrive last exercise from prior session to prepopulate form
    pulls = RefCategory.objects.get(pk=CATEGORY_ID['pulls']).get_last_exercise(athlete)
    core = RefCategory.objects.get(pk=CATEGORY_ID['core']).get_last_exercise(athlete)
    push = RefCategory.objects.get(pk=CATEGORY_ID['push']).get_last_exercise(athlete)
    triceps = RefCategory.objects.get(pk=CATEGORY_ID['triceps']).get_last_exercise(athlete)

    if request.method == 'POST':
        form = AthleteConditioningForm(request.POST)
        if form.is_valid():
            conditioning = form
            coreObject = Conditioning()
            debugging(DATE, athlete)
            coreObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            coreObject.exercise = conditioning.cleaned_data['Core']
            coreObject.repetitions = conditioning.cleaned_data['Core_Reps']
            coreObject.setNum = conditioning.cleaned_data['Set']

            pullObject = Conditioning()
            debugging(DATE, athlete)
            pullObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pullObject.exercise = conditioning.cleaned_data['Pulls']
            pullObject.repetitions = conditioning.cleaned_data['Pull_Reps']
            pullObject.setNum = conditioning.cleaned_data['Set']

            pushObject = Conditioning()
            debugging(DATE, athlete)
            pushObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pushObject.exercise = conditioning.cleaned_data['Push']
            pushObject.repetitions = conditioning.cleaned_data['Push_Reps']
            pushObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject = Conditioning()
            debugging(DATE, athlete)
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
        content['form'] = AthleteConditioningForm(initial={'Pulls': pulls, 'Core': core, 'Push': push,
                'Triceps': triceps })

    return render(request, 'new_conditioning.html', content)


@login_required
@user_passes_test(is_coach)
def coachNewConditioning(request):
    content = standard_content(request)
    athlete = get_object_or_404(Athlete, pk=1)


    if request.method == 'POST':
        form = FullConditioningForm(request.POST)
        if form.is_valid():
            conditioning = form #save(commit=False)
            athlete = conditioning.cleaned_data['Athlete']
            coreObject = Conditioning()
            debugging(DATE, athlete)
            coreObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            coreObject.exercise = conditioning.cleaned_data['Core']
            coreObject.repetitions = conditioning.cleaned_data['Core_Reps']
            coreObject.setNum = conditioning.cleaned_data['Set']

            pullObject = Conditioning()
            debugging(DATE, athlete)
            pullObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pullObject.exercise = conditioning.cleaned_data['Pulls']
            pullObject.repetitions = conditioning.cleaned_data['Pull_Reps']
            pullObject.setNum = conditioning.cleaned_data['Set']

            pushObject = Conditioning()
            debugging(DATE, athlete)
            pushObject.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pushObject.exercise = conditioning.cleaned_data['Push']
            pushObject.repetitions = conditioning.cleaned_data['Push_Reps']
            pushObject.setNum = conditioning.cleaned_data['Set']

            TricepsObject = Conditioning()
            debugging(DATE, athlete)
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
        content['form'] = FullConditioningForm()

    return render(request, 'coach_conditioning_entry.html', content)

@login_required
def pinch_blocks(request):
    athlete = get_user(request)
    content = standard_content(request)

    if request.method == 'POST':
        form = PinchBlockForm(request.POST)
        if form.is_valid():
            pinch_training = form.save(commit=False)
            debugging(DATE, athlete)
            pinch_training.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            pinch_training.save()
            return redirect('pinch_blocks')
    else:
        content['form'] = PinchBlockForm()

    content['pinch_training'] = athlete.get_weighted_training(PinchBlocks)

    return render(request, 'training/add_pinch_blocks.html', content)

@login_required
@user_passes_test(is_coach)
def coach_pinch_blocks(request):
    content = standard_content(request)

    if request.method == 'POST':
        form = FullPinchBlockForm(request.POST)
        if form.is_valid():
            pinch_training = form
            athlete = pinch_training.cleaned_data['Athlete']
            debugging(DATE, athlete)
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
        content['form'] = FullPinchBlockForm()

    return render(request, 'training/add_pinch_blocks.html', content)

@login_required
def weighted_hangs(request):
    content = standard_content(request)
    athlete = get_user(request)

    if request.method == 'POST':
        form = WeightedHangsForm(request.POST)
        if form.is_valid():
            weighted_hang = form.save(commit=False)
            debugging(DATE, athlete)
            weighted_hang.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            weighted_hang.save()
            return redirect('weighted_hangs')
    else:
        content['form'] = WeightedHangsForm()

    content['weighted_hangs'] = athlete.get_weighted_training(WeightedHangs)

    return render(request, 'training/add_weighted_hangs.html', content)

@login_required
@user_passes_test(is_coach)
def coach_weighted_hangs(request):
    contenet = standard_content(request)

    if request.method == 'POST':
        form = FullWeightedHangsForm(request.POST)
        if form.is_valid():
            hang_form = form#.save(commit=False)
            athlete = hang_form.cleaned_data['Athlete']
            debugging(DATE, athlete)
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
        content['form'] = FullWeightedHangsForm()
    return render(request, 'training/add_weighted_hangs.html', content)

@login_required
def max_conditioning(request):
    content = standard_content(request)
    athlete = get_user(request)
    if request.method == 'POST':
        form = MaxConditioningForm(request.POST)
        if form.is_valid():
            max_conditioning = form.save(commit=False)
            debugging(DATE, athlete)
            max_conditioning.session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            max_conditioning.save()
            return redirect('max_conditioning')
    else:
        content['form'] = MaxConditioningForm()
    return render(request, 'training/add_max_conditioning.html', content)

@login_required
def athleteMetrics(request):
    content = standard_content(request)
    return render(request, 'athlete_metrics.html', content)

@login_required
@user_passes_test(is_coach)
def coach_max_conditioning(request):
    content = standard_content(request)
    if request.method == 'POST':
        form = CoachMaxConditioningForm(request.POST)
        if form.is_valid():
            max_form = form#.save(commit=False)
            athlete = max_form.cleaned_data['Athlete']
            debugging(DATE, athlete)
            session, created = Session.objects.get_or_create(sessionDate=DATE,
                athlete=athlete)
            today = MaxConditioning()
            today.exercise = max_form.cleaned_data['exercise']
            today.repetitions = max_form.cleaned_data['repetitions']
            today.session = session
            today.save()
            return redirect('coach_max_conditioning')
    else:
        content['form'] = CoachMaxConditioningForm()
    return render(request, 'training/add_max_conditioning.html', content)

@login_required
def practice_schedule(request):
    content = standard_content(request)
    athlete = get_user(request)
    content['practice'] = Practice.objects.all()
    content['assigned_practice'] = athlete.get_assigned_practice()

    return render(request, 'practice_schedule.html', content)

@login_required
def exercise_description(request, exercise_name):
    content = standard_content(request)
    content['exercise'] = get_object_or_404(RefExercise, pk=exercise_name)
    return render(request, 'exercise_description.html', content)
