from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agenda.views.home', name='home'),
    # url(r'^agenda/', include('agenda.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('usermanagement.urls')),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, {'next_page': '/accounts/login/'}),
    url(r'^accounts/profile/$', login_required(TemplateView.as_view(template_name="registration/profile.html"))),
)
