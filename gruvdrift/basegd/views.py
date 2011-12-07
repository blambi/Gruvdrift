from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import logout, authenticate, login
from django.template import RequestContext

# Create your views here.
def index( req ):
    return render_to_response( "basegd/index.html", RequestContext( req ) )

def auth( req ):
    # do logout if user is logged in, else show loggin form
    # if we get login request login, log them in.

    if req.user.is_authenticated():
        # Do something for authenticated users.
        logout( req )
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
                    return HttpResponseRedirect( '/' ) # just root
                
                else:
                    # Return a 'disabled account' error message
                    login_failed = "Your account is disabled for some reason."
                
            else:
                # Return an 'invalid login' error message.
                login_failed = "Sorry, but that isn't a valid login request dear sir"
            
        else:
            # nothing else since that's just showing login form
            login_failed = False

    c = RequestContext( req, { 'login_failed': login_failed } )
    return render_to_response( "basegd/auth.html", c )
