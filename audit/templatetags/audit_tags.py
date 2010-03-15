#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sun 14 Mar 10:08:52 2010 

"""Inclusion tags so you can include statistics displays on your site.
"""

from django.template import Library
register = Library()
 
from audit.models import *
from audit.conf import settings 
from audit.utils import *

from django.utils.translation import ugettext

PLOT_CONTENTS = ['logged', 'anonymous', 'robots', 'all'] 

@register.inclusion_tag('audit/embed/navigation.html')
def audit_navigation(months):
  """Navigation through standard displays."""
  return {'months': months, 
          'choice': range(1, settings.AUDIT_MONTHS_TO_LOG + 1)}

@register.inclusion_tag('audit/embed/summary.html')
def audit_summary(months=settings.AUDIT_MONTHS_TO_SHOW):
  """Prints out numbers that summarize website access.""" 

  date = datetime.datetime.now() - relativedelta(months=int(months))
  q = ParsedProxy.objects.all().filter(date__gte=date)    
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ)
  
  #separate bots and humans
  unlog_humans = unlog.exclude(RobotQ)
  unlog_bots = unlog.filter(RobotQ)

  #entries
  hits = {
          'total': q.count(),
          'log': log.count(),
          'unlog': unlog_humans.count(),
          'bots': unlog_bots.count(),
         }

  #errors
  eq = q.exclude(SuccessQ)

  errors = {
            'total': eq.count(),
            'log': eq.exclude(AnonymousQ).count(),
            'unlog': eq.filter(AnonymousQ).exclude(RobotQ).count(),
            'bots': eq.filter(AnonymousQ).filter(RobotQ).count(),
           }

  return { 
          'date': date,
          'hits': hits, 
          'errors': errors, 
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_response_time(months=settings.AUDIT_MONTHS_TO_SHOW, 
                        bins=20,
                        height=settings.AUDIT_PLOT_HEIGHT,
                        legend=True,
                       ):
  """Plots the response time for the website."""

  since = datetime.datetime.now() - relativedelta(months=int(months))

  return { 
           'chart': serving_time(since, bins, legend),
           'height': height,
         }

def getq(months, type):
  if type == 'all':
    q = ParsedProxy.objects.all()
  elif type == 'logged':
    q = ParsedSiteUserProxy.objects.all()
  elif type == 'anonymous':
    q = ParsedAnonymousProxy.objects.all()
  elif type == 'robots':
    q = RobotProxy.objects.all()
  else:
    raise SyntaxError, 'The type should be in range %s' % PLOT_CONTENTS
  since = datetime.datetime.now() - relativedelta(months=int(months))
  return q.filter(date__gte=since)

@register.inclusion_tag('audit/embed/chart.html')
def audit_country_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                      type='all',
                      clip=settings.AUDIT_NUMBER_OF_COUNTRIES,
                      height=settings.AUDIT_PLOT_HEIGHT,
                      legend=True,
                     ):
  return {
          'chart': pie_country(getq(months, type), clip, legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_city_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                   type='all',
                   clip=settings.AUDIT_NUMBER_OF_CITIES,
                   height=settings.AUDIT_PIE_HEIGHT,
                   legend=True,
                  ):
  return {
          'chart': pie_city(getq(months, type), clip, legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_browser_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                      type='all',
                      clip=8,
                      height=settings.AUDIT_PIE_HEIGHT,
                      legend=True,
                     ):
  return {
          'chart': pie_browser(getq(months, type), clip, legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_os_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                 type='all',
                 clip=8,
                 height=settings.AUDIT_PIE_HEIGHT,
                 legend=True,
                ):
  return {
          'chart': pie_os(getq(months, type), clip, legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_bot_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                  clip=12,
                  height=settings.AUDIT_PIE_HEIGHT,
                  legend=True,
                 ):
  return {
          'chart': pie_bots(getq(months, 'robots'), clip, legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_usage_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                    height=settings.AUDIT_PIE_HEIGHT,
                    legend=True,
                    ):
  
  return {
          'chart': pie_usage(getq(months, 'all'), legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_fidelity_pie(months=settings.AUDIT_MONTHS_TO_SHOW, 
                       clip=12,
                       height=settings.AUDIT_PIE_HEIGHT,
                       legend=True,
                       ):
  
  return {
          'chart': pie_fidelity(getq(months, 'logged'), clip, legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_daily_plot(months=settings.AUDIT_MONTHS_TO_SHOW, 
                     height=settings.AUDIT_PIE_HEIGHT,
                     legend=True,
                     style='bars',
                    ):
  
  return {
          'chart': daily_popularity(getq(months, 'all'), 30, legend, style),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_weekly_plot(months=settings.AUDIT_MONTHS_TO_SHOW, 
                      height=settings.AUDIT_PIE_HEIGHT,
                      legend=True,
                      style='bars',
                     ):
  
  return {
          'chart': weekly_popularity(getq(months, 'all'), legend, style),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_monthly_plot(months=settings.AUDIT_MONTHS_TO_SHOW, 
                       height=settings.AUDIT_PIE_HEIGHT,
                       legend=True,
                       style='bars',
                      ):
  
  return {
          'chart': monthly_popularity(getq(months, 'all'), legend, style),
          'height': height,
         }

@register.inclusion_tag('audit/embed/chart.html')
def audit_usagehours_plot(months=settings.AUDIT_MONTHS_TO_SHOW, 
                          height=settings.AUDIT_PIE_HEIGHT,
                          legend=True,
                         ):
  
  return {
          'chart': usage_hours(getq(months, 'all'), legend),
          'height': height,
         }

@register.inclusion_tag('audit/embed/mostpop.html')
def audit_popular_urls(months=settings.AUDIT_MONTHS_TO_SHOW,
                       maxurls=settings.AUDIT_MAXIMUM_URLS):
  
  return {
          'visited': most_visited(getq(months, 'anonymous'), maxurls), 
         }

