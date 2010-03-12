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
from models import *
from utils import *
from conf import settings
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
  q = ParsedProxy.objects.all().filter(date__gte=date)    
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ)
  
  #separate bots and humans
  unlog_humans = unlog.exclude(RobotQ)
  unlog_bots = unlog.filter(RobotQ)

  #errors
  eq = q.exclude(SuccessQ)

  errors = {
            'total': eq.count(),
            'log': eq.exclude(AnonymousQ).count(),
            'unlog': eq.filter(AnonymousQ).exclude(RobotQ).count(),
            'bots': eq.filter(AnonymousQ).filter(RobotQ).count(),
           }

  width = settings.AUDIT_PIE_WIDTH 
  height = settings.AUDIT_PIE_HEIGHT

  logunlog = pie_usage(width, height, _(u'Site usage'), log, unlog_humans)
  fidelity = user_fidelity(width, height, _(u'User fidelity'), log,
      settings.AUDIT_USERS_TO_SHOW)

  #and we display it
  return render_to_response('audit/overview.html',
                            { 
                              'hits': (
                                log.count(), 
                                unlog_humans.count(), 
                                unlog_bots.count(),
                                ),
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
  q = ParsedProxy.objects.all().filter(date__gte=date)    
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ)
  
  #separate bots and humans
  unlog_humans = unlog.exclude(RobotQ)
  unlog_bots = unlog.filter(RobotQ)

  #errors
  eq = q.exclude(SuccessQ)

  errors = {
            'total': eq.count(),
            'log': eq.exclude(AnonymousQ).count(),
            'unlog': eq.filter(AnonymousQ).exclude(RobotQ).count(),
            'bots': eq.filter(AnonymousQ).filter(RobotQ).count(),
           }

  #now we have a date from the past to look-up
  hq = q.exclude(RobotQ).filter(AnonymousQ)
  visited = most_visited(hq, settings.AUDIT_MAXIMUM_URLS)
  daily = daily_popularity(settings.AUDIT_PLOT_WIDTH,
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per day'), q)
  popularity = monthy_popularity(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per month'), q)
  weekly = weekly_popularity(settings.AUDIT_PLOT_WIDTH,
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per week'), q)
  hours = usage_hours(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Usage hours'), q)

  #and we display it
  return render_to_response('audit/overview.html',
                            { 
                              'hits': (
                                log.count(), 
                                unlog_humans.count(), 
                                unlog_bots.count(),
                                ),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'popularity': popularity,
                              'daily': daily,
                              'weekly': weekly,
                              'visited': visited, 
                              'hours': hours,
                            },
                            context_instance=RequestContext(request))


@permission_required('audit.view_audit')
def identity(request, months=None):

  date, months_ago = get_date(months)
  q = ParsedProxy.objects.all().filter(date__gte=date)    
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ)
  
  #separate bots and humans
  unlog_humans = unlog.exclude(RobotQ)
  unlog_bots = unlog.filter(RobotQ)

  #errors
  eq = q.exclude(SuccessQ)

  errors = {
            'total': eq.count(),
            'log': eq.exclude(AnonymousQ).count(),
            'unlog': eq.filter(AnonymousQ).exclude(RobotQ).count(),
            'bots': eq.filter(AnonymousQ).filter(RobotQ).count(),
           }

  width = settings.AUDIT_PIE_WIDTH 
  height = settings.AUDIT_PIE_HEIGHT
  users_caption = _(u'Site users')
  anonymous_caption = _(u'Anonymous users')
  bots_caption = _(u'Search bots')

  country = (pie_country(width, height, users_caption, log, 
    settings.AUDIT_NUMBER_OF_COUNTRIES), pie_country(width, height, 
      anonymous_caption, unlog_humans, settings.AUDIT_NUMBER_OF_COUNTRIES))
  city = (pie_city(width, height, users_caption, log,
    settings.AUDIT_NUMBER_OF_CITIES), pie_city(width, height, 
      anonymous_caption, unlog_humans, settings.AUDIT_NUMBER_OF_CITIES))
  os, browser = pie_browsers(width, height, users_caption, log)
  osu, browseru = pie_browsers(width, height, anonymous_caption, unlog_humans)
  os = (os, osu)
  browser = (browser, browseru)
  bots = pie_bots(width, height, bots_caption, unlog_bots)

  #and we display it
  return render_to_response('audit/overview.html',
                            { 
                              'hits': (
                                log.count(), 
                                unlog_humans.count(), 
                                unlog_bots.count()
                                ),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'country': country,
                              'city': city,
                              'os': os,
                              'browser': browser,
                              'bots': bots,
                            },
                            context_instance=RequestContext(request))


@permission_required('audit.view_audit')
def performance(request, months=None):
  
  date, months_ago = get_date(months)
  q = ParsedProxy.objects.all().filter(date__gte=date)    
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ)
  
  #separate bots and humans
  unlog_humans = unlog.exclude(RobotQ)
  unlog_bots = unlog.filter(RobotQ)

  #errors
  eq = q.exclude(SuccessQ)

  errors = {
            'total': eq.count(),
            'log': eq.exclude(AnonymousQ).count(),
            'unlog': eq.filter(AnonymousQ).exclude(RobotQ).count(),
            'bots': eq.filter(AnonymousQ).filter(RobotQ).count(),
           }

  serving = serving_time(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Request serving time'), q)

  return render_to_response('audit/overview.html',
                            { 
                              'hits': (
                                log.count(), 
                                unlog_humans.count(), 
                                unlog_bots.count()
                                ),
                              'errors': errors, 
                              'date': date,
                              'months': months,
                              'ago': months_ago,
                              'serving': serving,
                            },
                            context_instance=RequestContext(request))
