from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from basegd.models import UserProfile
import libunlock
import settings
import os

# Create your views here.
def index( req ):
    return render_to_response( "basegd/index.html", RequestContext( req ) )

def placeholder( req ):
    return render_to_response( "basegd/notready.html", RequestContext( req ) )

def auth( req ):
    # do logout if user is logged in, else show loggin form
    # if we get login request login, log them in.

    if req.GET.has_key( 'next' ) and req.GET['next'].startswith( '/' ):
        next_uri = req.GET['next']
    elif req.POST.has_key( 'next' ) and req.POST['next'].startswith( '/' ):
        next_uri = req.GET['next']
    else:
        next_uri = None

    if req.user.is_authenticated():
        # Do something for authenticated users.
        logout( req )
        if req.GET.has_key( 'next' ) and req.GET['next'].startswith( '/' ):
            return HttpResponseRedirect( req.GET['next'] )
        
        return HttpResponseRedirect( '/' ) # just root
    
    else:
        # handle login
        if req.POST.has_key( 'user' ) and req.POST.has_key( 'pass' ):

            username = req.POST['user']
            password = req.POST['pass']
            
            user = authenticate( username=username, password=password )
            
            if user is not None:
                if user.is_active:
                    login( req, user )
                    # yay we have an user here :D
                    if not next_uri:
                        return HttpResponseRedirect( '/' ) # just root
                    else:
                        return HttpResponseRedirect( next_uri )
                
                else:
                    # Return a 'disabled account' error message
                    login_failed = "Your account is disabled for some reason."
                
            else:
                # Return an 'invalid login' error message.
                login_failed = "Sorry, but that isn't a valid login request dear sir"
            
        else:
            # nothing else since that's just showing login form
            login_failed = False

    c = RequestContext( req, { 'login_failed': login_failed, 'next': next_uri } )
    return render_to_response( "basegd/auth.html", c )

def unlock( req, username ):
    """Used for unlocking new accounts (they get the unlock code from MC kick"""
    unlock_failed = ""

    user = get_object_or_404( User, username__iexact=username )
    profile = user.get_profile()
    
    if profile.unlocked:
        unlock_failed = "Your already unlocked."
        #unlock_failed = libunlock.create( username )
    
    if req.POST.has_key( 'code' ) and req.POST.has_key( 'pass' ) and \
            req.POST.has_key( 'pass2' ):
        # Check code
        if libunlock.validate( username, req.POST['code'] ):
            pass
        else:
            unlock_failed = "Nope that code wan't valid"

        if req.POST['pass'] == req.POST['pass2']:
            # set password and check profile unlock
            profile.unlocked = True
            profile.save()
            user.set_password( req.POST['pass'] )
            user.save()
            c = RequestContext( req, { 'username': username } )
            return render_to_response( "basegd/unlock-unlocked.html", c )
        else:
            unlock_failed = "Password mismatch."
    
    c = RequestContext( req, { 'unlock_failed': unlock_failed } )
    return render_to_response( "basegd/unlock.html", c )

def profile( req, username ):
    user = get_object_or_404( User, username__iexact=username )
    profile = user.get_profile()

    invitees = UserProfile.objects.filter( invited_by = user )

    if os.path.exists( settings.MEDIA_ROOT + 'cache/' + profile.user.username + '.png' ):
        image_name = profile.user.username
    else:
        image_name = 'char'
    
    c = RequestContext( req, { 'profile': profile, 'invitees': invitees, 'image_name': image_name } )
    return render_to_response( "basegd/profile.html", c )
