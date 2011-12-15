# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from wohaapi.models import Game_Sessions

import datetime

def auth( req, username ):
    try:
        user = User.objects.get( username__iexact=username )
    except:
        return HttpResponse( "NOT_WHITELISTED" )

    profile = user.get_profile()
    ret = "FAIL" 

    if profile.banned:
        return HttpResponse( "BANNED:%s" % profile.ban_reason )
    
    if profile.whitelisted and user.is_active: # is active is a super disable:
        ret = "OK"
        if profile.jailed:
            ret += "|JAILED"

        if profile.warning.strip(): # remove emtpy ones...
            ret += "|WARNING:%s" % profile.warning
    else:
        ret = "NOT_WHITELISTED"


    if ret.startswith( "OK" ):
        # add to online list
        pass
    
    return HttpResponse( ret )

def ping( req, users ):
    # update sessions
    any_p = False
    if users.find( '|' ) != -1:
        users = users.split('|')
    else:
        users = [ users ]

    for u in users:
        try:
            user = User.objects.get( username__iexact=u )
        except:
            continue # just skip bad ones...

        try:
            #timeout = datetime.datetime.now() - datetime.timedelta( minutes=2 )
            #gs = Game_Sessions.objects.get( user=user, last_ping__lt = timeout )
            gsx = Game_Sessions.objects.filter( user=user )
            gs = filter( lambda x: not x.timedout(), gsx )
            #last_ping < timeout, gsx ) #timedout()
            
        except:
            continue # sadly it had timedout

        any_p = True
        if gs == []:
            continue
        
        for x in gs:
            x.ping()
        #gs.ping()

    if any_p:
        return HttpResponse( "PONG" )
    else:
        return HttpResponse( "PLONK" )

def logout( req, username ):
    return HttpResponse( "not ready" )

# Non API pages
def online( req ):
    return render_to_response( "wohaapi/online.html", RequestContext( req ) )
