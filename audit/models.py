#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:08:46 CEST 

"""Models to log user statistics
"""

import os
from datetime import datetime
from django.db import models
from django.db.models import Q
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

  request_url = models.CharField(_(u'Requested URL'), max_length=800)

  referer_url = models.URLField(_(u'Referer'), help_text=_(u'If the user was re-directed from another website, define it here.'), verify_exists=False, max_length=800, blank=True, null=True)

  client_address = models.IPAddressField(_(u'Client IP address'), blank=True, null=True)

  client_host = models.CharField(_(u'Client hostname'), max_length=256, blank=True, null=True)

  browser_info = models.CharField(_(u'Browser'), help_text=_(u'The user agent tag from the browser. Please note this may not correspond to actual client being used since many browsers can send fake tags.'), null=True, blank=True, max_length=512)

  error = models.TextField(_(u'Error'), help_text=_(u'If an error was produced during the user visit, log it here.'), null=True, blank=True)

  city = models.CharField(_(u'City'), help_text=_(u'The city from where the request originated.'), blank=True, null=False, max_length='64', default='')

  country = models.CharField(_(u'Country'), help_text=_(u'The country from where the request originated.'), blank=True, null=False, max_length='32', default='')

  country_code = models.CharField(_(u'Country code'), help_text=_(u'The 2-digit country code from where the request originated.'), blank=True, null=False, max_length=3, db_index=True, default='')

  languages = models.CharField(_(u'Accepted languages'), help_text=_(u'The language codes that would be better according to the requester.'), blank=True, null=True, max_length=100, default='')

  # information that will get parsed by UASparser
  ua_name = models.CharField(_(u'Browser'), help_text=_(u'The browser name'), blank=True, null=True, max_length=150)

  ua_icon = models.CharField(_(u'Browser icon'), help_text=_(u'The name of the browser icon to use for this user agent'), blank=True, null=True, max_length=50)

  ua_family = models.CharField(_(u'Browser family'), help_text=_(u'The family of browsers this browser belongs to'), blank=True, null=True, max_length=50)

  os_name = models.CharField(_(u'OS'), help_text=_(u'The name of the OS the request came from'), blank=True, null=True, max_length=50)

  os_icon = models.CharField(_(u'OS icon'), help_text=_(u'The name of the OS icon to use for this operating system'), blank=True, null=True, max_length=50)
  
  os_family = models.CharField(_(u'OS family'), help_text=_(u'The family of OSs this browser belongs to'), blank=True, null=True, max_length=50)

  ua_type = models.CharField(_(u'Browser type'), help_text=_(u'The browser type'), blank=True, null=True, max_length=50)

  def os_icon_url(self):
    """Computes the icon URL for the activity."""
    return reverse('media', args=[os.path.join('audit', 'db', 'ua', 'img', 'os', self.os_icon)])
  os_icon_url.short_description = _(u'OS icon URL')

  def ua_icon_url(self):
    """Computes the icon URL for the activity."""
    return reverse('media', args=[os.path.join('audit', 'db', 'ua', 'img', 'ua', self.ua_icon)])
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

#
# Queries setup to facilitate our work
#

# Tells if a User Agent string has already been identified on the Activity
NoIdQ = (Q(ua_name__iexact='unknown') | Q(ua_name='') | Q(ua_name=None))

# Tells if the User Agent string comes from a web robot. Please note this
# should only be applied if the UserActivity has been identified
RobotQ = Q(ua_type__iexact='robot')

# Tells if the request came from a local network or from outside
LocalNetQ = (Q(client_address__startswith='10.') | \
             Q(client_address__startswith='192.168.') | \
             Q(client_address__startswith='127.0.0') | \
             Q(client_address__startswith='169.254.'))

# Tells if the origin (IP) of the request has be localized
UnlocatedQ = (Q(city='') | Q(country=''))

# Tells if the request comes from an Anonymous user or someone registered on
# the site.
AnonymousQ = Q(user=None)

# Tells if the entry the response was successful
SuccessQ = (Q(error=None) | Q(error=''))

#
# A series of Proxies to simplify the querying of the database
#

class UnparsedManager(models.Manager):
  def get_query_set(self):
    return super(UnparsedManager, self).get_query_set().filter(NoIdQ)
class UnparsedProxy(UserActivity):
  objects = UnparsedManager()
  class Meta:
    proxy = True

class ParsedManager(models.Manager):
  def get_query_set(self):
    return super(ParsedManager, self).get_query_set().exclude(NoIdQ)
class ParsedProxy(UserActivity):
  objects = ParsedManager()
  class Meta:
    proxy = True

class RobotManager(ParsedManager):
  def get_query_set(self):
    return super(RobotManager, self).get_query_set().filter(RobotQ)
class RobotProxy(ParsedProxy):
  objects = RobotManager()
  class Meta:
    proxy = True

class HumanManager(ParsedManager):
  def get_query_set(self):
    return super(HumanManager, self).get_query_set().exclude(RobotQ)
class HumanProxy(ParsedProxy):
  objects = HumanManager()
  class Meta:
    proxy = True

class InternalManager(models.Manager):
  def get_query_set(self):
    return super(InternalManager, self).get_query_set().filter(LocalNetQ)
class InternalProxy(UserActivity):
  objects = InternalManager()
  class Meta:
    proxy = True

class ExternalManager(models.Manager):
  def get_query_set(self):
    return super(ExternalManager, self).get_query_set().exclude(LocalNetQ)
class ExternalProxy(UserActivity):
  objects = ExternalManager()
  class Meta:
    proxy = True

class UnlocatedManager(ExternalManager):
  def get_query_set(self):
    return super(UnlocatedManager, self).get_query_set().filter(UnlocatedQ)
class UnlocatedProxy(ExternalProxy):
  objects = UnlocatedManager()
  class Meta:
    proxy = True

class LocatedManager(ExternalManager):
  def get_query_set(self):
    return super(LocatedManager, self).get_query_set().exclude(UnlocatedQ)
class LocatedProxy(ExternalProxy):
  objects = LocatedManager()
  class Meta:
    proxy = True

class AnonymousManager(models.Manager):
  def get_query_set(self):
    return super(AnonymousManager, self).get_query_set().filter(AnonymousQ)
class AnonymousProxy(UserActivity):
  objects = AnonymousManager()
  class Meta:
    proxy = True

class ParsedAnonymousManager(HumanManager):
  def get_query_set(self):
    return super(ParsedAnonymousManager, self).get_query_set().filter(AnonymousQ)
class ParsedAnonymousProxy(HumanProxy):
  objects = ParsedAnonymousManager()
  class Meta:
    proxy = True

class SiteUserManager(models.Manager):
  def get_query_set(self):
    return super(SiteUserManager, self).get_query_set().exclude(AnonymousQ)
class SiteUserProxy(UserActivity):
  objects = SiteUserManager()
  class Meta:
    proxy = True

class SuccessManager(models.Manager):
  def get_query_set(self):
    return super(SuccessManager, self).get_query_set().filter(SuccessQ)
class SuccessProxy(UserActivity):
  objects = SiteUserManager()
  class Meta:
    proxy = True

class ErrorManager(models.Manager):
  def get_query_set(self):
    return super(ErrorManager, self).get_query_set().exclude(SuccessQ)
class ErrorProxy(UserActivity):
  objects = SiteUserManager()
  class Meta:
    proxy = True

class ParsedSiteUserManager(HumanManager):
  def get_query_set(self):
    return super(ParsedSiteUserManager, self).get_query_set().exclude(AnonymousQ)
class ParsedSiteUserProxy(HumanProxy):
  objects = ParsedSiteUserManager()
  class Meta:
    proxy = True

