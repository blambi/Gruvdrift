from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'wiki.views',
    url( r'^$', 'index' ),
    # other actions
    url( r'^edit/(?P<pagename>[\w]+)$', 'edit' ),
    url( r'^(?P<pagename>[\w]+)$', 'view' ),
    )
