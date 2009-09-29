#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 14:42:06 CEST 

"""Installation instructions for audit
"""

from setuptools import setup, find_packages

setup(

    name = "audit",
    version = "0.1", 
    packages = find_packages(),

    # we also need all translation files and templates
    package_data = {
      'audit': [
        'templates/audit/*.html',
        'media/db/*.dat',
        'media/db/install.sh',
        'media/db/Makefile',
        'locale/*/LC_MESSAGES/django.po',
        'locale/*/LC_MESSAGES/django.mo',
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

