import settings
from django.conf.urls.defaults import *
from django.contrib import admin
import audit.urls

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^audit/', audit.urls.namespaced),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    (r'^rosetta/', include('rosetta.urls')),

    # Media serving
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT,
     'show_indexes': True}
     ), 
    )
