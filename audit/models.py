#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:08:46 CEST 

"""Models to log user statistics
"""

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _

class UserAgent(models.Model):
  """Represents an identified user agent."""

  def __unicode__(self):
    return u'%s@%s: regexp("%s")' % (self.browser, self.os, self.regexp)

  regexp = models.CharField(_(u'Regular expression'), max_length=100,
      db_index=True, unique=True, null=False, blank=False,
      help_text=_(u'The regular expression that will match the user agent'))

  browser = models.CharField(_(u'Browser'), max_length=100,
      help_text=_(u'The actual browser doing the request'))

  os = models.CharField(_(u'Operating System'), max_length=100, 
      help_text=_(u'The Operating System for this browser'))

class UserActivity(models.Model):
  """Represents a user (single) hit at our website."""

  class Meta:
    permissions = ( 
         ('view_audit', 'Can view statistics'), 
                  )

  def __unicode__(self):
    user = _(u'anonymous')
    if self.user: user = self.user.username
    return u'%s@%s %s (%s): %s' % (user, self.date, self.request_url, self.browser_info, self.error)

  user = models.ForeignKey(User, null=True, blank=True, db_index=True,
      help_text=_(u'If the request was by a site registered user, defined it here.'))

  date = models.DateTimeField(_(u'Date'), help_text="Date on which the request started processing", auto_now_add=True, db_index=True)

  processing_time = models.IntegerField(_(u'Processing time'), help_text=_(u'Time the request took to process (in microseconds)'), null=True, blank=True)

  request_url = models.CharField(_(u'Requested URL'), max_length=800, db_index=True)

  referer_url = models.URLField(_(u'Referer'), help_text=_(u'If the user was re-directed from another website, define it here.'), verify_exists=False, db_index=True, blank=True, null=True)

  client_address = models.IPAddressField(_(u'Client IP address'), blank=True, null=True)

  client_host = models.CharField(_(u'Client hostname'), max_length=256, blank=True, null=True)

  browser_info = models.CharField(_(u'Browser'), help_text=_(u'The user agent tag from the browser. Please note this may not correspond to actual client being used since many browsers can send fake tags.'), null=True, blank=True, max_length=512)

  error = models.TextField(_(u'Error'), help_text=_(u'If an error was produced during the user visit, log it here.'), null=True, blank=True)

  city = models.CharField(_(u'City'), help_text=_(u'The city from where the request originated.'), blank=True, null=False, max_length='64', default='')

  country = models.CharField(_(u'Country'), help_text=_(u'The country from where the request originated.'), blank=True, null=False, max_length='32', default='')

  country_code = models.CharField(_(u'Country code '), help_text=_(u'The 2-digit country code from where the request originated.'), blank=True, null=False, max_length=3, db_index=True, default='')

  def set_processing_time(self):
    self.processing_time = (datetime.now()-self.date).microseconds

