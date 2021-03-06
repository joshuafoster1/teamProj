from django import forms
from .models import *
from django.apps import apps


class BoulderingRoutineMetricsForm(forms.ModelForm):
    class Meta:
        model = BoulderingRoutineMetrics
        fields = ['total_points', 'total_climbs', 'max', 'min']
        widgets = {
            'total_points': forms.NumberInput(attrs={
                'id': 'total_points',
                'required': True,
                'placeholder': 'Total'}),
            'total_climbs': forms.NumberInput(attrs={
                'id': 'total_climbs',
                'required': True,
                'placeholder': 'Total Points'
            }),

        }


class RopeRoutineMetricsForm(forms.ModelForm):
    class Meta:
        model = RopeRoutineMetrics
        fields = ['total_climbs', 'max', 'min']

class HangboardMetrics(forms.ModelForm):
    class Meta:
        model = HangboardMetrics
        fields = ['complete']

class Top3RopeSendsForm(forms.ModelForm):
    class Meta:
        model = Top3RopeSends
        fields = ['send_1', 'send_2', 'send_3']

class Top3BoulderSendsForm(forms.ModelForm):
    class Meta:
        model = Top3BoulderSends
        fields = ['send_1', 'send_2', 'send_3']

class RouteRedpointForm(forms.ModelForm):
    class Meta:
        model = RouteRedpoint
        fields = ['grade', 'sent']

class BoulderRedpointForm(forms.ModelForm):
    class Meta:
        model = BoulderRedpoint
        fields = ['grade', 'sent']

class BaseBoulderingFormset(forms.BaseModelFormSet):
     def __init__(self, *args, **kwargs):
        super(BaseBoulderingFormset, self).__init__(*args, **kwargs)
        self.queryset = BoulderingRoutineMetrics.objects.none()

class BaseRouteRedpointFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseRouteRedpointFormset, self).__init__(*args, **kwargs)
        self.queryset = RouteRedpoint.objects.none()

class BaseBoulderRedpointFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseBoulderRedpointFormset, self).__init__(*args, **kwargs)
        self.queryset = BoulderRedpoint.objects.none()

class BoulderProjectForm(forms.ModelForm):
    class Meta:
        model = BoulderProjectMetrics
        fields = ['name', 'grade', 'number_of_moves', 'moves_completed', 'sent']

class RouteProjectForm(forms.ModelForm):
    class Meta:
        model = RouteProjectMetrics
        fields = ['name', 'grade', 'hangs', 'top', 'sent']

BoulderingFormset = forms.modelformset_factory(BoulderingRoutineMetrics, form = BoulderingRoutineMetricsForm, formset = BaseBoulderingFormset, extra = 6)
RouteRedpointFormset = forms.modelformset_factory(RouteRedpoint, form = RouteRedpointForm, formset = BaseRouteRedpointFormset, extra = 6)
BoulderRedpointFormset = forms.modelformset_factory(BoulderRedpoint, form = BoulderRedpointForm, formset = BaseBoulderRedpointFormset, extra = 6)
