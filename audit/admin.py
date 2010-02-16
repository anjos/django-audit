#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Ter 29 Set 2009 14:02:27 CEST 

"""Administrative interface for usage reports
"""

from django.contrib import admin
from audit.models import * 
from django.utils.translation import ugettext_lazy as _

class UserAgentAdmin(admin.ModelAdmin):
  list_display = ('browser', 'version', 'os', 'locked', 'bot', 'regexp')
  list_filter = ('locked', 'bot', 'os', 'browser')
  model = UserAgent 

admin.site.register(UserAgent, UserAgentAdmin)

def error(object):
  return bool(object.error) 
error.short_description = _(u'Error')

def bot(object):
  if object.agent: return object.agent.bot
  return False
bot.short_descriptio = _(u'Bot')

class ActivityAdmin(admin.ModelAdmin):
  list_display = ('user', 'date', 'request_url', 'processing_time', error, 'agent', bot)
  list_filter = ('user', 'date', 'request_url', 'agent')
  model = UserActivity

admin.site.register(UserActivity, ActivityAdmin)

