from wohaapi.models import Game_Sessions
from django.contrib import admin

def make_offline( modeladmin, request, queryset ):
    queryset.update( online = False )
make_offline.short_description = "Mark selected as offline"

class Game_Admin( admin.ModelAdmin ):
    list_display = ('user', 'online', 'last_ping', 'timedout' )
    actions = [ make_offline ]

admin.site.register( Game_Sessions, Game_Admin )

