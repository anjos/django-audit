#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Wed 15 Apr 23:26:54 2009 

from django.conf.urls.defaults import *

urlpatterns = patterns('audit.views',
                       url(r'^$', 'overview', name='overview'),
                       url(r'^(?P<months>\d{1,2})/months/$',
                         'overview', name='overview-months'),
                       url(r'^popularity/$', 'popularity', name='popularity'),
                       url(r'^popularity/(?P<months>\d{1,2})/months/$',
                         'popularity', name='popularity-months'),
                       url(r'^identity/$', 'identity', name='identity'),
                       url(r'^identity/(?P<months>\d{1,2})/months/$',
                         'identity', name='identity-months'),
                       url(r'^performance/$', 'performance', name='performance'),
                       url(r'^performance/(?P<months>\d{1,2})/months/$',
                         'performance', name='performance-months'),
                      )

# use this instead of urlpatterns directly
namespaced = (urlpatterns, 'audit', 'audit')
