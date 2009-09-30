#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 24 Set 2009 12:31:06 CEST 

"""A script to be executed to cleanup our database
"""

import os
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from audit.models import UserActivity 
from audit.utils import try_set_location

for k in UserActivity.objects.filter(country=''):
   try_set_location(k)
   k.save()
