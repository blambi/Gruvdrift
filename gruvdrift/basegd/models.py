from django.db import models
from django.contrib.auth.models import User
from wohaapi.models import Game_Sessions
from django.db.models.signals import post_save
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

    def get_total_playtime_int( self ):
        """Returns an INT with the total play time, good for sorting"""
        try:
            gs = Game_Sessions.objects.filter( user=self.user ).order_by( 'logged_in' )
        except:
            return None # NO playtime to report

        total_playtime = 0

        for g in gs:
            total_playtime += g.duration

        return int( total_playtime )
    
    def get_total_playtime( self ):
        total_playtime = self.get_total_playtime_int()
        # Will just build a string then
        hours = total_playtime / 3600
        mins  = total_playtime / 60 % 60
        secs  = total_playtime % 60

        if hours > 1 or hours == 0:
            ret = "%d hours, %d minutes and %d seconds." %( hours, mins, secs )
        else:
            ret = "%d hour, %d minutes and %d seconds." %( hours, mins, secs )
        return ret


# Automatically create user profiles
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
