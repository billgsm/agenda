from django.forms import ModelForm, HiddenInput
from django.contrib.auth.models import User

from models import Invitation, Contact, Circle, UserInfo

class InvitationForm(ModelForm):
  class Meta:
    model = Invitation
    exclude = ('sender',)

class CircleForm(ModelForm):
  class Meta:
    model = Circle
    exclude = ('owner',)

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('optional_informations',)

class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
