from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from wiki.models import Page # maybe? Revision

# Create your views here.
def index( req ):
    #c = RequestContext( req, { 'wiki_title': "Lorem" } )
    #return render_to_response( "wiki/index.html", c )

    # later in real version
    return view( req, "Portal" )

def view( req, pagename ):
    """render and show our nice readers their requested page (if there is one)"""
    try:
        page = Page.objects.get( title__iexact=pagename )
    except:
        page = None
    
    if page:
        # try to fetch the last our last revision.
        revision = page.get_last_revision()
        page_text = None
        wiki_title = page.title.replace( '_', ' ' )
        
    else:
        revision = None
        page_text = "No such page sorry"
        wiki_title = "404 sorry"
        
    c = RequestContext( req, { 'wiki_title': wiki_title,
                               'page_text': page_text,
                               'revision': revision } )
    return render_to_response( "wiki/view.html", c )
