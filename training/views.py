# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Athlete, Session, Conditioning, RefCategory, RefExercise
from .forms import FullConditioningForm, ConditioningForm
# Create your views here.


def home(request):
    athletes = Athlete.objects.all()

    return render(request, 'home.html', {'athletes': athletes})

def athletePage(request, pk):
    athlete = get_object_or_404(Athlete, pk=pk)
    athletes = Athlete.objects.all()
    conditioning = Conditioning.objects.all()
    total = conditioning.count()-1
    recent_conditioning = conditioning[total:]
    date = datetime.date.today()

    return render(request, 'athlete_page.html', {'athlete': athlete, 'date': date, 'conditioning': recent_conditioning, 'athletes': athletes})

def athleteInfo(request, pk):
    athlete = get_object_or_404(Athlete, pk=pk)
    return render(request, 'athleteInfo.html', {'athlete': athlete})

def newConditioning(request, pk):
    athlete = get_object_or_404(Athlete, pk=pk)

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
            # conditioning.athlete = athlete
            # conditioning.session, created = Session.objects.get_or_create(sessionDate=date,
                # athlete=athlete
            # )
            # conditioning.save()

            return redirect('athletePage', pk=athlete.id)
    # session, created = Session.objects.get_or_create(sessionDate=date, athlete=athlete)
    else:
        form = FullConditioningForm()
        # form = ConditioningForm(categoryInit=CoreCategory)
    return render(request, 'new_conditioning.html', {'athlete': athlete, 'form': form, 'date': date})
