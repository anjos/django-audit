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
AUDIT_MONTHS_TO_LOG = 24

# Default number of months to show in views
AUDIT_MONTHS_TO_SHOW = 6 

# Users to show when displaying the fidelity
AUDIT_USERS_TO_SHOW = 6

# The width and height of pie charts produced
AUDIT_PIE_WIDTH = 400 #pixels
AUDIT_PIE_HEIGHT = 100 #pixels

# The number of countries and cities on the statistics
AUDIT_NUMBER_OF_COUNTRIES = 6
AUDIT_NUMBER_OF_CITIES = 8 

# The popularity bar chart configuration
AUDIT_POPULARITY_WIDTH = 600 #pixels
AUDIT_POPULARITY_HEIGHT = 200 #pixels

# How many URLs in the "most visited" category
AUDIT_MAXIMUM_URLS = 10 

# Colors for logged and anonymous users
AUDIT_CHART_COLORS = ['4d89f9', 'c6d9fd']
