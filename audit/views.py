#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 18:01:52 CEST 

"""Views for site statistics
"""

from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from audit.models import *
from audit.utils import *
from audit.conf import settings
import datetime
from dateutil.relativedelta import *

def get_date(months=None):
  if months: 
    return (datetime.datetime.now() - relativedelta(months=months), months)
  return (datetime.datetime.now() - \
    relativedelta(months=settings.AUDIT_MONTHS_TO_SHOW), 
    settings.AUDIT_MONTHS_TO_SHOW)

@permission_required('audit.view_audit')
def overview(request, months=None):
  """General view of the current statistics for city/country/browser usage."""

  date, months_ago = get_date(months)
  q = UserActivity.objects.filter(date__gte=date)
  log = q.exclude(user=None)
  unlog = q.filter(user=None)

  width = settings.AUDIT_PIE_WIDTH 
  height = settings.AUDIT_PIE_HEIGHT

  logunlog = pie_usage(width, height, _(u'Site usage'), log, unlog)
  fidelity = user_fidelity(width, height, _(u'User fidelity'), log,
      settings.AUDIT_USERS_TO_SHOW)

  eq = q.exclude(error=None).exclude(error=u'')
  errors = {'total': eq.count(), 
            'log': eq.exclude(user=None).count(),
            'unlog': eq.filter(user=None).count(),
           }

  #and we display it
  return render_to_response('audit/overview.html',
                            { 
                              'hits': (log.count(), unlog.count()),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'logunlog': logunlog,
                              'fidelity': fidelity,
                            },
                            context_instance=RequestContext(request))

@permission_required('audit.view_audit')
def popularity(request, months=None):

  date, months_ago = get_date(months)
  q = UserActivity.objects.filter(date__gte=date)
  log = q.exclude(user=None)
  unlog = q.filter(user=None)

  #now we have a date from the past to look-up
  visited = most_visited(q, settings.AUDIT_MAXIMUM_URLS)
  popularity = monthy_popularity(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per month'), q)
  weekly = weekly_popularity(settings.AUDIT_PLOT_WIDTH,
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per week'), q)
  hours = usage_hours(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Usage hours'), q)

  eq = q.exclude(error=None).exclude(error=u'')
  errors = {'total': eq.count(), 
            'log': eq.exclude(user=None).count(),
            'unlog': eq.filter(user=None).count(),
           }

  #and we display it
  return render_to_response('audit/overview.html',
                            { 
                              'hits': (log.count(), unlog.count()),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'popularity': popularity,
                              'weekly': weekly,
                              'visited': visited, 
                              'hours': hours,
                            },
                            context_instance=RequestContext(request))


@permission_required('audit.view_audit')
def identity(request, months=None):

  date, months_ago = get_date(months)
  q = UserActivity.objects.filter(date__gte=date)
  log = q.exclude(user=None)
  unlog = q.filter(user=None)

  width = settings.AUDIT_PIE_WIDTH 
  height = settings.AUDIT_PIE_HEIGHT
  users_caption = _(u'Site users')
  anonymous_caption = _(u'Anonymous')

  country = (pie_country(width, height, users_caption, log, 
    settings.AUDIT_NUMBER_OF_COUNTRIES), pie_country(width, height, 
      anonymous_caption, unlog, settings.AUDIT_NUMBER_OF_COUNTRIES))
  city = (pie_city(width, height, users_caption, log,
    settings.AUDIT_NUMBER_OF_CITIES), pie_city(width, height, 
      anonymous_caption, unlog, settings.AUDIT_NUMBER_OF_CITIES))
  os, browser = pie_browsers(width, height, users_caption, log)
  osu, browseru = pie_browsers(width, height, anonymous_caption, unlog)
  os = (os, osu)
  browser = (browser, browseru)

  eq = q.exclude(error=None).exclude(error=u'')
  errors = {'total': eq.count(), 
            'log': eq.exclude(user=None).count(),
            'unlog': eq.filter(user=None).count(),
           }

  #and we display it
  return render_to_response('audit/overview.html',
                            { 
                              'hits': (log.count(), unlog.count()),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'country': country,
                              'city': city,
                              'os': os,
                              'browser': browser,
                            },
                            context_instance=RequestContext(request))


@permission_required('audit.view_audit')
def performance(request, months=None):
  
  date, months_ago = get_date(months)
  q = UserActivity.objects.filter(date__gte=date)
  log = q.exclude(user=None)
  unlog = q.filter(user=None)
  serving = serving_time(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Request serving time'), q)

  eq = q.exclude(error=None).exclude(error=u'')
  errors = {'total': eq.count(), 
            'log': eq.exclude(user=None).count(),
            'unlog': eq.filter(user=None).count(),
           }

  return render_to_response('audit/overview.html',
                            { 
                              'hits': (log.count(), unlog.count()),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'serving': serving,
                            },
                            context_instance=RequestContext(request))
