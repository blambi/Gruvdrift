from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game_Sessions( models.Model ):
    user = models.ForeignKey( User, unique=True )
    total_time = models.DateTimeField() # total played time, added on
                                        # pings and logout.
    online = models.BooleanField()      # if set to false, kick user
                                        # on next ping
    logged_in = models.DateTimeField( 'date published' )
    last_ping = models.DateTimeField()
