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

    # basegd (move to separate file later)
    (r'^auth/$', 'basegd.views.auth'),
    (r'^$', 'news.views.index'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^static/(?P<path>.*)$', 
         'serve', {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True }),
        )
