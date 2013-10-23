from django.forms import ModelForm, HiddenInput
from django.contrib.auth.models import User

from models import Invitation

class InvitationForm(ModelForm):
  class Meta:
    model = Invitation
    exclude = ('sender',)
