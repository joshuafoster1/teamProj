from django import forms
from .models import *
class BoulderingRoutineMetricsForm(forms.ModelForm):
    class Meta:
        model = BoulderingRoutineMetrics
        fields = ['total_points', 'total_climbs', 'max', 'min']

class RopeRoutineMetricsForm(forms.ModelForm):
    class Meta:
        model = BoulderingRoutineMetrics
        fields = ['total_climbs', 'max', 'min']
