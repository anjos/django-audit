#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 16:48:31 CEST 

"""My own settings
"""
import os
from django.conf import settings

# The file containing the country IP database. Set it to empty if you don't
# want to execute IP country lookups.
AUDIT_COUNTRY_DATABASE = getattr(settings, 'AUDIT_COUNTRY_DATABASE',
  os.path.join(settings.MEDIA_ROOT, 'audit/db/GeoIP.dat'))

# The file containing the city IP database. Set it to empty if you don't
# want to execute IP country lookups.
AUDIT_CITY_DATABASE = getattr(settings, 'AUDIT_CITY_DATABASE',
  os.path.join(settings.MEDIA_ROOT, 'audit/db/GeoLiteCity.dat'))

# The directory that contains the UserAgent database 
AUDIT_USERAGENT_DATABASE = getattr(settings, 'AUDIT_USERAGENT_DATABASE',
  os.path.join(settings.MEDIA_ROOT, 'audit/db/ua'))

# Number of months to log
AUDIT_MONTHS_TO_LOG = getattr(settings, 'AUDIT_MONTHS_TO_LOG', 24)

# Default number of months to show in views
AUDIT_MONTHS_TO_SHOW = getattr(settings, 'AUDIT_MONTHS_TO_SHOW', 6)

# The width and height of pie charts produced
AUDIT_MAP_WIDTH = getattr(settings, 'AUDIT_MAP_WIDTH', 440) #pixels
AUDIT_MAP_HEIGHT = getattr(settings, 'AUDIT_MAP_HEIGHT', 220) #pixels
AUDIT_PIE_WIDTH = getattr(settings, 'AUDIT_PIE_WIDTH', 500) #pixels
AUDIT_PIE_HEIGHT = getattr(settings, 'AUDIT_PIE_HEIGHT', 200) #pixels
AUDIT_PLOT_WIDTH = getattr(settings, 'AUDIT_PLOT_WIDTH', 500) #pixels
AUDIT_PLOT_HEIGHT = getattr(settings, 'AUDIT_PLOT_HEIGHT', 200) #pixels

# The number of countries and cities on the statistics
AUDIT_NUMBER_OF_COUNTRIES = getattr(settings, 'AUDIT_NUMBER_OF_COUNTRIES', 6)
AUDIT_NUMBER_OF_CITIES = getattr(settings, 'AUDIT_NUMBER_OF_CITIES', 8)

# How many URLs in the "most visited" category
AUDIT_MAXIMUM_URLS = getattr(settings, 'AUDIT_MAXIMUM_URLS', 10)

# Colors for logged and anonymous users
AUDIT_MAP_BACKGROUND = getattr(settings, 'AUDIT_MAP_BACKGROUND', 'CCEEFF')
AUDIT_MAP_COLORS = getattr(settings, 'AUDIT_MAP_COLORS', 
    ['FFFFFF', 'EEEE00', 'FF9900', 'FF0000'])
AUDIT_PIE_COLORS = getattr(settings, 'AUDIT_PIE_COLORS', 
    ['66CC00', '3366CC', ])
AUDIT_PLOT_COLORS = getattr(settings, 'AUDIT_PLOT_COLORS',
    ['33CC00', '3366CC', '330066', ])

# Background colors for the charts
AUDIT_IMAGE_BACKGROUND = getattr(settings, 'AUDIT_IMAGE_BACKGROUND', 'ffffff')
AUDIT_CHART_BACKGROUND = getattr(settings, 'AUDIT_CHART_BACKGROUND', 'ffffff')

# Keep the amount of bot statistics to a fraction of the total amount of
# non-robot statistics. If you set this to to a number smaller than zero, no
# statistics for bots will be kept. 
AUDIT_KEEP_BOT_STATISTICS = getattr(settings, 'AUDIT_KEEP_BOT_STATISTICS', 0.2)

# URLs regular expressions we are not supposed to track
AUDIT_NO_TRACKING = ['^media/(?!cv\/cv\.pdf$)', '^admin', '^openid',
    '^login', '^logout', '^robots.txt', '^.*favicon.ico'] 
