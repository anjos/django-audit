#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Ter 29 Set 2009 14:02:27 CEST 

"""Administrative interface for usage reports
"""

from django.contrib import admin
from audit.models import * 
from django.utils.translation import ugettext_lazy as _

def error(object):
  return bool(object.error) 
error.short_description = _(u'Error')

class ActivityAdmin(admin.ModelAdmin):
  list_display = ('user', 'date', 'request_url', 'processing_time', error)
  list_filter = ('user', 'date')
  model = UserActivity

admin.site.register(UserActivity, ActivityAdmin)

