#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 11 Mar 2010 11:57:28 CET 

"""This script is used to download files from
http://user-agent-string.info/download.
"""

import os, sys

if len(sys.argv) != 3:
  print 'usage: %s directory url' % sys.argv[0]
  sys.exit(1)

dir = sys.argv[1]
url = sys.argv[2]

if not os.path.exists(dir): os.makedirs(dir)

import urllib2
web = urllib2.urlopen(url)

print 'Downloading contents of', url
import tempfile
tmp = tempfile.TemporaryFile()
tmp.write(web.read())
tmp.seek(0)
web.close()

print 'Extracting contents of file into directory', dir
import zipfile
zip = zipfile.ZipFile(tmp, 'r')
zip.extractall(dir)
