# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from wohaapi.models import Game_Sessions
from  basegd import libunlock
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

    if not profile.unlocked:
        return HttpResponse( "BANNED:Use key %s to unlock at %s" %(
                libunlock.create( username ),
                "http://gruvdrift.se/unlock/%s" % username ) )
    
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
        gs = Game_Sessions( user=user, logged_in = datetime.datetime.now(),
                            last_ping = datetime.datetime.now(), duration = 0,
                            online = True )
        gs.save()
    
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
            gs = Game_Sessions.objects.filter( user=user, online=True ).order_by( '-logged_in' )[0]
            
        except:
            continue # sadly it had timedout

        if gs.timedout():
            continue

        any_p = True
        gs.ping()

    if any_p:
        return HttpResponse( "PONG" )
    else:
        return HttpResponse( "PLONK" )

def logout( req, username ):
    def doit( username ):
        try:
            user = User.objects.get( username__iexact=username )
        except:
            return "UNF"

        try:
            gs = Game_Sessions.objects.filter( user=user ).order_by( '-logged_in' )[0]
            
        except:
            return "GSF"

        if gs.timedout() or not gs.online:
            return "ALREADY_OUT"

        gs.online = False
        gs.ping()        
        return "OK"

    ret = doit( username )
    return HttpResponse( ret )

# Non API pages
def online( req ):
    online_users = map( lambda gs: gs.user,
                        filter( lambda gs: not gs.timedout(),
                                Game_Sessions.objects.filter( online = True )
                                ))
    users_with_playtime = map( lambda p: ( p.username, p.profile.get_total_playtime(), p.profile.get_total_playtime_int(), p.profile.banned ),
                               filter( lambda p: p.profile.unlocked and p.profile.whitelisted,
                                               User.objects.all() ) )

    users_with_playtime = sorted( users_with_playtime, cmp=lambda x,y: y[2] - x[2] )

    c = RequestContext( req, { 'online_users': online_users,
                               'users_with_playtime': users_with_playtime } )
    return render_to_response( "wohaapi/online.html", c )
