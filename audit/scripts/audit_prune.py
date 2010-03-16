#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:31:06 CEST 

"""A script to be executed to cleanup our database
"""

import os, sys
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from audit.conf import settings
from audit.models import UserActivity 
import datetime, re
from dateutil.relativedelta import *

def main():

  if len(sys.argv) > 1:
    # Checks if we need to keep this activity...
    NOTRACK_REGEXP = [re.compile(k) for k in settings.AUDIT_NO_TRACKING]
    for k in UserActivity.objects.all():
      request_url = k.request_url
      if request_url[0] == '/': request_url = request_url[1:]
      if True in [bool(r.match(request_url)) for r in NOTRACK_REGEXP]:
        print 'Deleting entry #%d for' % k.id, k.request_url
        k.delete()

  cut_date = datetime.datetime.today() - \
      relativedelta(months=settings.AUDIT_MONTHS_TO_LOG)
  for k in UserActivity.objects.filter(date__lte=cut_date): 
    print 'Deleting entry #%d from' % k.id, k.date
    k.delete()
