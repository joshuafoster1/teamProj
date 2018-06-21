from django.conf.urls import url
from django.contrib import admin
from challenge import views


urlpatterns = [
    url(r'^home/$', views.home, name = 'challenge_home'),
    url(r'^list/$', views.categories, name = 'challenge_categories'),
    url(r'^category/(?P<category>[0-9a-zA-Z\ \-\(\)\'\.\+\,]+)/$', views.list, name='challenge_list'),
    url(r'^description/(?P<challenge>[0-9a-zA-Z\ \-\(\)\'\.\+\,]+)/(?P<category>[0-9a-zA-Z\ \-\(\)\'\.\+\,]+)/$', views.description, name='challenge_description'),
    url(r'^complete/(?P<name>[0-9a-zA-Z\ \-\(\)\'\.\+\,]+)/(?P<category>[0-9a-zA-Z\ \-\(\)\'\.\+\,]+)/$', views.complete, name='challenge_complete'),
    url(r'^remove/(?P<pk>\d+)/$', views.remove, name = 'challenge_remove'),
]
