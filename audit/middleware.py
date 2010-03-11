#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:28:29 CEST 

"""Code responsible for tracking the user activity in your website.
"""

from datetime import datetime
from audit.models import UserActivity
from audit.utils import try_set_location, try_ua_parsing

class Activity:
  """Middleware that tracks the user activity on every website hit."""

  def process_request(self, request):
    self.activity = UserActivity(
      user = request.user if request.user.is_authenticated() else None,
      date = datetime.now(),
      request_url = request.META.get('PATH_INFO', ''),
      referer_url = request.META.get('HTTP_REFERER', ''),
      client_address = request.META.get('REMOTE_ADDR', ''),
      client_host = request.META.get('REMOTE_HOST', ''), 
      browser_info = request.META.get('HTTP_USER_AGENT', ''),
      languages = request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
    )

    # Makes 1 database lookup. If the city database is available, prefer that 
    # one, otherwise, mark the city as "Unknown" and perform country lookup.
    try_set_location(self.activity)

    # Makes a second database lookup for decoding the UserAgent string
    try_ua_parsing(self.activity)
        
  def process_exception(self, request, exception):
    self.activity.error = str(exception)
    self.activity.set_processing_time()
    self.activity.save()

  def process_response(self, request, response):
    self.activity.set_processing_time()
    self.activity.save()
    return response

