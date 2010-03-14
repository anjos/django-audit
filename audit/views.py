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

@permission_required('audit.view_audit')
def fidelity(request, months=6, template_name='audit/fidelity.html'):
  """General view of the current statistics for user fidelity."""

  return render_to_response(template_name,
                            { 
                              'months': months,
                            },
                            context_instance=RequestContext(request))

@permission_required('audit.view_audit')
def popularity(request, months=6, template_name='audit/popularity.html'):

  date = datetime.datetime.now() - relativedelta(months=int(months))
  q = ParsedProxy.objects.all().filter(date__gte=date)    
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ)
  unlog_humans = unlog.exclude(RobotQ)
  unlog_bots = unlog.filter(RobotQ)

  #now we have a date from the past to look-up
  hq = q.exclude(RobotQ).filter(AnonymousQ)
  daily = daily_popularity(settings.AUDIT_PLOT_WIDTH,
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per day'), q)
  monthly = monthy_popularity(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per month'), q)
  weekly = weekly_popularity(settings.AUDIT_PLOT_WIDTH,
      settings.AUDIT_PLOT_HEIGHT, _(u'Hits per week'), q)
  hours = usage_hours(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PLOT_HEIGHT, _(u'Usage hours'), q)
  visited = most_visited(hq, settings.AUDIT_MAXIMUM_URLS)

  #and we display it
  return render_to_response(template_name,
                            { 
                              'months': months,
                              'daily': daily,
                              'weekly': weekly,
                              'monthly': monthly,
                              'hours': hours,
                              'visited': visited, 
                            },
                            context_instance=RequestContext(request))


@permission_required('audit.view_audit')
def identity(request, months=6, template_name='audit/identity.html'):
  
  return render_to_response(template_name, { 'months': months, },
                            context_instance=RequestContext(request))

@permission_required('audit.view_audit')
def performance(request, months=6, template_name='audit/performance.html'):
  
  return render_to_response(template_name, { 'months': months, },
                            context_instance=RequestContext(request))
