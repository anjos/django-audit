#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Wed 15 Apr 23:26:54 2009 

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from conf import settings

default_months = settings.AUDIT_MONTHS_TO_SHOW

urlpatterns = patterns('audit.views',

    url(r'^$', redirect_to, {'url': 'popularity'}, name='index'), 

    url(r'^fidelity/$', redirect_to, {'url': '%d/' % default_months}, 
        name='fidelity'),
    url(r'^fidelity/(?P<months>\d{1,2})/$', 'fidelity', name='fidelity-months'),

    url(r'^popularity/$',
        redirect_to, {'url': '%d/' % default_months},
        name='popularity'),
    url(r'^popularity/(?P<months>\d{1,2})/$', 
        'popularity', 
        name='popularity-months'),

    url(r'^identity/$', redirect_to, {'url': '%d/' % default_months}, 
        name='identity'),
    url(r'^identity/(?P<months>\d{1,2})/$', 'identity', name='identity-months'),

    url(r'^performance/$', 
        redirect_to, {'url': '%d/' % default_months}, 
        name='performance'),
    url(r'^performance/(?P<months>\d{1,2})/$', 
        'performance', 
        name='performance-months'),
  )

# use this instead of urlpatterns directly
namespaced = (urlpatterns, 'audit', 'audit')
