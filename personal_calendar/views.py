#-*-coding: utf-8-*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms import HiddenInput

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
  return render(request, 'personal_calendar/event/create.html',
                {'form': form})

def update(request, id):
  event = Evenement.objects.get(pk=id)
  if request.method == 'POST':
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
      event = form.save()
      return HttpResponseRedirect('/agenda/%i/details/' % event.pk)
  else:
    form = EventForm(instance=event)
  return render(request, 'personal_calendar/event/create.html',
                {'form': form})

def details(request, id):
  event = Evenement.objects.get(pk=id)
  if request.method == 'POST':
    form = Evenement_ParticipantForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/agenda/%s/details/' % id)
  else:
    form = Evenement_ParticipantForm(initial={'evenement': event})
    participants = [user.pk for user in event.participants.all()]
    form.fields['participant'].queryset = User.objects.exclude(pk__in=participants)
    form.fields['evenement'].widget = HiddenInput()
  return render(request, 'personal_calendar/event/details.html',
      {
        'event': event,
        'form': form
      })

def delete_participant(request, id, participant):
  if request.method == 'POST':
    event = Evenement.objects.get(pk=id)
    participant = User.objects.get(pk=participant)
    to_delete = Evenement_Participant.objects.get(
        evenement=event,
        participant=participant,
        )
    to_delete.delete()
  return HttpResponseRedirect('/agenda/%s/details/' % id)

def delete(request, id):
  if request.method == 'POST':
    event = Evenement.objects.get(pk=id)
    event.delete()
  return HttpResponseRedirect('/agenda/list/')

def liste(request):
  events = Evenement.objects.all()
  return render(request, 'personal_calendar/event/list.html',
                {"events": events})
