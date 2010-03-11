#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:31:06 CEST 

"""A script to be executed to relocate and re-parse UA strings. As a side
effect, it refreshes databases for IP location and UA strings. You should run
this once a month, at most. Around the 5th is a good choice.

You can do the non-full re-parsing once a day. It should be relatively fast.
"""

import os, sys
import urllib, shutil

if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from audit.conf import settings

# finds my own location
ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

def refresh_db(path, bin):
  print "Refreshing installation of %s..." % path
  (gzip, headers) = urllib.urlretrieve(bin)
  os.system('gzip -d %s' % gzip)
  if os.path.exists(path): os.unlink(path)
  dir = os.path.dirname(path)
  if not os.path.exists(dir): os.makedirs(dir)
  shutil.move(gzip[:-3], path)

def unzip_url(dir, url):
  import urllib2, tempfile, zipfile
  if dir[0] != os.sep: 
    dir = os.path.join(settings.AUDIT_USERAGENT_DATABASE, dir)
  if not os.path.exists(dir): os.makedirs(dir)
  web = urllib2.urlopen(url)
  print 'Downloading contents of', url
  tmp = tempfile.TemporaryFile()
  tmp.write(web.read())
  tmp.seek(0)
  web.close()

  zip = zipfile.ZipFile(tmp, 'r')
  print 'Testing zip archive...',
  error = zip.testzip()
  if error:
    print
    print 'Error testing downloaded archive at', url
    print 'Error detected on file', error
    return
  print 'OK!'

  for info in zip.infolist():
    basename = os.path.basename(info.filename)
    print 'Extracting %s - %d bytes => %d bytes' % (basename, info.compress_size, info.file_size),
    data = zip.read(info.filename)
    nf = file(os.path.join(dir, basename), 'w')
    nf.write(data)
    nf.close()
    print 'OK!'

  print "Done!"
  zip.close()

def main():
  try:
    pass
    refresh_db(settings.AUDIT_COUNTRY_DATABASE, 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz')
    refresh_db(settings.AUDIT_CITY_DATABASE, 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz')
  except Exception, e:
    print "Could not update the GeoIP databases: %s" % e
    print "Continuing without a GeoIP database refresh..."

  try:
    unzip_url('img/os', 'http://user-agent-string.info/rpc/get_data.php?ico=os')
    unzip_url('img/ua', 'http://user-agent-string.info/rpc/get_data.php?ico=ua')
    unzip_url(ROOT, 'http://user-agent-string.info/ua_rep/uasparser.py.zip')
  except Exception, e:
    print "Could not update the UASparser databases or code: %s" % e
    print "Continuing without this update..."
