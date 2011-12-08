# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
import settings
import os

def index( req ):
    class MapImage:
        def __init__( self, x, y, sx, sy ):
            if os.path.exists( "%smaps/0.%d.%d.png" %( settings.MEDIA_ROOT, x, y ) ):
                self.img = "maps/0.%d.%d.png" %( x, y )
            else:
                self.img = "img/map-empty.png"

            self.center = False
            self.x = x - sx
            self.y = y - sy
                                       
    # read center from json
    if not os.path.exists( "%smaps/json.js" % settings.MEDIA_ROOT ):
        sx = 16
        sy = 13
    else:
        js_data = file( "%smaps/json.js" % settings.MEDIA_ROOT,
                        'r' ).read()
        js_obj = json.loads( js_data[16:-1] )
        sx = int( js_obj['world']['cx'] ) / 300
        sy = int( js_obj['world']['cy'] ) / 300

    # calc centers
    if req.GET.has_key( 'x' ) and req.GET.has_key( 'y' ) and \
            req.GET['x'].strip('-').isdigit() and \
            req.GET['y'].strip('-').isdigit():
        cx = int( req.GET['x'] ) + sx
        cy = int( req.GET['y'] ) + sy

    else:
        cx = 0 + sx
        cy = 0 + sy

    # generate map part list
    parts = list()
    for y in range( cy -1, cy +2 ):
        parts.append( list() )
        for x in range( cx -1, cx +2 ):
            parts[-1].append( MapImage( x, y, sx, sy ) )

            if x == cx and y == cy:
                parts[-1][-1].center = True
    
    c = { 'parts': parts }
    return render_to_response( "maps/index.html", RequestContext( req, c ) )
