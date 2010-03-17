#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:18:55 CEST 

"""Utilities for statistics lookup
"""

# execute when we load
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db import models
from django.db.models import Min, Max, Count
from pygeoip import GeoIP
from conf import settings
from models import *
import os

try:
  from audit.uasparser import UASparser
except ImportError:
  print '### WARNING ### You need to install the UASparser plugin!'
  pass

# Loads location databases
if os.path.exists(settings.AUDIT_COUNTRY_DATABASE):
  COUNTRY = GeoIP(settings.AUDIT_COUNTRY_DATABASE)
else: COUNTRY=None
if os.path.exists(settings.AUDIT_CITY_DATABASE):
  CITY = GeoIP(settings.AUDIT_CITY_DATABASE)
else: CITY=None

from pygooglechart import * 
import operator
import datetime
from dateutil.relativedelta import *

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

def try_ua_parsing(activity):
  """Tries to parse the UA string from the request."""
  if not activity.browser_info: return
  parser = UASparser(settings.AUDIT_USERAGENT_DATABASE)
  result = parser.parse(str(activity.browser_info))
  activity.ua_name = result['ua_name']
  activity.ua_icon = result['ua_icon']
  activity.ua_family = result['ua_family']
  activity.os_name = result['os_name']
  activity.os_icon = result['os_icon']
  activity.os_family = result['os_family']
  activity.ua_type = result['typ']

def pie_chart(data, labels, legend):
  width = settings.AUDIT_PIE_WIDTH
  height = settings.AUDIT_PIE_HEIGHT
  chart = PieChart2D(width, height)
  chart.set_colours(settings.AUDIT_PIE_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data(data)
  # calculates the percentages
  total = sum(data)
  if not total: return
  if legend:
    lab = [k.encode('utf-8') for k in labels]
    for l in range(len(lab)): lab[l] += ' (%.1f%%)' % (100.0*data[l]/total)
    chart.set_pie_labels(lab)
  return chart

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

def pie_usage(q, legend):
  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ).exclude(RobotQ)
  robot = q.filter(AnonymousQ).filter(RobotQ)
  return pie_chart([log.count(), unlog.count(), robot.count()],
    [ugettext(u'Logged users'), ugettext(u'Anonymous'), ugettext(u'Robots')],
    legend)

def pie_fidelity(q, n, legend):
  users = q.values('user__username').annotate(count=Count('user'))
  data = {}
  for k in users: data[k['user__username']] = k['count']
  clutter(data, n, ugettext('others'))
  return pie_chart(data.values(), data.keys(), legend)

def eval_field(q, n, field):
  """Evaluate field statistics."""
  data = q.values(field).annotate(count=Count(field))
  tmp = {}
  for k in data: 
    if k[field]: tmp[k[field]] = k['count']
    else: tmp[ugettext(u'Unknown').encode('utf-8')] = k['count']
  if n: clutter(tmp, n, ugettext(u'others').encode('utf-8'))
  return tmp 

def pie_country(q, n, legend):
  hits = eval_field(q, n, 'country')
  return pie_chart(hits.values(), hits.keys(), legend)

def map_country(q, focus):

  class MyMapChart(MapChart):
    GEO = ['africa', 'asia', 'europe', 'middle_east', 
           'south_america', 'usa', 'world']

    def __init__(self, *args):
      super(MyMapChart, self).__init__(*args)
    def set_geo_area(self, focus):
      geo = MyMapChart.GEO
      if focus not in geo:
        raise RuntimeError, '"focus" has to be one of %s' % ', '.join(geo)
      self.geo_area = focus
    def get_url(self, *args):
      return super(MyMapChart, self).get_url(*args) + \
          '&chtm=%s' % self.geo_area
    def add_data(self, values):
      self.auto_scale = False #we scale the data ourselves
      scaled = [int(round(float(SimpleData.max_value)*v/max(values))) for v in values]
      super(MyMapChart, self).add_data(scaled)

  width = settings.AUDIT_MAP_WIDTH
  height = settings.AUDIT_MAP_HEIGHT
  chart = MyMapChart(width, height)
  chart.set_geo_area(focus)
  chart.set_colours(settings.AUDIT_MAP_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_MAP_BACKGROUND)
  hits = eval_field(q, 0, 'country_code')
  unk = ugettext(u'Unknown').encode('utf-8')
  if hits.has_key(unk): del hits[unk]
  chart.set_codes(hits.keys())
  chart.add_data(hits.values())
  return chart 

def pie_city(q, n, legend):
  data = q.values('city', 'country_code').annotate(count=Count('city'))
  hits = {}
  for k in data: 
    if k['city']: hits[k['city'] + ', ' + k['country_code']] = k['count']
    elif k['country_code']: hits[ugettext(u'Unknown').encode('utf-8') + ', ' \
        + k['country_code']] = k['count']
    else: hits[ugettext(u'Unknown').encode('utf-8')] = k['count']
  clutter(hits, n, ugettext(u'others').encode('utf-8'))
  return pie_chart(hits.values(), hits.keys(), legend)

def pie_browser(q, clip, legend):
  """Evaluates browser statistics."""
  browser = {} 
  for k in q: browser[k.ua_family] = browser.get(k.ua_family, 0) + 1
  clutter(browser, clip, ugettext(u'others').encode('utf-8'))
  return pie_chart(browser.values(), browser.keys(), legend)

def pie_os(q, clip, legend):
  """Evaluates OS statistics."""
  os = {}
  for k in q: os[k.os_family] = os.get(k.os_family, 0) + 1
  clutter(os, clip, ugettext(u'others').encode('utf-8'))
  return pie_chart(os.values(), os.keys(), legend)

def pie_bots(q, clip, legend):
  """Evaluates bot statistics."""
  browser = {} 
  for k in q: browser[k.ua_family] = browser.get(k.ua_family, 0) + 1
  clutter(browser, clip, ugettext(u'others').encode('utf-8'))
  return pie_chart(browser.values(), browser.keys(), legend)

def bar_line_chart(values, legend, style):
  """Calls the Google Chart service to draw either a line or bar chart of the
  given values."""

  width = settings.AUDIT_PLOT_WIDTH
  height = settings.AUDIT_PLOT_HEIGHT

  if style == 'bars':
    M = max([sum((k['logged'], k['anon'], k['bots'])) for k in values])
    chart = StackedVerticalBarChart(width, height, y_range=(0, M))
    chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
    chart.set_bar_width((width-50-(3*len(values)))/len(values))
    chart.set_grid(0, 25, 2, 2)
  elif style == 'lines':
    M = max([max((k['logged'], k['anon'], k['bots'])) for k in values])
    chart = SimpleLineChart(width, height, y_range=(0, M))
    slice = 1/float(len(values)-1)
    chart.fill_linear_stripes(Chart.CHART, 0, 'EEEEEE', slice, 
                                              'FFFFFF', slice)
    chart.set_grid(100*slice, 25, 2, 2)
  else:
    raise SyntaxError, '"style" parameter can only be "values" or "lines"'

  if not M: return 

  chart.set_colours(settings.AUDIT_PLOT_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.add_data([k['logged'] for k in values])
  chart.add_data([k['anon'] for k in values])
  chart.add_data([k['bots'] for k in values])
  if legend:
    chart.set_legend([ugettext(u'Logged users').encode('utf-8'), 
      ugettext(u'Anonymous').encode('utf-8'),
      ugettext(u'Search bots').encode('utf-8')])
    chart.set_legend_position('b')

  chart.set_axis_labels(Axis.BOTTOM, [k['label0'] for k in values])
  left_labels = [int(round(k*M/4.0)) for k in range(5)]
  chart.set_axis_labels(Axis.LEFT, left_labels)

  # draws a second label if there is one
  if values[0].has_key('label1'):
    label1 = [k['label1'] for k in values]
    # avoids duplicates in the second label axis
    for k in reversed(range(1,len(label1))):
      if label1[k] == label1[k-1]: label1[k] = ''
    chart.set_axis_labels(Axis.BOTTOM, label1)
 
  return chart

def monthly_popularity(q, legend, style):
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

  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ).exclude(RobotQ)
  bots = q.filter(AnonymousQ).filter(RobotQ)
  bars = []
  for k in range(len(intervals)-1):
    bars.append({
      'label0': intervals[k].strftime('%b'), 
      'label1': intervals[k].strftime('%Y'),
      'logged': log.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'anon': unlog.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'bots': bots.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      })

  return bar_line_chart(bars, legend, style)

def weekly_popularity(q, legend, style):
  """Calculates a popularity barchart per week."""

  if not q: return

  minimum = q.aggregate(Min('date'))['date__min'] 
  minimum = datetime.datetime(minimum.year, minimum.month, minimum.day, 0, 0, 0) + relativedelta(weekday=MO(-1))
  maximum = q.aggregate(Max('date'))['date__max']
  maximum = datetime.datetime(maximum.year, maximum.month, maximum.day, 0, 0, 0) + relativedelta(weekday=MO(-1))
  weeks = (maximum - minimum).days/7

  intervals = [minimum + relativedelta(weeks=k) for k in range(weeks)]
  intervals += [maximum, maximum + relativedelta(weeks=1)]

  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ).exclude(RobotQ)
  bots = q.filter(AnonymousQ).filter(RobotQ)
  bars = []
  for k in range(len(intervals)-1):
    bars.append({
      'label0': intervals[k].strftime('%U'), 
      'label1': intervals[k].strftime('%Y'),
      'logged': log.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'anon': unlog.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'bots': bots.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      })

  return bar_line_chart(bars, legend, style)

def daily_popularity(q, days, legend, style):
  """Calculates a popularity barchart per day."""

  if not q: return

  maximum = q.aggregate(Max('date'))['date__max']
  maximum = datetime.datetime(maximum.year, maximum.month, maximum.day, 0, 0, 0)
  minimum = maximum - relativedelta(days=days)

  intervals = [minimum + relativedelta(days=k) for k in range(days)]
  intervals += [maximum, maximum + relativedelta(days=1)]

  log = q.exclude(AnonymousQ)
  unlog = q.filter(AnonymousQ).exclude(RobotQ)
  bots = q.filter(AnonymousQ).filter(RobotQ)

  bars = []
  for k in range(len(intervals)-1):
    bars.append({
      'label0': days-k, 
      'logged': log.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'anon': unlog.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      'bots': bots.filter(date__gte=intervals[k]).filter(date__lt=intervals[k+1]).count(),
      })

  return bar_line_chart(bars, legend, style)

def usage_hours(q, legend):
  """An histogram of the usage hours"""

  log = [k.date.hour for k in q.exclude(AnonymousQ)]
  unlog = [k.date.hour for k in q.filter(AnonymousQ).exclude(RobotQ)]
  bots = [k.date.hour for k in q.filter(AnonymousQ).filter(RobotQ)]
  intervals = range(24)

  bars = []
  for k in intervals:
    bars.append({
      'label0': k, 
      'logged': log.count(k),
      'anon': unlog.count(k),
      'bots': bots.count(k),
      })

  return bar_line_chart(bars, legend, 'bars')

def most_visited(q, n):
  """Calculates the most visited URLs."""
  
  data = {}
  for hit in q: data[hit.request_url] = data.get(hit.request_url, 0) + 1
  if data:
    vals = sorted(zip(data.keys(), data.values()), key=operator.itemgetter(1), reverse=True)
    retval = vals[:n]
    retval.append((_(u'others'), sum(map(operator.itemgetter(1), vals[n:]))))
    return retval
  else:
    return {}

def serving_time(since, bins, legend):
  """An histogram of the time to serve a request."""

  q = ParsedProxy.objects.filter(date__gte=since) 
  q_log = ParsedSiteUserProxy.objects.filter(date__gte=since) 
  q_unlog = ParsedAnonymousProxy.objects.filter(date__gte=since) 
  q_robots = RobotProxy.objects.filter(date__gte=since) 

  data = [k.processing_time/1000 for k in q]
  
  # we calculate the maximum, the minimum and the width of each bin, finally,
  # the intervals for the histogram
  minimum = 0 
  maximum = max(data)
  binwidth = float(maximum) / (bins)
  intervals = [k*binwidth for k in range(bins+1)]

  log = [int(k/binwidth) for k in [k.processing_time/1000 for k in q_log]]
  unlog = [int(k/binwidth) for k in [k.processing_time/1000 for k in q_unlog]]
  bots = [int(k/binwidth) for k in [k.processing_time/1000 for k in q_robots]]

  bar_log = [log.count(k) for k in range(bins)]
  bar_unlog = [unlog.count(k) for k in range(bins)]
  bar_bots = [bots.count(k) for k in range(bins)]

  max_y = max([sum(k) for k in zip(bar_log, bar_unlog, bar_bots)])

  chart = StackedVerticalBarChart(settings.AUDIT_PLOT_WIDTH, 
      settings.AUDIT_PIE_HEIGHT, y_range=(0, max_y))

  chart.set_bar_width(18) # pixels
  chart.set_colours(settings.AUDIT_PLOT_COLORS)
  chart.fill_solid(Chart.BACKGROUND, settings.AUDIT_IMAGE_BACKGROUND)
  chart.fill_solid(Chart.CHART, settings.AUDIT_CHART_BACKGROUND)
  chart.add_data(bar_log)
  chart.add_data(bar_unlog)
  chart.add_data(bar_bots)
  chart.set_axis_labels(Axis.BOTTOM, [int(round(k)) for k in intervals])
  chart.set_axis_positions(0, [(100*k)/max(intervals) for k in intervals]) 

  unit = [''] * len(intervals) 
  unit[len(intervals)/2] = ugettext(u'milliseconds').encode('utf-8')
  chart.set_axis_labels(Axis.BOTTOM, unit)
  chart.set_axis_labels(Axis.LEFT, (0, max_y))

  if legend:
    # Legends 
    legend = [
              ugettext(u'Logged users').encode('utf-8'),
              ugettext(u'Anonymous users').encode('utf-8'),
              ugettext(u'Search bots').encode('utf-8'),
             ]
    chart.set_legend(legend)
    chart.set_legend_position('b')

  return chart 
