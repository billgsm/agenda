#-*-coding: utf-8-*-
from django.shortcuts import render, HttpResponseRedirect

from forms import EventForm, Evenement_ParticipantForm
from models import Evenement, Evenement_Participant


def create(request):
  if request.method == 'POST':
    form = EventForm(request.POST)
    if form.is_valid():
      event = form.save()
      return HttpResponseRedirect('/agenda/%i/details/' % event.pk)
  else:
    form = EventForm()
  return render(request, 'personal_calendar/event/create.html', {'form': form})

def details(request, id):
  if request.method == 'POST':
    form = Evenement_ParticipantForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/event/%s/details/' % id)
  else:
    form = Evenement_ParticipantForm()
  event = Evenement.objects.get(pk=id)
  return render(request, 'personal_calendar/event/details.html',
      {
        'event': event,
        'form': form
      })
