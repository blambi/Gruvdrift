from django.http import HttpResponse
from django.shortcuts import render_to_response

# Create your views here.
def index( req ):
    return HttpResponse( "Hi there nothing here yet" )

def auth( req ):
    # do logout if user is logged in, else show loggin form
    # if we get login request login, log them in.
    
    return render_to_response( "basegd/auth.html" )
