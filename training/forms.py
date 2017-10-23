from django.forms import inlineformset_factory
from django import forms
from .models import Conditioning, RefExercise, Athlete, PinchBlocks, WeightedHangs
class AthleteConditioningForm(forms.Form):
    Pulls = forms.ModelChoiceField(queryset=RefExercise.objects.filter(category__id=1))
    Pull_Reps = forms.IntegerField(min_value=1, max_value=12)
    Core = forms.ModelChoiceField(queryset=None)
    Core_Reps = forms.IntegerField(min_value=1, max_value=12)
    Push = forms.ModelChoiceField(queryset=None)
    Push_Reps = forms.IntegerField(min_value=1, max_value=12)
    Triceps = forms.ModelChoiceField(queryset=None)
    Tricep_Reps = forms.IntegerField(min_value=1, max_value=12)
    Set = forms.IntegerField(min_value=1, max_value=3)

    def __init__(self, *args, **kwargs):
        super(AthleteConditioningForm, self).__init__(*args, **kwargs)
        # self.fields['Pulls'].queryset =RefExercise.objects.filter(category__id=1)
        self.fields['Core'].queryset =RefExercise.objects.filter(category__id=3)
        self.fields['Push'].queryset =RefExercise.objects.filter(category__id=2)
        self.fields['Triceps'].queryset =RefExercise.objects.filter(category__id=4)

class FullConditioningForm(AthleteConditioningForm):
    Athlete = forms.ModelChoiceField(queryset=Athlete.objects.all())

    def __init__(self, *args, **kwargs):
        super(FullConditioningForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['Athlete', ]

class ConditioningForm(forms.ModelForm):
    # category_choices = RefExercise.objects.get(category__id=1)
    #
    # creator = forms.ChoiceField(required=True, label='Project creator', choices=category_choices)
    class Meta:
        model = Conditioning
        fields = ['repetitions', 'setNum', 'exercise']

    z = 2
    def __init__(self, *args, **kwargs):
        print('start')
        categoryInit = kwargs.pop('categoryInit') # the kargs.pop takes the argument from theviews function and passes it into the from here
        super(ConditioningForm, self).__init__(*args, **kwargs)
        x = RefExercise.objects.filter(category=categoryInit)#id=self.z)
        self.fields['exercise'].queryset = x


class PinchBlockForm(forms.ModelForm):
    class Meta:
        model = PinchBlocks
        fields = ['block', 'seconds']

class WeightedHangsForm(forms.ModelForm):
    class Meta:
        model = WeightedHangs
        fields = ['rung', 'seconds']
