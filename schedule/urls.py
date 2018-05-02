from django.conf.urls import url, include
from django.contrib import admin
from schedule import views

urlpatterns = [
    url(r'^practice/(?P<id>\d+)/$', views.practice_form, name='practice'),
    url(r'^home/$', views.practice_home, name='practice_home'),
    url(r'^practice/overview/$', views.practice_overview, name='practice_overview'),
    url(r'^protocol/(?P<protocol_type>[0-9a-zA-Z\ \-\(\)\']+)/$', views.protocol_home, name='protocol_display'),
    url(r'^protocol/execute/(?P<protocol>[0-9a-zA-Z\ \-\(\)\']+)/$', views.protocol, name='protocol'),
]
