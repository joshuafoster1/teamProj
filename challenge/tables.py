import django_tables2 as tables
from .models import *
from django_tables2.utils import A


class ChallengeCategoryTable(tables.Table):
    remove = tables.LinkColumn('challenge_remove', text='Remove', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})

    class Meta:
        model = AthleteChallenge
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ['challenge', 'date']
