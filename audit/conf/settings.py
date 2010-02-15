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

# Number of months to log
AUDIT_MONTHS_TO_LOG = getattr(settings, 'AUDIT_MONTHS_TO_LOG', 24)

# Default number of months to show in views
AUDIT_MONTHS_TO_SHOW = getattr(settings, 'AUDIT_MONTHS_TO_SHOW', 6)

# Users to show when displaying the fidelity
AUDIT_USERS_TO_SHOW = getattr(settings, 'AUDIT_USERS_TO_SHOW', 6)

# The width and height of pie charts produced
AUDIT_PIE_WIDTH = getattr(settings, 'AUDIT_PIE_WIDTH', 450) #pixels
AUDIT_PIE_HEIGHT = getattr(settings, 'AUDIT_PIE_HEIGHT', 120) #pixels
AUDIT_PLOT_WIDTH = getattr(settings, 'AUDIT_PLOT_WIDTH', 600) #pixels
AUDIT_PLOT_HEIGHT = getattr(settings, 'AUDIT_PLOT_HEIGHT', 200) #pixels

# The number of countries and cities on the statistics
AUDIT_NUMBER_OF_COUNTRIES = getattr(settings, 'AUDIT_NUMBER_OF_COUNTRIES', 6)
AUDIT_NUMBER_OF_CITIES = getattr(settings, 'AUDIT_NUMBER_OF_CITIES', 8)

# How many URLs in the "most visited" category
AUDIT_MAXIMUM_URLS = getattr(settings, 'AUDIT_MAXIMUM_URLS', 10)

# Colors for logged and anonymous users
AUDIT_CHART_COLORS = getattr(settings, 'AUDIT_CHART_COLORS', ['ff5555', '55ff55', '5555ff'])

# Background colors for the charts
AUDIT_IMAGE_BACKGROUND = getattr(settings, 'AUDIT_IMAGE_BACKGROUND', 'ffffff')
AUDIT_CHART_BACKGROUND = getattr(settings, 'AUDIT_CHART_BACKGROUND', 'ffffff')

# Cache the views for about 10 minutes. If you want to disable caching, please
# set this value to 0. Also note that if you enable this, you need to make the
# proper changes to your project's settings.py file, enabling the cache system
# with at least CACHE_BACKEND='dummy://'. Please read details here:
# http://docs.djangoproject.com/en/dev/topics/cache/
AUDIT_CACHE_ALL_VIEWS = getattr(settings, 'AUDIT_CACHE_ALL_VIEWS', 0)

# Keep the amount of bot statistics to a fraction of the total amount of
# non-robot statistics. If you set this to to a number smaller than zero, no
# statistics for bots will be kept. 
AUDIT_KEEP_BOT_STATISTICS = getattr(settings, 'AUDIT_KEEP_BOT_STATISTICS', 0.2)
