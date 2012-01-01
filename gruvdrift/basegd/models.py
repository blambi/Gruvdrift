from django.db import models
from django.contrib.auth.models import User
from wohaapi.models import Game_Sessions
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    whitelisted = models.BooleanField( default=False )
    jailed = models.BooleanField( default=False )
    banned = models.BooleanField( default=False )
    # check if user haven't unlocked their account
    unlocked = models.BooleanField( default=False )
    ban_reason = models.CharField( max_length = 100, blank = True )
    warning = models.CharField( max_length = 100, blank = True )
    invited_by = models.ForeignKey( User, null = True, related_name="invitee" )

    def get_total_playtime( self ):
        try:
            gs = Game_Sessions.objects.filter( user=self.user ).order_by( 'logged_in' )
        except:
            return None # NO playtime to report


        total_playtime = 0

        for g in gs:
            total_playtime += g.duration

        # Will just build a string then
        hours = total_playtime / 3600
        mins  = total_playtime / 60 % 60
        secs  = total_playtime % 60

        if hours > 1 or hours == 0:
            ret = "%d hours, %d minutes and %d seconds." %( hours, mins, secs )
        else:
            ret = "%d hour, %d minutes and %d seconds." %( hours, mins, secs )
        return ret

User.profile = property( lambda u: UserProfile.objects.get_or_create( user=u )[0] )
