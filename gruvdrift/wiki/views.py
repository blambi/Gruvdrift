from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import datetime
from wiki.models import Page, Revision

# Create your views here.
def index( req ):
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
        page_text = "New page to create edit this entry."
        wiki_title = pagename
        
        
    c = RequestContext( req, { 'wiki_title': wiki_title,
                               'pagename': pagename,
                               'page_text': page_text,
                               'revision': revision } )
    return render_to_response( "wiki/view.html", c )

@login_required
def ajux( req ):
    # TODO: implement me!
    return

@login_required
def edit( req, pagename ):
    try:
        page = Page.objects.get( title__iexact=pagename )
    except:
        page = None

    if req.POST.has_key( 'body' ): # We should save something
        #if req.POST.has_key( 'base_rev' ):
        # ^ TODO: Add super merging fun time.
        # ^ TODO: Add op-only check.
        
        if not page:
            page = Page( title=pagename, op_only=False )
            page.save()
        
        rev = Revision( author=req.user, pub_date=datetime.datetime.now(),
                        body = req.POST['body'], page=page )
        rev.save()
        return HttpResponseRedirect( "/wiki/%s" % pagename )
    
    if page:
        # try to fetch the last our last revision.
        revision = page.get_last_revision()
        wiki_title = page.title.replace( '_', ' ' )
        
    else:
        revision = None
        wiki_title = pagename.replace( '_', ' ' )

    c = RequestContext( req, { 'wiki_title': wiki_title,
                               'pagename': pagename,
                               'revision': revision } )
    
    return render_to_response( "wiki/edit.html", c )
