#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:08:46 CEST 

"""Models to log user statistics
"""

import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

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

  country_code = models.CharField(_(u'Country code'), help_text=_(u'The 2-digit country code from where the request originated.'), blank=True, null=False, max_length=3, db_index=True, default='')

  languages = models.CharField(_(u'Accepted languages'), help_text=_(u'The language codes that would be better according to the requester.'), blank=True, null=True, max_length=100, default='')

  # information that will get parsed by UASparser
  ua_name = models.CharField(_(u'Browser'), help_text=_(u'The browser name'), blank=True, null=True, max_length=50)

  ua_icon = models.CharField(_(u'Browser icon'), help_text=_(u'The name of the browser icon to use for this user agent'), blank=True, null=True, max_length=50)

  ua_family = models.CharField(_(u'Browser family'), help_text=_(u'The family of browsers this browser belongs to'), blank=True, null=True, max_length=50)

  os_name = models.CharField(_(u'OS'), help_text=_(u'The name of the OS the request came from'), blank=True, null=True, max_length=50)

  os_icon = models.CharField(_(u'OS icon'), help_text=_(u'The name of the OS icon to use for this operating system'), blank=True, null=True, max_length=50)
  
  os_family = models.CharField(_(u'OS family'), help_text=_(u'The family of OSs this browser belongs to'), blank=True, null=True, max_length=50)

  ua_type = models.CharField(_(u'Browser type'), help_text=_(u'The browser type'), blank=True, null=True, max_length=50)

  def os_icon_url(self):
    """Computes the icon URL for the activity."""
    return reverse('media', args=[os.path.join('audit', 'img', 'os', self.os_icon)])
  os_icon_url.short_description = _(u'OS icon URL')

  def ua_icon_url(self):
    """Computes the icon URL for the activity."""
    return reverse('media', args=[os.path.join('audit', 'img', 'ua', self.ua_icon)])
  ua_icon_url.short_description = _(u'Browser icon URL')

  def is_error(self):
    """Verifies if we were on error"""
    return bool(self.error)
  is_error.short_description = _(u'Error')
  is_error.boolean = True

  def is_success(self):
    """Verifies if we returned successfuly"""
    return not self.is_error()
  is_success.short_description = _(u'Success')
  is_success.boolean = True

  def is_bot(self):
    """Is the user agent a robot?"""
    return self.ua_type.lower() == 'robot'
  is_bot.short_description = _(u'Bot')
  is_bot.boolean = True

  def is_human(self):
    """Is the user agent representing a real user?"""
    return not self.is_bot()
  is_human.short_description = _(u'Human')
  is_human.boolean = True

  def set_processing_time(self):
    self.processing_time = (datetime.now()-self.date).microseconds

# From this point onwards a series of proxies to help us locate specific user
# activities faster.
class UnidentifiedActivityManager(models.Manager):
  """Selects user activities from which the system does not know about the UA/OS"""

  def get_query_set(self):
    return super(IdentifiedActivity, self).get_query_set().filter(Q(ua_name__iexact='unknown') | Q(ua_name='') | Q(ua_name=None))

class UnidentifiedActivity(UserActivity):
  """Activites without the UA string correctly identified."""
  manager = UnidentifiedActivityManager()

  class Meta:
    proxy = True

class IdentifiedActivityManager(models.Manager):
  """Selects user activities from which the system knows about the UA/OS"""

  def get_query_set(self):
    return super(IdentifiedActivity, self).get_query_set().exclude(Q(ua_name__iexact='unknown') | Q(ua_name='') | q(ua_name=None))

class IdentifiedActivity(UserActivity):
  """Activites with the UA string correctly identified."""
  manager = IdentifiedActivityManager()

  class Meta:
    proxy = True

class RobotActivityManager(IdentifiedActivityManager):
  """Select robot activity"""

  def get_query_set(self):
    return super(RobotActivity, self).get_query_set().filter(ua_type__iexact='robot')

class RobotActivity(IdentifiedActivity):
  """Activites by robots."""
  manager = RobotActivityManager()

  class Meta:
    proxy = True

class HumanActivityManager(IdentifiedActivityManager):
  """Select human activity"""

  def get_query_set(self):
    return super(HumanActivity, self).get_query_set().exclude(ua_type__iexact='robot')

class HumanActivity(IdentifiedActivity):
  """Activites by humans."""
  manager = HumanActivityManager()

  class Meta:
    proxy = True

class UnlocatedActivityManager(models.Manager):
  """Selects places with cities or countries that were not identified."""

  def get_query_set(self):
    return super(UnlocatedActivityManager, self).get_query_set().filter(Q(city='')|Q(country=''))

class UnlocatedActivity(UserActivity):
  """Activites without city or country located."""
  manager = UnidentifiedActivityManager()

  class Meta:
    proxy = True

class LocatedActivityManager(models.Manager):
  """Selects activities that were well located."""

  def get_query_set(self):
    return super(LocatedActivityManager, self).get_query_set().exclude(Q(city='')|Q(country=''))

class LocatedActivity(UserActivity):
  """Activites with city and country located."""
  manager = LocatedActivityManager()

  class Meta:
    proxy = True

class SiteUserActivityManager(models.Manager):
  """Selects activities by site users."""

  def get_query_set(self):
    return super(SiteUserActivity, self).get_query_set().exclude(user=None)

class SiteUserActivityManager(UserActivity):
  """Activites by authenticated users."""
  manager = SiteUserActivityManager()

  class Meta:
    proxy = True

class AnonymousActivityManager(models.Manager):
  """Selects activities by unauthenticated users."""

  def get_query_set(self):
    return super(AnonymousActivity, self).get_query_set().filter(user=None)

class AnonymousActivity(UserActivity):
  """Activites by unauthenticated users."""

  manager = AnonymousActivityManager()

  class Meta:
    proxy = True
