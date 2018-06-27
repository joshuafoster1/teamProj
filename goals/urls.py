from django.conf.urls import url
from goals import views
urlpatterns = [
    url(r'^home/$', views.home, name = 'goals_home'),
    url(r'^set/$', views.set_goals, name = 'set_goals')
    url(r'^complete/$', views.complete, name = 'complete_goal'),
    url(r'^list/$'. views.list, name='list_goals'),
]
