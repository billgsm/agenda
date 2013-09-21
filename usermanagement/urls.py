# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

from usermanagement.views import create_account

urlpatterns = patterns('',
    url(r'^success/$', TemplateView.as_view(template_name='user/success.html')),
    url(r'^create_account/$', create_account),
    url(r'^login/$', login, {'template_name': 'user/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/user/login/'}),
    url(r'^profile/$', login_required(TemplateView.as_view(template_name="user/profile.html"))),
    )
