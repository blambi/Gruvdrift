from news.models import News_Post, News_Item
from django.contrib import admin

class News_Item_Inline( admin.TabularInline ):
    model = News_Item
    extra = 1
    
class News_Admin( admin.ModelAdmin ):
    fields = [ 'pub_date' ]
    inlines = [ News_Item_Inline ]

admin.site.register( News_Post, News_Admin )

