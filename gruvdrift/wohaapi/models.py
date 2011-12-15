from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Game_Sessions( models.Model ):
    user = models.ForeignKey( User, unique=False )
    logged_in = models.DateTimeField()
    last_ping = models.DateTimeField()
    duration = models.PositiveIntegerField()
    #online = models.BooleanField()
    
    def __unicode__( self ):
        return self.user.username

    def ping( self ):
        t_now = datetime.datetime.now()
        self.last_ping = t_now
        t_delta = t_now - self.logged_in
        self.duration = t_delta.seconds
        self.save()
        
    def timedout( self ):
        t_out = datetime.datetime.now() - datetime.timedelta( minutes=2 )
        return self.last_ping < t_out
        
    class Meta:
        verbose_name = 'Game Session'
        verbose_name_plural = 'Game Sessions'
