from django import forms
from .models import *

class FingerPowerForm(forms.ModelForm):
    class Meta:
        model = FingerPower
        fields = ['weight', 'time']
class FingerEnduranceForm(forms.ModelForm):
    class Meta:
        model = FingerEndurance
        fields = ['weight', 'time']
class FingerMuscularEnduranceForm(forms.ModelForm):
    class Meta:
        model = FingerMuscularEndurance
        fields = ['weight', 'time']

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
        fields = ['moves', 'time']

class LateralCoreForm(forms.ModelForm):
    class Meta:
        model = LateralCore
        fields = ['distance_left_side', 'distance_right_side']
