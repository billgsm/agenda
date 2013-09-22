from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponseRedirect


def create_account(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/user/success')
  else:
    form = UserCreationForm()
  return render(request, 'user/create.html', {'form': form})
