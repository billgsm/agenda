# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^success/$', TemplateView.as_view(template_name='user/success.html')),
    )
