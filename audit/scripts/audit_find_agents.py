#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Sun 14 Feb 17:07:40 2010 

"""A script to be executed to find a match for user agents 
"""

import os, sys, re

# setup Python
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
  os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from audit.models import UserAgent, UserActivity

def main():
  """Tries to match the UserActivity with some UserAgent string."""

  # by default we only look at requests w/o agents attached, but we can do a
  # full reset as well, if the user provides 'full' as first argument
  objects = UserActivity.objects.filter(agent=None)
  if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'full':
      objects = UserActivity.objects.all()
    else:
      print 'usage: %s [full]' % sys.argv[0]
      sys.exit(1)

  # compiles the regular expressions from our user agent tables
  ua = {}
  for k in UserAgent.objects.all(): ua[k] = re.compile(k.regexp, re.IGNORECASE)

  for k in objects:
    curr = None
    for agent, regexp in ua.iteritems():
      if regexp.search(k.browser_info): 
        if not curr: curr = agent
        elif len(agent.regexp) > len(curr.regexp): curr = agent
    if curr: #save a match
      k.agent = curr
      k.save()

if __name__ == '__main__':
  main()
