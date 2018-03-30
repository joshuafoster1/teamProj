from django import forms
from .models import *
class CurrentSendForm(forms.ModelForm):
    class Meta:
        model = SendingLevel
        fields = ['boulder_onsight', 'boulder_redpoint', 'route_onsight', 'route_redpoint']

class FingerPowerForm(forms.ModelForm):
    class Meta:
        model = FingerPower
        fields = ['weight', 'time']
class FingerEnduranceForm(forms.ModelForm):
    class Meta:
        model = FingerEndurance
        fields = [ 'time', 'rung', 'feet_on']
class FingerMuscularEnduranceForm(forms.ModelForm):
    class Meta:
        model = FingerMuscularEndurance
        fields = ['time']

class PullAndSlapForm(forms.ModelForm):
    class Meta:
        model = PullAndSlap
        fields = ['height_right_hand', 'height_left_hand']

class MaxWeightPullUpForm(forms.ModelForm):
    class Meta:
        model = MaxWeightPullUp
        fields = ['weight', 'lateral']

class MaxPullUpsForm(forms.ModelForm):
    class Meta:
        model = MaxPullUps
        fields = ['repetitions', 'lateral']

class CampusPowerEnduranceForm(forms.ModelForm):
    class Meta:
        model = CampusPowerEndurance
        fields = ['moves', 'time', 'rung', 'feet_on']

class LateralCoreForm(forms.ModelForm):
    class Meta:
        model = LateralCore
        fields = ['distance_left_side', 'distance_right_side']
