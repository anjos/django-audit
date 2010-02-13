#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sex 12 Fev 2010 16:56:35 CET 

"""A script to be executed to repopulate our User Agent Database 
"""

import os, sys, csv
from audit.models import UserAgent
import urllib, shutil

# setup Python
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

def download(db, name):
  """Downloads the file pointed by "db" and put it in "name"."""

  print "Downloading %s" % db
  (f, headers) = urllib.urlretrieve(db)
  if os.path.exists(name): os.unlink(name)
  shutil.move(f, name)
  
  # strip the first two lines, which are the DB version
  f = open(name, 'r')
  f2 = open(name + '.tmp', 'w')
  f2.write(f.readlines()[2:])
  f.close()
  f2.close()
  os.unlink(name)
  shutil.move(name + '.tmp', name)

def main():
  """Loads a CSV database of user agents and using a URL from internet."""

  db = 'db.csv'
  download('http://browsers.garykeith.com/stream.asp?BrowsCapCSV', db)

  reader = csv.reader(open(db), delimiter=',', quote='"')

  for entry in reader:
    print entry[0]
