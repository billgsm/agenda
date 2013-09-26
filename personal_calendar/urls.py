# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from views import create, details, delete_participant


urlpatterns = patterns('',
    url(r'^create/$', create),
    url(r'^(\d+)/details/$', details),
    url(r'^(\d+)/participant/(\d+)/delete/$', delete_participant),
    )
