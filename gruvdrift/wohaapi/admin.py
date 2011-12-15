from wohaapi.models import Game_Sessions
from django.contrib import admin

class Game_Admin( admin.ModelAdmin ):
    list_display = ('user', 'last_ping', 'timedout')

admin.site.register( Game_Sessions, Game_Admin )

