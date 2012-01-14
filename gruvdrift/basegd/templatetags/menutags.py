from django import template
register = template.Library()

@register.simple_tag
def menu_current( req, pattern ):
    if pattern == u'/':
        if pattern == req.path:
            return u'currentpage'
        else:
            return u''
    
    elif req.path.startswith( pattern ):
        return u'currentpage'
    else:
        return u''

