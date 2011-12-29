from wiki.models import Page, Revision
from django.contrib import admin

class Revision_Inline( admin.TabularInline ):
    model = Revision
    extra = 1
    
class Page_Admin( admin.ModelAdmin ):
    fields = [ 'title', 'op_only' ]
    inlines = [ Revision_Inline ]
    list_display = ('title', 'op_only' )

admin.site.register( Page, Page_Admin )


