from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import MAXIMUM_PASSWORD_LENGTH
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class UserCreateForm(UserCreationForm):
  #email = forms.EmailField(required=True)
  password1 = forms.CharField(label=_("Password"),
      widget=forms.PasswordInput, max_length=MAXIMUM_PASSWORD_LENGTH)
  password2 = forms.CharField(label=_("Password confirmation"),
      widget=forms.PasswordInput,
      max_length=MAXIMUM_PASSWORD_LENGTH,
      help_text=_("Enter the same password as above, for verification."))
  class Meta:
    model = User
    fields = ('username', 'email',)

  #def save(self, commit=True):
  #  user = super(UserCreateForm, self).save(commit=True)
  #  user.email = self.cleaned_data['email']
  #  if commit:
  #    user.save()
  #  return user
