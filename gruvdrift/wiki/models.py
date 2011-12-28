from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Revision( models.Model ):
    pub_date = models.DateTimeField( 'date published' )
    body = models.TextField()
    author = models.ForeignKey( User, unique=False )

class Page( models.Model ):
    title = models.CharField( max_length=200, unique=True )
    last_rev = models.ForeignKey( Revision )
    op_only = models.BooleanField( default=False ) # only op can write

    def __unicode__( self ):
        return self.title
