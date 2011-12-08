from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from news.models import News_Post

# Create your views here.
def index( req ):
    latest_news = News_Post.objects.all().order_by( '-pub_date' )[:5]
    c = { 'latest_news': latest_news }
    return render_to_response( "news/index.html", RequestContext( req, c ) )
