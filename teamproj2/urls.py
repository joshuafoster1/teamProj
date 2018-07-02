"""teamproj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from training import views
# from timers import views as timerViews
from accounts import views as accounts_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    # url(r'^createathlete/$', accounts_views.create_athlete, name='create_athlete,'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),

    url(r'^timer/', include('timers.urls')),
    url(r'^metrics/', include('metrics.urls')),
    url(r'^schedule/', include('schedule.urls')),
<<<<<<< HEAD
    url(r'^challenge/', include('challenge.urls')),
    url(r'^goals/', include('goals.urls')),
=======
    url(r'^chart/', include('charts.urls')),
    url(r'^challenge/', include('challenge.urls')),
>>>>>>> pandas

    url(r'^admin/', admin.site.urls),
    url(r'^AthletePage/$', views.athletePage, name='athletePage'),
    url(r'^AthleteMetrics/$', views.athleteMetrics, name='athleteMetrics'),

    url(r'^AthleteInfo/$', views.athleteInfo, name='athleteInfo'),
    url(r'^AthleteInfo/update/(?P<pk>\d+)/$', views.UpdateAthlete.as_view(), name='update_athleteInfo'),
    url(r'^AthleteInfo/update/Bday/(?P<pk>\d+)/$', views.UpdateAthleteBday.as_view(), name='update_athleteBdayInfo'),

    url(r'^AthletePage/new/$', views.newConditioning, name='newConditioning'),

    url(r'^ccform/add/$', views.coachNewConditioning, name='ccform'),

    url(r'^PinchBlocks/add/$', views.pinch_blocks, name='pinch_blocks'),
    url(r'^coachPinchBlocks/add/$', views.coach_pinch_blocks, name='coach_pinch_blocks'),


    url(r'^WeightedHangs/add/$', views.weighted_hangs, name='weighted_hangs'),
    url(r'^coachWeightedHangs/add/$', views.coach_weighted_hangs, name='coach_weighted_hangs'),

    url(r'^coachmaxconditioning/add/$', views.coach_max_conditioning, name='coach_max_conditioning'),
    url(r'^maxconditioning/add/$', views.max_conditioning, name='max_conditioning'),


    url(r'^schedule/$', views.practice_schedule, name='practice_schedule'),

    url(r'^exercise/description/(?P<exercise_name>[\w.@+-]+)$', views.exercise_description, name='exercise_description'),
]
