# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy

from views import (InvitationListView, InvitationCreateView,
    CircleCreateView, CircleListView, UserInfoUpdateView,
    ContactListView, ContactCreateView)
from models import Invitation, Contact, Circle, UserInfo


urlpatterns = patterns('',
    url(r'^invitation-list/$', InvitationListView.as_view(), name='invitation_list'),##
    url(r'^invitation-creation/$', InvitationCreateView.as_view(), name='invitation_create'),##
    url(r'^(?P<pk>\d+)/invitation/$', DetailView.as_view(model=Invitation), name='invitation_detail'),

    url(r'^contact/(?P<pk>\d+)/$', DetailView.as_view(model=Contact), name='contact_detail'),##
    url(r'contact/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(model=Contact,
            success_url=reverse_lazy('contact_list')),
        name='contact_delete'),##
    url(r'^contact-list/$', ContactListView.as_view(), name='contact_list'),##
    url(r'^contact/(?P<pk>\d+)/update/$', UserInfoUpdateView.as_view(), name='contact_update'),##

    url(r'circle-list/$', CircleListView.as_view(model=Circle), name='circle_list'),#
    url(r'circle/(?P<pk>\d+)/$', DetailView.as_view(model=Circle), name='circle_detail'),##
    url(r'circle/(?P<pk>\d+)/delete/$',
      DeleteView.as_view(model=Circle,
        success_url=reverse_lazy('circle_list')),
      name='circle_delete'),
    url(r'circle/create/$', CircleCreateView.as_view(), name='circle_create'),##
    )
