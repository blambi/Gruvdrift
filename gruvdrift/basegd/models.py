from django.db import models
from django.contrib.auth.models import User
from wohaapi.models import Game_Sessions
from django.db.models.signals import post_save
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import Q
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
            reply = Game_Sessions.objects.filter( user=self.user ).aggregate(Sum('duration'))
        except:
            return 0 # NO playtime to report
        
        if reply["duration__sum"] == None:
          return 0
        
        return reply["duration__sum"]
    
    def get_average_playtime_int( self ):
        """Returns an INT with the average play time for all sessions"""
        try:
            reply = Game_Sessions.objects.filter( ~Q(duration = 0), user=self.user ).aggregate(Avg('duration'))
        except:
            return 0 # NO playtime to report
        
        if reply["duration__avg"] == None:
          return 0
        
        return reply["duration__avg"]
    
    def get_number_of_sessions( self ):
        """Returns an INT with the count of all sessions"""
        try:
            result = Game_Sessions.objects.filter( ~Q(duration = 0), user=self.user ).count()
        except:
            return 0 # NO playtime to report
        
        return result
    
    def get_total_playtime( self ):
        return self.build_time_string( self.get_total_playtime_int())
    
    def get_average_playtime( self ):
        return self.build_time_string( self.get_average_playtime_int())
      
    def build_time_string( self, total_seconds ):
        # Will just build a string then
        hours = int(total_seconds / 3600)
        mins  = int(total_seconds / 60 % 60)
        secs  = int(total_seconds % 60)
        
        hour_text = "hours"
        if hours == 1:
          hour_text = "hour"
        
        min_text = "minutes"
        if mins == 1:
          min_text = "minute"
        
        sec_text = "seconds"
        if secs == 1:
          sec_text = "second"
        
        ret = "";
        if hours > 0:
          ret += "%d %s, " %(hours, hour_text)
        if hours > 0 or mins > 0:
          ret += "%d %s and " %(mins, min_text)
        if hours > 0 or mins > 0 or secs > 0:
          ret += "%d %s" %(secs, sec_text)
        if ret != "":
          ret += "."
        else:
          ret = "None"
        
        return ret
      

# Automatically create user profiles
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
