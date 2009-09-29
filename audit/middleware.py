#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:28:29 CEST 

"""Code responsible for tracking the user activity in your website.
"""

from datetime import datetime
from audit.models import *
from audit.conf import settings
from audit.utils import country_lookup, city_lookup 

class Activity:
  """Middleware that tracks the user activity on every website hit."""

  def process_request(self, request):

    if request.META.has_key('HTTP_REFERER'):
      referer = request.META['HTTP_REFERER']
    else:
      referer = ''

    self.activity = UserActivity(
      user = request.user if request.user.is_authenticated() else None,
      date = datetime.now(),
      request_url = request.META['PATH_INFO'],
      referer_url = referer,
      client_address = request.META['REMOTE_ADDR'],
      client_host = request.META['REMOTE_HOST'],  
      browser_info = request.META['HTTP_USER_AGENT']
    )

    # Makes 1 database lookup. If the city database is available, prefer that 
    # one, otherwise, mark the city as "Unknown" and perform country lookup.
    location = city_lookup(request.META['REMOTE_ADDR'])
    if location:
      self.activity.city = location['city']
      self.activity.country = location['country_name']
      self.activity.country_code = location['country_code']
    else:
      location = country_lookup(request.META['REMOTE_ADDR'])
      if location:
        self.activity.country = location['country_name']
        self.activity.country_code = location['country_code']
        
  def process_exception(self, request, exception):
    self.activity.error = str(exception)
    self.activity.set_processing_time()
    self.activity.save()

  def process_response(self, request, response):
    self.activity.set_processing_time()
    self.activity.save()
    return response

