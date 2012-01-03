from django import template
import re

register = template.Library()

wiki_link = re.compile( "\[([A-Za-z_]+)\]([^(])" )

@register.filter
def wikify( value ):
    """Mostly expansions to ReST so we get more recognised wiki links"""
    # wander around and fix all the links
    # TODO: add map link / image macro
    # HTML for image:
    # <div class="Wiki_image">
    # <img src="/static/img/creeper.png" /><br />
    # A creepy Creeper.
    # </div>

    output = wiki_link.sub( r'[\1](/wiki/\1)\2', value )
    return output
