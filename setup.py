#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 14:42:06 CEST 

"""Installation instructions for audit
"""

from setuptools import setup, find_packages

setup(

    name = "audit",
    version = "0.3.9", 
    packages = find_packages(),

    # we also need all translation files and templates
    package_data = {
      'audit': [
        'templates/audit/*.html',
        'locale/*/LC_MESSAGES/django.po',
        'locale/*/LC_MESSAGES/django.mo',
        ],
      },

    entry_points = {
      'console_scripts': [
        'audit_relocate.py = audit.scripts.audit_relocate:main',
        'audit_refresh_db.py = audit.scripts.audit_refresh_dbs:main',
        'audit_prune.py = audit.scripts.audit_prune:main',
        'audit_update_ua_db.py = audit.scripts.audit_update_ua_db:main',
        'audit_find_agents.py = audit.scripts.audit_find_agents:main',
        'audit_prune_bots.py = audit.scripts.audit_prune_bots:main',
        ],
      },

    zip_safe=False,

    install_requires = [
      'Django>=1.1',
      'docutils',
      'setuptools',
      'pygeoip',
      'pygooglechart',
      'dateutils',
      ],

    dependency_links = [
      'http://docutils.sourceforge.net/docutils-snapshot.tgz',
      ],

    # metadata for upload to PyPI
    author = "Andre Anjos",
    author_email = "andre.dos.anjos@gmail.com",
    description = "Provides a django application that saves site usage statistics",
    license = "PSF",
    keywords = "django usage statistics",
    url = "",   # project home page, if any

)

