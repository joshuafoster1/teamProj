from django.shortcuts import render

# Create your views here.
def home(request):

    return render(request,
        'goals/home.html',
        {'test':'test'}
        )

def set_goals(request):

    return render(request,
        'goals/set_goals.html',
        {'test':'test'}
        )

def complete(request):

    return render(request,
        'goals/complete.html',
        {'test':'test'}
        )

def list(request):

    return render(request,
        'goals/list.html',
        {'test':'test'}
        )
