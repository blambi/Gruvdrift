from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def index( req ):
    c = RequestContext( req, { 'wiki_title': "Lorem" } )
    return render_to_response( "wiki/index.html", c )
