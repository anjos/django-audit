#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:31:06 CEST 

"""A script to be executed to cleanup our database
"""

import os
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from audit.conf import settings
import urllib, shutil

def refresh_db(path, bin):
  print "Refreshing installation of %s..." % path
  (gzip, headers) = urllib.urlretrieve(bin)
  os.system('gzip -d %s' % gzip)
  if os.path.exists(path): os.unlink(path)
  dir = os.path.dirname(path)
  if not os.path.exists(dir): os.makedirs(dir)
  shutil.move(gzip[:-3], path)

def main():
  refresh_db(settings.AUDIT_COUNTRY_DATABASE, 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz')
  refresh_db(settings.AUDIT_CITY_DATABASE, 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz')
