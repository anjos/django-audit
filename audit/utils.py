#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:18:55 CEST 

"""Utilities for statistics lookup
"""

# execute when we load
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.models import Min, Max, Count
from pygeoip import GeoIP
from audit.conf import settings
import os

# Loads location databases
if os.path.exists(settings.AUDIT_COUNTRY_DATABASE):
  COUNTRY = GeoIP(settings.AUDIT_COUNTRY_DATABASE)
else: COUNTRY=None
if os.path.exists(settings.AUDIT_CITY_DATABASE):
  CITY = GeoIP(settings.AUDIT_CITY_DATABASE)
else: CITY=None

from pygooglechart import PieChart3D, StackedVerticalBarChart, Axis, Chart
import operator
import datetime
from dateutil.relativedelta import *

def pie_chart(width, height, caption, data, labels):
  chart = PieChart3D(width, height)
  chart.set_colours(settings.AUDIT_CHART_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data(data)
  # calculates the percentages
  total = sum(data)
  if not total: return
  lab = [k.encode('utf-8') for k in labels]
  for l in range(len(lab)): lab[l] += ' (%.1f%%)' % (100.0*data[l]/total)
  chart.set_pie_labels(lab)
  return {'url': chart.get_url(), 'width': width, 'height': height,
      'caption': caption}

def pie_usage(width, height, caption, log, unlog):
  return pie_chart(width, height, caption, [log.count(), unlog.count()],
      [ugettext(u'Logged users'), ugettext(u'Anonymous')])

def clutter(data, n, other_label):
  if len(data) > n:
    threshold = sorted(data.values(), reverse=True)[n-1]
    data[other_label] = 0
    delete = []
    for k in data.iterkeys():
      if data[k] < threshold and k != other_label:
        data[other_label] += data[k]
        delete.append(k)
    for k in delete: del data[k]

def user_fidelity(width, height, caption, log, n):
  users = log.values('user__username').annotate(count=Count('user'))
  data = {}
  for k in users: data[k['user__username']] = k['count']
  clutter(data, n, ugettext('others'))
  return pie_chart(width, height, caption, data.values(), data.keys())

def country_lookup(ip):
  return {
      'country_code': COUNTRY.country_code_by_addr(ip),
      'country_name': COUNTRY.country_name_by_addr(ip),
      'city': None,
    }

def try_set_location(activity):
  location = None
  if not activity.client_address: return
  if activity.client_address:
    try:
      if CITY: 
        location = CITY.record_by_addr(activity.client_address)
        location['city'] = location.get('city', '')
      elif COUNTRY: location = country_lookup(activity.client_address)
    except:
      return
  else: return
  if not location: return
  activity.city = location['city'].decode('iso-8859-1')
  activity.country = location['country_name'].decode('iso-8859-1')
  activity.country_code = location['country_code'].decode('iso-8859-1')

def eval_field(q, n, field):
  """Evaluate field statistics."""
  data = q.values(field).annotate(count=Count(field))
  tmp = {}
  for k in data: 
    if k[field]: tmp[k[field]] = k['count']
    else: tmp[ugettext(u'Unknown').encode('utf-8')] = k['count']
  clutter(tmp, n, ugettext(u'Others').encode('utf-8'))
  return tmp 

def pie_country(width, height, caption, q, n=6):
  hits = eval_field(q, n, 'country')
  return pie_chart(width, height, caption, hits.values(), hits.keys())

def pie_city(width, height, caption, q, n=10):
  data = q.values('city', 'country_code').annotate(count=Count('city'))
  hits = {}
  for k in data: 
    if k['city']: hits[k['city'] + ', ' + k['country_code']] = k['count']
    elif k['country_code']: hits[ugettext(u'Unknown').encode('utf-8') + ', ' \
        + k['country_code']] = k['count']
    else: hits[ugettext(u'Unknown').encode('utf-8')] = k['count']
  clutter(hits, n, ugettext(u'Others').encode('utf-8'))
  return pie_chart(width, height, caption, hits.values(), hits.keys())

BROWSER = [
      'safari',
      'konqueror',
      'msie',
      'firefox',
      'chrome',
      'netscape',
    ]

BOTS = [
      'googlebot',
      'msnbot',
      'slurp',
    ]

OPERATING_SYSTEM = [
      'linux',
      'windows',
      'macintosh',
    ]

def eval_browsers(q, exclude_bots=True):
  """Evaluate browser statistics."""

  for k in q:
    print k
  
  # evaluate browsers
  browser = {}
  consider = BROWSER
  if not exclude_bots: consider += BOTS
  
  os_qs = [] #saves the queries used for browsers
  for k in consider:
    xq = q.filter(browser_info__icontains=k)
    if exclude_bots:
      for b in BOTS: xq = xq.exclude(browser_info__icontains=b)
    if xq.count():
      browser[k] = xq.count()
    os_qs.append(xq)

  browser['others'] = q.count() - sum(browser.values()) 
  if exclude_bots:
    bots = eval_bots(q)
    browser['others'] -= sum(bots.values())
 
  # evaluate OS based on the exclusion criteria as before
  os = {}
  totals = 0
  for query in os_qs:
    for k in query:
      os[k] = q.filter(browser_info__icontains=k).count()
      totals += os[k]
  os['others'] = q.count() - totals

  return os, browser

def eval_bots(q):
  """Evaluate browser statistics."""
  browser = {}
  os = {}
  totals = 0
  for k in BOTS: 
    browser[k] = q.filter(browser_info__icontains=k).count()
    totals += browser[k]
  return browser 

def pie_browsers(width, height, caption, q):
  os, browser = eval_browsers(q)
  return (pie_chart(width, height, caption, os.values(), os.keys()),
      pie_chart(width, height, caption, browser.values(), browser.keys()))

def pie_bots(width, height, caption, q):
  browser = eval_bots(q)
  return pie_chart(width, height, caption, browser.values(), browser.keys())

def monthy_popularity(width, height, caption, q):
  """Calculates a popularity barchart per month."""

  if not q: return

  minimum = q.aggregate(Min('date'))['date__min'] 
  minimum = datetime.datetime(minimum.year, minimum.month, 1, 0, 0, 0)
  maximum = q.aggregate(Max('date'))['date__max']
  maximum = datetime.datetime(maximum.year, maximum.month, 1, 0, 0, 0)
  months = abs(relativedelta(minimum, maximum).months)

  minimum = datetime.datetime(minimum.year, minimum.month, 1, 0, 0, 0)
  intervals = [minimum + relativedelta(months=k) for k in range(months)]
  intervals += [maximum, maximum + relativedelta(months=1)]

  log = q.exclude(user=None)
  unlog = q.filter(user=None)
  max = 0
  bars = []
  for k in range(len(intervals)-1):
    bars.append({
      'label0': intervals[k].strftime('%b'), 
      'label1': intervals[k].strftime('%Y'),
      'logged': log.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'anon': unlog.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      })
    hits = bars[-1]['logged'] + bars[-1]['anon']
    if hits > max: max = hits

  # here we have all labels organized and entries counted.
  if not max: return 

  chart = StackedVerticalBarChart(width, height, y_range=(0, max))
  chart.set_colours(settings.AUDIT_CHART_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data([k['logged'] for k in bars])
  chart.add_data([k['anon'] for k in bars])
  chart.set_legend([ugettext(u'Logged users').encode('utf-8'), 
    ugettext(u'Anonymous').encode('utf-8')])
  chart.set_axis_labels(Axis.BOTTOM, [k['label0'] for k in bars])
  label1 = [k['label1'] for k in bars]
  # avoid duplicates in the year axis
  for k in reversed(range(1,len(label1))):
    if label1[k] == label1[k-1]: label1[k] = ''
  chart.set_axis_labels(Axis.BOTTOM, label1)
  chart.set_axis_labels(Axis.LEFT, (0, max))
 
  return {'url': chart.get_url(), 'width': width, 'height': height,
      'caption': caption}

def weekly_popularity(width, height, caption, q):
  """Calculates a popularity barchart per month."""

  if not q: return

  minimum = q.aggregate(Min('date'))['date__min'] 
  minimum = datetime.datetime(minimum.year, minimum.month, minimum.day, 0, 0, 0) + relativedelta(weekday=MO(-1))
  maximum = q.aggregate(Max('date'))['date__max']
  maximum = datetime.datetime(maximum.year, maximum.month, maximum.day, 0, 0, 0) + relativedelta(weekday=MO(-1))
  weeks = abs(relativedelta(minimum, maximum).days/7)

  intervals = [minimum + relativedelta(weeks=k) for k in range(weeks)]
  intervals += [maximum, maximum + relativedelta(weeks=1)]

  log = q.exclude(user=None)
  unlog = q.filter(user=None)
  max = 0
  bars = []
  for k in range(len(intervals)-1):
    bars.append({
      'label0': intervals[k].strftime('%U'), 
      'label1': intervals[k].strftime('%Y'),
      'logged': log.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'anon': unlog.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      })
    hits = bars[-1]['logged'] + bars[-1]['anon']
    if hits > max: max = hits

  # here we have all labels organized and entries counted.
  if not max: return 

  chart = StackedVerticalBarChart(width, height, y_range=(0, max))
  chart.set_colours(settings.AUDIT_CHART_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data([k['logged'] for k in bars])
  chart.add_data([k['anon'] for k in bars])
  chart.set_legend([ugettext(u'Logged users').encode('utf-8'), 
    ugettext(u'Anonymous').encode('utf-8')])
  chart.set_axis_labels(Axis.BOTTOM, [k['label0'] for k in bars])
  label1 = [k['label1'] for k in bars]
  # avoid duplicates in the year axis
  for k in reversed(range(1,len(label1))):
    if label1[k] == label1[k-1]: label1[k] = ''
  chart.set_axis_labels(Axis.BOTTOM, label1)
  chart.set_axis_labels(Axis.LEFT, (0, max))
 
  return {'url': chart.get_url(), 'width': width, 'height': height,
      'caption': caption}

def most_visited(q, n):
  """Calculates the most visited URLs."""
  
  data = {}
  for hit in q: data[hit.request_url] = data.get(hit.request_url, 0) + 1
  if data:
    vals = sorted(zip(data.keys(), data.values()), key=operator.itemgetter(1), reverse=True)
    retval = vals[:n]
    retval.append((_(u'Others'), sum(map(operator.itemgetter(1), vals[n:]))))
    return retval
  else:
    return {}

def serving_time(width, height, caption, q, bins=15):
  """An histogram of the time to serve a request."""
  data = [k.processing_time/1000 for k in q] 
  
  # we calculate the maximum, the minimum and the width of each bin, finally,
  # the intervals for the histogram
  minimum = 0 
  maximum = max(data)
  binwidth = maximum / bins
  intervals = [k*binwidth for k in range(bins)]
  # intervals.append(maximum)

  log = [int(k/binwidth) for k in [k.processing_time/1000 for k in q.exclude(user=None)]]
  unlog = [int(k/binwidth) for k in [k.processing_time/1000 for k in q.filter(user=None)]]
  bar_log = [log.count(k) for k in range(bins)]
  bar_unlog = [unlog.count(k) for k in range(bins)]
  max_y = max([sum(k) for k in zip(bar_log, bar_unlog)])

  chart = StackedVerticalBarChart(width, height, y_range=(0, max_y))
  chart.set_colours(settings.AUDIT_CHART_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data(bar_log)
  chart.add_data(bar_unlog)
  chart.set_axis_labels(Axis.BOTTOM, intervals)
  unit = [''] * bins
  unit[bins/2] = ugettext(u'milliseconds').encode('utf-8')
  chart.set_axis_labels(Axis.BOTTOM, unit)
  chart.set_axis_labels(Axis.LEFT, (0, max_y))
  chart.set_legend([ugettext(u'Logged users').encode('utf-8'), 
    ugettext(u'Anonymous').encode('utf-8')])

  return {'url': chart.get_url(), 'width': width, 'height': height,
      'caption': caption}

def usage_hours(width, height, caption, q):
  """An histogram of the usage hours"""
  log = [k.date.hour for k in q.exclude(user=None)]
  unlog = [k.date.hour for k in q.filter(user=None)]
  intervals = range(24)

  bar_log = [log.count(k) for k in intervals]
  bar_unlog = [unlog.count(k) for k in intervals]
  maximum = max([sum(k) for k in zip(bar_log, bar_unlog)])

  chart = StackedVerticalBarChart(width, height, y_range=(0, maximum))
  chart.set_colours(settings.AUDIT_CHART_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data(bar_log)
  chart.add_data(bar_unlog)
  chart.set_bar_width(15) #pixels
  chart.set_axis_labels(Axis.BOTTOM, intervals)
  unit = [''] * 24
  unit[12] = ugettext(u'day hours').encode('utf-8')
  chart.set_axis_labels(Axis.BOTTOM, unit)
  chart.set_axis_labels(Axis.LEFT, (0, maximum))
  chart.set_legend([ugettext(u'Logged users').encode('utf-8'), 
    ugettext(u'Anonymous').encode('utf-8')])

  return {'url': chart.get_url(), 'width': width, 'height': height,
      'caption': caption}
