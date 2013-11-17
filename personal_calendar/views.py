#-*-coding: utf-8-*-
import json
import datetime

from django.shortcuts import (render, HttpResponseRedirect,
    render_to_response, HttpResponse)
from django.contrib.auth.models import User
from django.forms import HiddenInput
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from forms import EventForm, Evenement_ParticipantForm
from models import Evenement, Evenement_Participant


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
      #################### regenerate the form with the right remaining participants
      updated_form = Evenement_ParticipantForm(initial={'evenement': event})
      create_form_updated = render_to_string("personal_calendar/blocks/participant_form.html",
                                     {
                                       'form': updated_form,
                                     },
                                     # Needed for the csrf_token
                                     RequestContext(request)
                                    )
      #################### END
      data = {'ack': 'OK',
              'form': create_form_updated}
      return HttpResponse(json.dumps(data), mimetype="application/json")
  return HttpResponseRedirect('/agenda/%s/detail/' % id)

class Evenement_Detail(DetailView):
  model = Evenement

  def get_context_data(self, **kwargs):
    print self.request.user.username
    context = super(Evenement_Detail, self).get_context_data(**kwargs)
    form = Evenement_ParticipantForm(initial={'evenement': self.object})
    context['form'] = form
    return context

  def post(self, request, *args, **kwargs):
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
        #################### regenerate the form with the right remaining participants
        updated_form = Evenement_ParticipantForm(initial=
            {
              'evenement': form.instance.evenement
            })
        create_form_updated = render_to_string("personal_calendar/blocks/participant_form.html",
                                       {
                                         'form': updated_form,
                                       },
                                       # Needed for the csrf_token
                                       RequestContext(request)
                                      )
        #################### regenerate the form with the right remaining participants
        data = {'participant': form.instance.participant.username,
                'get_status_display': form.instance.get_status_display(),
                'delete_form': delete_form,
                'form': create_form_updated}
        return HttpResponse(json.dumps(data), mimetype="application/json")
      else:
        # Not ajax
        return HttpResponseRedirect('/agenda/{0}/detail/'.format(form.instance.evenement.id))
    else:
      # Form invalid
      if request.is_ajax():
        return render(request, 'personal_calendar/blocks/participant_form.html',
            {
              'event': form.instance.evenement,
              'form': form
            })
      else:
        return render(request, 'personal_calendar/event/detail.html',
            {
              'event': form.instance.evenement,
              'form': form
            })

class Evenement_List(ListView):

  def get_queryset(self):
    print self.request.user
    #events = Evenement.objects.filter(participants=self.request.user.id,
    #    date__gte=datetime.datetime.now())
    events = Evenement.objects.filter(participants=self.request.user.id)
    if 'field' in self.kwargs:
      events = events.filter((self.kwargs['field'], self.kwargs['pattern']))
    return events
