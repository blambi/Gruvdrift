from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Example:
    # (r'^gruvdrift/', include('gruvdrift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # pile of placeholders
    (r'^signup/$', 'basegd.views.placeholder' ),
    (r'^market/.*', 'basegd.views.placeholder' ),

    # our homebaked site
    (r'^auth/$', 'basegd.views.auth'),
    (r'^unlock/(?P<username>\w+)$', 'basegd.views.unlock'),
    (r'^wohaapi/', include( 'wohaapi.urls' )),
    (r'^wiki/', include( 'wiki.urls' )),
    (r'^online/$', 'wohaapi.views.online' ),
    (r'^profile/(?P<username>\w+)$', 'basegd.views.profile' ),
    (r'^map/$', 'maps.views.index' ),
    (r'^$', 'news.views.index'),
)

if settings.DEBUG and settings.LDEVPATH:
    urlpatterns += patterns(
        'django.views.static',
        (r'^static/(?P<path>.*)$', 
         'serve', {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True }),
        )
