from django.db import models
from django.contrib.auth.models import User

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


User.profile = property( lambda u: UserProfile.objects.get_or_create( user=u )[0] )
