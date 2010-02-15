#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sex 12 Fev 2010 16:56:35 CET 

"""A script to be executed to repopulate our User Agent Database 
"""

import os, sys, csv, codecs
import urllib, shutil, re

class UTF8Recoder:
  """Iterator that reads an encoded stream and reencodes the input to UTF-8"""

  def __init__(self, f, encoding):
    self.reader = codecs.getreader(encoding)(f)

  def __iter__(self):
    return self

  def next(self):
    return self.reader.next().encode("utf-8")

class UnicodeReader:
  """A CSV reader which will iterate over lines in the CSV file "f", which is 
     encoded in the given encoding.
  """

  def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
    f = UTF8Recoder(f, encoding)
    self.reader = csv.reader(f, dialect=dialect, **kwds)

  def next(self):
    row = self.reader.next()
    return [unicode(s, "utf-8") for s in row]

  def __iter__(self):
    return self

# setup Python
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from audit.models import UserAgent
from audit.conf import settings

def download(db, name):
  """Downloads the file pointed by "db" and put it in "name"."""

  print "Downloading %s" % db
  (f, headers) = urllib.urlretrieve(db)
  if os.path.exists(name): os.unlink(name)
  shutil.move(f, name)
  
  # strip the first two lines, which are the DB version
  f = open(name, 'r')
  f2 = open(name + '.tmp', 'w')
  f2.writelines(f.readlines()[2:])
  f.close()
  f2.close()
  os.unlink(name)
  shutil.move(name + '.tmp', name)

def main():
  """Loads a CSV database of user agents and using a URL from internet."""

  db = 'db.csv'
  url = 'http://browsers.garykeith.com/stream.asp?BrowsCapCSV'
  download(url, db)

  reader = UnicodeReader(open(db, 'rt'), encoding='latin1', delimiter=',', quotechar='"')

  got_header = False 
  version_re = re.compile(r'^(?P<browser>\S*)\s*(?P<version>[\d\.]*)$')
  updated = 0
  created = 0
  bots = 0

  for entry in reader:

    # special reading for the header
    if not got_header: 
      got_header = True
      parent = entry.index('Parent')
      browser = entry.index('Browser')
      regexp = entry.index('UserAgent')
      platform = entry.index('Platform')
      continue

    # process output
    b = entry[browser]
    if not b: b = entry[parent]

    # see if there is a version
    match = version_re.match(b)
    v = ''
    if match:
      b = match.group('browser').strip()
      v = match.group('version').strip()

    r = entry[regexp].strip('[]').replace('.', '\.').replace('*', '.*').replace('(', '\(').replace(')', '\)').replace('-', '\-').replace('?','.')
    
    # create the user agents, if none for the same regexp is there
    try: 
      ua = UserAgent.objects.get(regexp=r)
      updated += 1
    except: 
      ua = UserAgent()
      #print 'Creating %s:%s@%s' % (b, v, entry[platform])
      created += 1
    ua.regexp = r
    if b: ua.browser = b.lower()
    if v: ua.version = v.lower()
    else: ua.version = 'unknown'
    if entry[platform]: ua.os = entry[platform].lower()
    else: ua.os = 'unknown'

    #checks bot status
    ua.bot = False
    for k in AUDIT_KNOWN_BOTS:
      if ua.browser.find(k) >= 0 or ua.regexp.find(k) >= 0:
        ua.bot = True
        bots += 1
        break

    ua.save()

  # remove the downloaded database
  os.unlink(db)

  # summary
  print 'Finished updating User-Agent database from %s' % url
  print 'Updated %d entries' % updated
  print 'Created %d entries' % created 
  print '%d robots in total' % bots 

if __name__ == '__main__':
  main()
