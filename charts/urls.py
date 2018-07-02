from django.conf.urls import url, include
from django.contrib import admin
from schedule import views

urlpatterns = [
    url(r'^practice/(?P<id>\d+)/$', views.practice_form, name='practice'),
    url(r'^home/$', views.practice_home, name='practice_home'),
    url(r'^practice/overview/$', views.practice_overview, name='practice_overview'),
    url(r'^protocol/execute/(?P<protocol>[0-9a-zA-Z\ \-\(\)\']+)/$', views.protocol, name='protocol'),
    url(r'^protocol/summary/$', views.protocol_summary, name='protocol_summary'),
    url(r'^protocol/chart_data/$', views.chart_data, name='chart_data'),
    url(r'^protocol/json/$', views.json_example, name='json_example'),
    url(r'^protocol/(?P<protocol_type>[0-9a-zA-Z\ \-\(\)\']+)/$', views.protocol_home, name='protocol_display'),



]
