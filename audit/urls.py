#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Wed 15 Apr 23:26:54 2009 

from django.conf.urls.defaults import *
from django.conf import settings
from views import *

if settings.AUDIT_CACHE_ALL_VIEWS:
  from django.views.decorators.cache import cache_page
  overview = cache_page(overview, settings.AUDIT_CACHE_ALL_VIEWS)
  popularity = cache_page(popularity, settings.AUDIT_CACHE_ALL_VIEWS)
  identity = cache_page(identity, settings.AUDIT_CACHE_ALL_VIEWS)
  performance = cache_page(performance, settings.AUDIT_CACHE_ALL_VIEWS)

urlpatterns = patterns('',
                       url(r'^$', overview, name='overview'),
                       url(r'^(?P<months>\d{1,2})/months/$',
                         overview, name='overview-months'),
                       url(r'^popularity/$', popularity, name='popularity'),
                       url(r'^popularity/(?P<months>\d{1,2})/months/$',
                         popularity, name='popularity-months'),
                       url(r'^identity/$', identity, name='identity'),
                       url(r'^identity/(?P<months>\d{1,2})/months/$',
                         identity, name='identity-months'),
                       url(r'^performance/$', performance, name='performance'),
                       url(r'^performance/(?P<months>\d{1,2})/months/$',
                         performance, name='performance-months'),
                      )

# use this instead of urlpatterns directly
namespaced = (urlpatterns, 'audit', 'audit')
