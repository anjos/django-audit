#!/bin/bash 
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 16:49:23 CEST

export PYTHON=`which python2.5`
start_dir=`pwd`

source ./setup.sh
./install.sh

if [ ! -d project ]; then
  django-admin.py startproject project;
  rm -f project/settings.py;
  ln -s ../settings.py project/settings.py;
  rm -f project/urls.py;
  ln -s ../urls.py project/urls.py;

  # base django project installation
  cd project;
  ${PYTHON} manage.py syncdb --noinput;
  echo "Creating superuser for tests...";
  ${PYTHON} manage.py createsuperuser --username=admin --email=andre.dos.anjos@gmail.com 
  mkdir templates;
  cd templates;
  ln -s ../../base.html .;
  ln -s ../../sw/Django*/django/contrib/admin/templates/admin/404.html .;
  ln -s ../../sw/audit*/audit/templates/audit .;
  cd ${start_dir};

  # and prepare the database for a manual inspection
  ${PYTHON} sw/audit*/audit/test_initial.py
fi

if [ ! -d media ]; then
  mkdir media;
  cd media;
  ln -s ../sw/audit*/audit/media audit;
  ln -s ../sw/Django*/django/contrib/admin/media django;
  svn co http://django-rosetta.googlecode.com/svn/trunk/rosetta/templates/rosetta rosetta
  cd ${start_dir};
fi

# update the translation strings
cd sw/audit*/audit;
django-admin.py compilemessages
cd ${start_dir};

# now run all tests
cd project;
${PYTHON} -m compileall .
${PYTHON} manage.py test audit;
# and let the webserver running
${PYTHON} manage.py runserver 8080;
cd ${start_dir};

