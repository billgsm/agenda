# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from views import (delete_participant, Evenement_List, Evenement_Detail)
from models import Evenement
from personal_calendar.forms import EventForm


urlpatterns = patterns('',
    url(r'^create/$', CreateView.as_view(model=Evenement,
               form_class=EventForm), name='create'),

    url(r'^(?P<pk>\d+)/update/$', UpdateView.as_view(model=Evenement,
                       form_class=EventForm), name='update'),

    url(r'^lists/$', Evenement_List.as_view(paginate_by=10), name='liste'),

    url(r'^lists/(?P<field>[\w-]+)/(?P<pattern>[\w-]+)/$',
        Evenement_List.as_view(paginate_by=10), name='liste'),

    url(r'^(?P<pk>\d+)/delete/$', DeleteView.as_view(
                  model=Evenement, success_url=reverse_lazy('liste')),
        name='delete'
       ),

    url(r'^(\d+)/participant/(\d+)/delete/$', delete_participant,
        name='delete_participant'),

    url(r'^(?P<pk>\d+)/detail/$', Evenement_Detail.as_view(), name='details'),
    )
