#!/bin/bash 
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 23 Set 2009 14:51:58 CEST

country_bin=http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
city_bin=http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
country_csv=http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
city_csv=http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity_`date +%Y%m`01.zip
timeout=20 #seconds

function download_install () {
  local name=`basename $3`;
  if [ ! -e `basename $3 .$2` ]; then
    echo "Downloading ${name}...";
    wget --timeout=${timeout} --tries=1 $3;
    if [ $? = 0 ]; then
      $1 -d `basename ${name}`;
    else
      echo "ERROR: Could not download file after ${timeout} seconds!";
    fi
  else
    local final=`basename $3 .$2`;
    echo "INFO: The file ${final} is already available. Skipping.";
  fi
}

download_install gunzip gz ${country_bin}
download_install gunzip gz ${city_bin}
#download_install unzip zip ${country_csv}
#download_install unzip zip ${city_csv}

exit 0;
