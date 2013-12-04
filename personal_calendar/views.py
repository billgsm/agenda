#-*-coding: utf-8-*-
import json
import datetime

from django.shortcuts import (render, HttpResponseRedirect,
    render_to_response, HttpResponse)
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.forms import HiddenInput
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.mail import send_mail
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from forms import (EventForm, Evenement_ParticipantForm,
        UpdateParticipantForm)
from models import Evenement, Evenement_Participant
from addressbook.models import Contact


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
        updated_form = get_participants(updated_form, request.user)
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
    form = Evenement_ParticipantForm(initial={'evenement': self.object,
        })
    form = get_participants(form=form, user=self.request.user)
    context['form'] = form
    return context

  def post(self, request, *args, **kwargs):
    form = Evenement_ParticipantForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.status = 1
        cleaned_data = form.cleaned_data
        if not request.user in cleaned_data['evenement'].participants.all():
            Evenement_Participant.objects.create(
                    evenement=cleaned_data['evenement'],
                    participant=request.user,
                    status=0)
        obj.save()
        send_invitation(obj)
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
            updated_form = get_participants(form=updated_form, user=self.request.user)
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

class Evenement_ParticipantUpdateView(UpdateView):
    model = Evenement_Participant
    form_class = UpdateParticipantForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/agenda/lists/')
#########################
# independant Methods
#########################
def get_participants(form, user):
    queryset = form.fields['participant'].queryset
    contacts = [ c.user.pk for c in Contact().all_contacts(user) ]
    form.fields['participant'].queryset = queryset.filter(pk__in=contacts)
    return form

def send_invitation(evenement_participant):
    sender = evenement_participant.evenement.evenement_participant_set.get(
            status=0)
    message = """{0} has invited you to the event {1} which will take place\
 the {2} in {3}:
 {4}
 Mention your participation on \
 http://{5}/agenda/{6}/participation/""".format(sender.participant,
               evenement_participant.evenement.nom,
               evenement_participant.evenement.date,
               evenement_participant.evenement.lieu,
               evenement_participant.evenement.description,
               Site.objects.get_current().domain,
               evenement_participant.pk)
    sender = sender.participant.email
    subject = "You've been invited by {0}".format(sender)
    recipient_list = [evenement_participant.participant.email]
    send_mail(subject, message, sender, recipient_list, fail_silently=False)
