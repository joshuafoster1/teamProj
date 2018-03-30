from django.conf.urls import url
from metrics import views
urlpatterns = [
        url(r'^metrictest/(?P<metricform>[\w \-]+)/$', views.metric_test, name='metric_test'),
        url(r'^evaluation/$', views.evaluation, name='evaluation'),
        url(r'^evaluation/summary/$', views.eval_summary, name='eval_summary')
]
