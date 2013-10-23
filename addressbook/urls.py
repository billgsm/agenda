# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from views import InvitationListView, InvitationView


urlpatterns = patterns('',
    url(r'^invitations/$', InvitationListView.as_view(), name='invitation_list'),
    url(r'^invitation/$', InvitationView.as_view()),
    )
