# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def index( req ):
    c = dict()
    opts = list()
    
    if req.GET.has_key('world'):
        opts.append("worldname=%s" % req.GET['world'])
    if req.GET.has_key('map'):
        opts.append("mapname=%s" % req.GET['map'])

    if req.GET.has_key('x') and len(req.GET['x'] ) > 0:
        opts.append("x=%d" % int(req.GET['x']))
    else:
        opts.append("x=0")

    if req.GET.has_key('z') and len(req.GET['z'] ) > 0:
        opts.append("z=%d" % int(req.GET['z']))
    else:
        opts.append("z=0")

    if req.GET.has_key('zoom'):
        opts.append("zoom=%d" % int(req.GET['zoom']))


    c['options'] = "&".join(opts)
    
    return render_to_response( "maps/index.html", RequestContext( req, c ) )
