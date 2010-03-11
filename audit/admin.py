#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Ter 29 Set 2009 14:02:27 CEST 

"""Administrative interface for usage reports
"""

from django.contrib import admin
from audit.models import * 
from django.utils.translation import ugettext_lazy as _

def os_img(self):
  return '<img src="%s" height="16" width="16" title="%s"/>' % \
      (self.os_icon_url(), self.os_name)
os_img.short_description = _(u'OS') 
os_img.allow_tags = True

def ua_img(self):
  return '<img src="%s" height="16" width="16" title="%s"/>' % \
      (self.ua_icon_url(), self.ua_name)
ua_img.short_description = _(u'Browser') 
ua_img.allow_tags = True

class ActivityAdmin(admin.ModelAdmin):
  list_display = ('user', 'date', 'country', 'processing_time', os_img,
      ua_img, UserActivity.is_success, UserActivity.is_human, 'request_url')
  list_filter = ('user', 'date', 'ua_family', 'os_family', 'request_url')
  model = UserActivity

admin.site.register(UserActivity, ActivityAdmin)

