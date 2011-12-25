from hashlib import md5
import datetime
import settings

"""Simple library used for generating and validating onetime keys"""
def create( key ):
    now = datetime.date.today()
    skey = settings.SECRET_KEY[:min( len( settings.SECRET_KEY ) - 2, now.day )]
    ret = md5( "%d-%s-%d-%s" %( now.year, key, now.day, skey) )
    return ret.hexdigest()[2:10]

def validate( key, code ):
    ctrl_code = create( key )
    return ctrl_code == code
