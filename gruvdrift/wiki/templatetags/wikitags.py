from django import template
from django.utils.html import escape, strip_tags
import re

register = template.Library()

wiki_link = re.compile( "\[([A-Za-z_]+)\]([^(])" )

wiki_image = re.compile( "\[(.*?)\]\((.*?)\)" )
wiki_image_template = """<div class="Wiki_image">
  <a href="%(link)s"><img src="%(link)s" /></a>
  <p>%(text)s</p>
</div>"""

@register.filter
def wikify( value ):
    """Mostly expansions to ReST so we get more recognised wiki links"""
    # wander around and fix all the links
    # TODO: add map link / image macro

    
    output = wiki_link.sub( r'[\1](/wiki/\1)\2', value )

    for title, link in wiki_image.findall( output ):
        if link.endswith( '.png' ) or link.endswith( '.jpeg' ) or link.endswith( '.jpg' ):
            # we got an image
            output = output.replace( "[%s](%s)" %( title, link ),
                                     wiki_image_template % {
                    'link': strip_tags( link ),
                    'text': escape( title ) } )
    return output
