from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'wiki.views',
    url( r'^$', 'index' ),
    url( r'^updates$', 'updates' ),
    url( r'^history/(?P<pagename>[\w]+)$', 'list_history' ),
    url( r'^history/(?P<pagename>[\w]+)/(?P<rev_id>\d+)$', 'view_history' ),
    url( r'^edit/(?P<pagename>[\w]+)$', 'edit' ),
    url( r'^ajax/edit_preview/$', 'ajax_edit_preview' ),
    url( r'^(?P<pagename>[\w]+)$', 'view' ),
    )
