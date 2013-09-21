#-*-coding: utf-8-*-
from django.shortcuts import render, HttpResponseRedirect

from forms import EventForm
from models import Evenement


def create(request):
  if request.method == 'POST':
    if request.POST:
      form = EventForm(request.POST)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/agenda/create/')
  else:
    form = EventForm()
  return render(request, 'personal_calendar/event/create.html', {'form': form})

def details(request, id):
  event = Evenement.objects.get(pk=id)
  return render(request, 'personal_calendar/event/detail.html', {'event': event})
