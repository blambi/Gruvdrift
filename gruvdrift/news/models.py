from django.db import models

# Create your models here.
class News_Post( models.Model ):
    pub_date = models.DateTimeField( 'date published' )

    def __unicode__( self ):
        return self.pub_date.strftime( "%Y-%m-%d %H:%M" )

    class Meta:
        verbose_name = 'News Post'
        verbose_name_plural = 'News Posts'

class News_Item( models.Model ):
    news_post = models.ForeignKey( News_Post )
    text = models.CharField( max_length = 200 )

    def __unicode__( self ):
        return self.text

    class Meta:
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'
