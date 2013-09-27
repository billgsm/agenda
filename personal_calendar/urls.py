# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from views import (details, delete_participant, liste, delete, update_create)


urlpatterns = patterns('',
    url(r'^(\d+)?/?update/$|create/$', update_create, name='update_create'),
    url(r'^(\d+)/details/$', details, name='details'),
    url(r'^(\d+)/participant/(\d+)/delete/$', delete_participant, name='delete_participant'),
    url(r'^(\d+)/delete/$', delete, name='delete'),
    url(r'^list/$', liste, name='liste'),
    )
