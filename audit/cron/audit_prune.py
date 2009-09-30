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
from audit.models import UserActivity 
import datetime
from dateutil.relativedelta import *

cut_date = datetime.datetime.today() -relativedelta(months=AUDIT_MONTHS_TO_LOG)
for k in UserActivity.objects.filter(date__lte=cut_date): k.delete()

