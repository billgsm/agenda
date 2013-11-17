# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

from views import InvitationListView, InvitationCreateView
from models import Invitation, Contact


urlpatterns = patterns('',
    url(r'^invitations/$', InvitationListView.as_view(), name='invitation_list'),
    url(r'^invitation-creation/$', InvitationCreateView.as_view(), name='invitation_create'),
    url(r'^(?P<pk>\d+)/invitation/$', DetailView.as_view(model=Invitation), name='invitation_detail'),
    url(r'^contact/(?P<pk>\d+)/$', DetailView.as_view(model=Contact), name='contact_detail'),
    )
