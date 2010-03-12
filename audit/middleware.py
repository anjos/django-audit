#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:28:29 CEST 

"""Code responsible for tracking the user activity in your website.
"""

from datetime import datetime
from models import UserActivity
from utils import try_set_location, try_ua_parsing
from conf import settings
import re

NOTRACK_REGEXP = [re.compile(k) for k in settings.AUDIT_NO_TRACKING]

class Activity:
  """Middleware that tracks the user activity on every website hit."""

  def process_request(self, request):

    # Checks if we need to keep track of this activity...
    request_url = request.META.get('PATH_INFO', '').strip()
    if request_url[0] == '/': request_url = request_url[1:]
    if True in [bool(k.match(request_url)) for k in NOTRACK_REGEXP]:
      self.activity = None
      return

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
    if self.activity:
      self.activity.error = str(exception)
      self.activity.set_processing_time()
      self.activity.save()

  def process_response(self, request, response):
    if self.activity:
      self.activity.set_processing_time()
      self.activity.save()
    return response

