from django.shortcuts import render, HttpResponseRedirect

from forms import UserCreateForm


def create_account(request):
  if request.method == 'POST':
    form = UserCreateForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/user/success')
  else:
    form = UserCreateForm()
  return render(request, 'user/create.html', {'form': form})
