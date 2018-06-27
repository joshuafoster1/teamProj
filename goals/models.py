from django.db import models
from training.models import Athlete, DATE

# Create your models here.
class Goal(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='goals')
    set_date = models.DateField(auto_now=True)
    due_date = models.DateField()
    completed = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200)
