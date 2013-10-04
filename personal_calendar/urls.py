# -*- coding: utf-8 -*-
import datetime

from django.conf.urls import patterns, include, url

from views import (details, delete_participant, delete, update_create, Evenement_List)
from models import Evenement


urlpatterns = patterns('',
    url(r'^create/$', update_create, name='update_create'),
    url(r'^(\d+)/details/$', details, name='details'),
    url(r'^lists/$', Evenement_List.as_view(paginate_by=10), name='liste'),
    url(r'^lists/(?P<field>[\w-]+)/(?P<pattern>[\w-]+)/$',
        Evenement_List.as_view(paginate_by=10), name='liste'),
    url(r'^(\d+)/delete/$', delete, name='delete'),
    url(r'^(\d+)/participant/(\d+)/delete/$', delete_participant,
        name='delete_participant'),
    url(r'^(\d+)/update/$', update_create, name='update_create'),
    )
