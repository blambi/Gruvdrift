# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
import settings
import os

def index( req, view = "iso" ):
    modes = ["top", "oblique", "obliqueangle", "isometric"]
    # This translates between images indexes and our map coords.
    magic_num = { 'top': 100, 'iso': 300 }
    class MapImage:
        def __init__( self, x, y, sx, sy, view ):
            if os.path.exists( "%smaps/%s/0.%d.%d.png" %( settings.MEDIA_ROOT, view, x, y ) ):
                self.img = "maps/%s/0.%d.%d.png" %( view, x, y )
            else:
                self.img = "img/map-empty.png"

            self.center = False
            self.x = x - sx
            self.y = y - sy
    
    # Fix which view to use if none or a bad one use iso.
    if not view in ["iso", "top"]:
        view = "iso"
    
    otherview = "top"
    if view == "top":
        otherview = "iso"
                                       
    # read center from json
    if not os.path.exists( "%smaps/%s/json.js" % (settings.MEDIA_ROOT, view) ):
        sx = 16
        sy = 13
    else:
        js_data = file( "%smaps/%s/json.js" % (settings.MEDIA_ROOT, view),
                        'r' ).read()
        js_obj = json.loads( js_data[16:-1] )
        sx = int( js_obj['world']['cx'] ) / magic_num[view]
        sy = int( js_obj['world']['cy'] ) / magic_num[view]

    # calc centers
    urlx = 0
    urly = 0
    if req.GET.has_key( 'x' ) and req.GET.has_key( 'y' ) and \
            req.GET['x'].strip('-').isdigit() and \
            req.GET['y'].strip('-').isdigit():
        urlx = int( req.GET['x'] )
        urly = int( req.GET['y'] )

    cx = urlx + sx
    cy = urly + sy

    # generate map part list
    parts = list()
    for y in range( cy -1, cy +2 ):
        parts.append( list() )
        for x in range( cx -1, cx +2 ):
            parts[-1].append( MapImage( x, y, sx, sy, view ) )

            if x == cx and y == cy:
                parts[-1][-1].center = True
    
    c = { 'parts': parts , 'otherview':otherview, 'x':urlx, 'y':urly}
    return render_to_response( "maps/index.html", RequestContext( req, c ) )
