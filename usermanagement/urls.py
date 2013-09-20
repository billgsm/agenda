# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from usermanagement.views import create_account

urlpatterns = patterns('',
    url(r'^success/$', TemplateView.as_view(template_name='user/success.html')),
    url(r'^create_account/$', create_account),
    )
