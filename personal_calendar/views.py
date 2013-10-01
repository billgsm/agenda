#-*-coding: utf-8-*-
import json

from django.shortcuts import (render, HttpResponseRedirect,
    render_to_response, HttpResponse)
from django.contrib.auth.models import User
from django.forms import HiddenInput
from django.template.loader import render_to_string
from django.template import RequestContext

from forms import EventForm, Evenement_ParticipantForm
from models import Evenement, Evenement_Participant


def update_create(request, id=None):
  try:
    event = Evenement.objects.get(pk=id)
  except Evenement.DoesNotExist:
    pass
  if request.method == 'POST':
    try:
      form = EventForm(request.POST, instance=event)
    except NameError:
      form = EventForm(request.POST)
    if form.is_valid():
      event = form.save()
      return HttpResponseRedirect('/agenda/%i/details/' % event.pk)
  else:
    try:
      form = EventForm(instance=event)
    except NameError:
      form = EventForm()
  return render(request, 'personal_calendar/event/create.html',
                {'form': form})

def details(request, id):
  event = Evenement.objects.get(pk=id)
  if request.method == 'POST':
    form = Evenement_ParticipantForm(request.POST)
    if form.is_valid():
      form.save()
      if request.is_ajax():
        delete_form = render_to_string("personal_calendar/blocks/delete_form.html",
                                       {
                                         'delete_url': form.instance.delete_url(),
                                       },
                                       # Needed for the csrf_token
                                       RequestContext(request)
                                      )
        data = {'participant': form.instance.participant.username,
                'get_status_display': form.instance.get_status_display(),
                'delete_form': delete_form}
        return HttpResponse(json.dumps(data), mimetype="application/json")

      return HttpResponseRedirect('/agenda/%s/details/' % id)
  else:
    form = Evenement_ParticipantForm(initial={'evenement': event})
    participants = [user.pk for user in event.participants.all()]
    form.fields['participant'].queryset = User.objects.exclude(pk__in=participants)
    form.fields['evenement'].widget = HiddenInput()
  if request.is_ajax():
    return render_to_response('personal_calendar/blocks/participant_form.html',
                              {
                                'event': event,
                                'form': form
                              })
  return render(request, 'personal_calendar/event/details.html',
                {
                  'event': event,
                  'form': form
                })

def delete(request, id):
  if request.method == 'POST':
    event = Evenement.objects.get(pk=id)
    event.delete()
  return HttpResponseRedirect('/agenda/list/')

def delete_participant(request, id, participant):
  if request.method == 'POST':
    event = Evenement.objects.get(pk=id)
    participant = User.objects.get(pk=participant)
    to_delete = Evenement_Participant.objects.get(
        evenement=event,
        participant=participant,
        )
    to_delete.delete()
    if request.is_ajax():
      return HttpResponse('OK')
  return HttpResponseRedirect('/agenda/%s/details/' % id)

def liste(request):
  events = Evenement.objects.all()
  return render(request, 'personal_calendar/event/list.html',
                {"events": events})
