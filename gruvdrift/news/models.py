from django.db import models

# Create your models here.
class News_Post( models.Model ):
    pub_date = models.DateTimeField( 'date published' )

    def __unicode__( self ):
        return self.pub_date.strftime( "%Y-%m-%d %H:%M" )

class News_Item( models.Model ):
    news_post = models.ForeignKey( News_Post )
    text = models.CharField( max_length = 200 )

    def __unicode__( self ):
        return self.text
