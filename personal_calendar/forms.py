from django.forms import ModelForm
from personal_calendar.models import Evenement

class EventForm(ModelForm):
  class Meta:
    model = Evenement
    exclude = ('participants',)
