from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserCreateForm(UserCreationForm):
  email = forms.EmailField(required=True)

  def save(self, commit=True):
    user = super(UserCreateForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
      user.save()
    return user
