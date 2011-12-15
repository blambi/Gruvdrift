from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'wohaapi.views',
    url( r'^auth/(?P<username>\w+)/$', 'auth' ),
    url( r'^ping/(?P<users>[|\w]+)$', 'ping' ),
    url( r'^logout/(?P<username>\w+)/$', 'logout' ),
    )
