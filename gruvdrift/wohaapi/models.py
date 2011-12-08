from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game_Sessions( models.Model ):
    user = models.ForeignKey( User, unique=True )
    total_time = models.DateTimeField() # total played time, added on
                                        # pings and logout.
    online = models.BooleanField()      # if set to false, kick user
                                        # on next ping
    logged_in = models.DateTimeField( 'last login' )
    logged_out = models.DateTimeField( 'last signout' )
    last_ping = models.DateTimeField()

    def __unicode__( self ):
        return self.user.username

    class Meta:
        verbose_name = 'Game Session'
        verbose_name_plural = 'Game Sessions'
