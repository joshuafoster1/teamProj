import django_tables2 as tables
from .models import *
from django_tables2.utils import A


class EvalTable(tables.Table):
    # remove = tables.LinkColumn('metric_remove', text='Remove', args=[A('pk')], orderable=False, empty_values=(), attrs={'td':{"class": "btn"}})
    date = tables.Column()
    class Meta:
        template_name = 'django_tables2/bootstrap-responsive.html'
