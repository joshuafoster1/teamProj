# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from .models import *
from .tables import *
# Create your views here.
def categories(request):
    athlete = Athlete.objects.get(user = request.user)

    categories = Category.objects.all()
    athChall = AthleteChallenge.objects.values('challenge__category__name').filter(athlete = athlete).annotate(num=models.Count('challenge'))
    table = CategoryCountTable(athChall)
    RequestConfig(request).configure(table)
    return render(request,
        'challenge/categories.html',
        {'categories':categories, 'table':table})


def home(request):
    athlete = Athlete.objects.get(user = request.user)
    challenges = AthleteChallenge.objects.filter(athlete=athlete)

    return render(request,
        'challenge/home.html',
        {'challenges': challenges})


def list(request, category):
    athlete = Athlete.objects.get(user = request.user)

    challenges = Challenge.objects.filter(category__name=category)
    athChall = AthleteChallenge.objects.filter(challenge__category__name = category, athlete=athlete)
    table = ChallengeCategoryTable(athChall)
    RequestConfig(request).configure(table)

    return render(request,
        'challenge/list_display.html',
        {'challenges': challenges, 'category': category, 'table': table})


def description(request, challenge, category):
    challenge = Challenge.objects.get(name = challenge, category__name=category)
    description = challenge.description
    category = challenge.category.name
    return render(request,
        'challenge/detail.html',
        {'description': description, 'name': challenge, 'category': category})


def complete(request, name, category):
    athlete = Athlete.objects.get(user = request.user)
    challenge = Challenge.objects.get(name=name, category__name=category)
    AthleteChallenge.objects.add_challenge(athlete, challenge)

    return redirect('challenge_categories')

def remove(request, pk):
    obj = AthleteChallenge.objects.get(pk = pk)
    category = obj.challenge.category.name
    obj.delete()

    return redirect('challenge_list', category=category)
