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
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from audit.models import *
from audit.utils import try_set_location, try_ua_parsing

def main():
  full = False
  if len(sys.argv) > 1: full = True

  if full:
    p = UserActivity.objects.all() # p = to relocate
    q = UserActivity.objects.all() # q = to re-parse UA string
    print 'Full processing, %d entries...' % q.count()
  else:
    p = UnlocatedActivity.objects.all() 
    q = UnidentifiedActivity.objects.all() 
    print 'Partial processing, %d entries...' % (p.count() + q.count())

  print 'Trying to find location of %d entries...' % p.count()
  for k in p: 
     try_set_location(k)
     k.save()
  print 'Done with relocation process.'

  print 'Trying to parse UA strings of %d entries...' % q.count()
  for k in q:
    try_ua_parsing(k)
    k.save()
  print 'Done with UA parsing process.'
  print 'Bye!'
