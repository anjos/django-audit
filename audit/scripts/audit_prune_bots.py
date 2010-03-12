#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:31:06 CEST 

"""A script to be executed to cleanup our database
"""

import os
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from audit.conf import settings
from audit.models import * 

def main():
  #keeping us safe...
  max = float(settings.AUDIT_KEEP_BOT_STATISTICS)
  if max < 0: max = 0

  bots = RobotProxy.objects.order_by('-date')
  nonbot_count = HumanProxy.objects.all().count()
  maximum_count_to_keep = nonbot_count * max

  to_delete = bots.count() - maximum_count_to_keep
  if bots.count() > maximum_count_to_keep: 
    for k in bots[maximum_count_to_keep:]: k.delete()
    print 'Deleted %d bot entries' % to_delete
  else:
    print 'Number of bot entries (%d) is smaller than threshold (%.2f%% = %d)' % (bots.count(), max, maximum_count_to_keep)
