# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from wohaapi.models import Game_Sessions

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

def ping( req, username ):
    # update session: last_ping and online
    # if session is set to offline (via for example admin) then kick user.
    return HttpResponse( "not ready" )

def logout( req, username ):
    return HttpResponse( "not ready" )

# Non API pages
def online( req ):
    return render_to_response( "wohaapi/online.html", RequestContext( req ) )
