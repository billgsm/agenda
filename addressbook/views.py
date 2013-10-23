from django.views.generic.list import ListView
from django.shortcuts import HttpResponseRedirect

from models import Invitation
from forms import InvitationForm

class InvitationView(ListView):
  form_class = InvitationForm
  model = Invitation

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.sender = self.request.user
    try:
      Invitation.objects.get(email=obj.email, sender=obj.sender)
      form._errors['email'] = ErrorList(
          [u'An invitation has already been sent to this address.'])
      return super(InvitationView, self).form_valid(form)
    except Invitation.DoesNotExist:
      pass
    obj.save()
    return HttpResponseRedirect(obj.get_absolute_url())

  def get_queryset(self):
    return Invitation.objects.filter(sender=self.request.user)

class InvitationListView(ListView):
  def get_queryset(self):
    return Invitation.objects.filter(sender=self.request.user)
