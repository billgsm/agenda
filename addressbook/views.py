#-*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.shortcuts import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import (Invitation, Contact, Circle)
from forms import InvitationForm, CircleForm


class UserInfoUpdateView(UpdateView):

  def get_form(self, form_class):
    import ipdb; ipdb.set_trace()
    form = super(UserInfoUpdateView, self).get_form(form_class)
    form.field['circle'].queryset = Circle.objects.filter(owner=self.request.user)
    return form


class InvitationCreateView(CreateView):
  """
  * Send an invitation:
    - create invitation object
    - if user found add him to sender's addressbook
    - if user not found:q
  """
  form_class = InvitationForm
  model = Invitation

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.sender = self.request.user
    try:
      Invitation.objects.get(email=obj.email, sender=obj.sender)
      form._errors['email'] = ErrorList(
          [u'An invitation has already been sent to this address.'])
      return super(InvitationCreateView, self).form_invalid(form)
    except Invitation.DoesNotExist:
      pass
    obj.save()
    return send_invitation(obj)

  def get_queryset(self):
    return Invitation.objects.filter(sender=self.request.user)


class CircleCreateView(CreateView):
  """
  * Create circles:
    - user cannot have two circles with the same name
  """
  form_class = CircleForm
  model = Circle

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.owner = self.request.user
    try:
      Circle.objects.get(name=obj.name, owner=obj.owner)
      form._errors['name'] = ErrorList(
          [u'This circle already exists.'])
      return super(CircleCreateView, self).form_invalid(form)
    except Circle.DoesNotExist:
      pass
    obj.save()
    return HttpResponseRedirect(reverse('circle_detail', kwargs={'pk': obj.pk}))

  def get_queryset(self):
    return Circle.objects.filter(owner=self.request.user)


class CircleListView(ListView):
  """
  """
  def get_queryset(self):
    return Contact().all_circles(user=self.request.user)


class InvitationListView(ListView):
  """
  """
  def get_queryset(self):
    return Invitation().all_invitations(user=self.request.user)


class ContactListView(ListView):
  """
  """
  def get_queryset(self):
    return Contact().all_contacts(user=self.request.user)

def send_invitation(invitation):
  """
  """
  try:
    user = User.objects.get(email=invitation.email)
    message = "{0} added you to his contacts".format(
        invitation.sender.username)
    contact = Contact(owner=invitation.sender, user=user)
    contact.save()
    invitation.delete()
    return HttpResponseRedirect(contact.get_absolute_url())
  except User.DoesNotExist:
    message = """
{0} Invites you to join his contacts.
You can register on http://{1}/user/create_account/ \
if you want to accept his invitation""".format(
        invitation.sender.username,
        Site.objects.get_current().domain
        )
  send_mail('An invitation sent to you',
             message,
             invitation.sender,
             [invitation.email],
             fail_silently=False
             )
  return HttpResponseRedirect(invitation.get_absolute_url())
