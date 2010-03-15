#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 18:01:52 CEST 

"""Views for site statistics, just as an example on what you can do.
"""

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from conf import settings

@permission_required('audit.view_audit')
def fidelity(request, months=settings.AUDIT_MONTHS_TO_SHOW, 
    template_name='audit/fidelity.html'):
  """General view of the current statistics for user fidelity."""
  return render_to_response(template_name, { 'months': months, },
                            context_instance=RequestContext(request))

@permission_required('audit.view_audit')
def popularity(request, months=settings.AUDIT_MONTHS_TO_SHOW, 
    template_name='audit/popularity.html'):
  return render_to_response(template_name, { 'months': months, },
                            context_instance=RequestContext(request))


@permission_required('audit.view_audit')
def identity(request, months=settings.AUDIT_MONTHS_TO_SHOW, 
    template_name='audit/identity.html'):
  return render_to_response(template_name, { 'months': months, },
                            context_instance=RequestContext(request))

@permission_required('audit.view_audit')
def performance(request, months=settings.AUDIT_MONTHS_TO_SHOW, 
    template_name='audit/performance.html'):
  return render_to_response(template_name, { 'months': months, },
                            context_instance=RequestContext(request))
