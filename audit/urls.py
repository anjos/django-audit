#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Wed 15 Apr 23:26:54 2009 

from django.conf.urls.defaults import *

urlpatterns = patterns('audit.views',
                       url(r'^$', 'overview', name='audit-overview'),
                       url(r'^(?P<months>\d{1,2})/months/$',
                         'overview', name='audit-overview-months'),
                       url(r'^popularity/$', 'popularity', 
                         name='audit-popularity'),
                       url(r'^popularity/(?P<months>\d{1,2})/months/$',
                         'popularity', name='audit-popularity-months'),
                       url(r'^identity/$', 'identity', name='audit-identity'),
                       url(r'^identity/(?P<months>\d{1,2})/months/$',
                         'identity', name='audit-identity-months'),
                       url(r'^performance/$', 'performance', 
                         name='audit-performance'),
                       url(r'^performance/(?P<months>\d{1,2})/months/$',
                         'performance', name='audit-performance-months'),
                      )

