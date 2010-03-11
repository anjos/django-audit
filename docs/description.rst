Audit is a Django application that monitors website traffic and activites,
reporting you usage statistics. Audit has graphics support using using
PyGoogleChart_ and Geographical location support using PyGeoIP_ from (MaxMind).
It parses user agents with the help of the execellent UAsParser_. Here are a 
few of its features:

* Can classify browser types and robots, filtering requests and displaying
  selected content;
* Per country and per city access for logged in and anonymous users;
* Displays website answer time response as an histogram;
* Displays popular URLs and usage hours;
* Tracks user fidelity;
* Piecharts and graphics support.

.. _PyGoogleChart: http://pygooglechart.slowchop.com
.. _PyGeoIP: http://www.maxmind.com/app/python
.. _UAsParser: http://user-agent-string.info/download/
