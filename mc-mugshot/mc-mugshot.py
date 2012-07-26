#!/usr/bin/env python
import Image, sys, urllib, StringIO, time


class Mugshooter:
    def __init__( self, api_url, bg_colour ):
        self.api_url = api_url
        self.bg_colour = bg_colour
        self.names = []
        
    def get_names( self ):
        try:
            file_url = urllib.urlopen( self.api_url + 'list/users' )
            self.names = file_url.read().split(', ')
            file_url.close()
        except:
            return None
        self.names.reverse()
        return self.names

    def process_one( self, name = None ):
        """If a name is set it will process that specific user else it will pop one from the names array"""
        url = "http://www.minecraft.net/skin/"
        
        if not name:
            if not self.names: # if its empty
                return (None, None)
            name = self.names.pop()
            
        url += name + '.png'

        file_url = urllib.urlopen( url )

        if file_url.getcode() != 200:
            return (name, None)

        file_img = StringIO.StringIO( file_url.read() )
        file_url.close()

        # Now when we have the image lets chop it up and 
        raw = Image.open( file_img )

        # make parts
        head = raw.crop( ( 8, 8, 16, 16 ) )
        head_thing = raw.crop( ( 40, 8, 48, 16 ) )
        arm = raw.crop( ( 44, 20, 48, 32 ) )
        torso = raw.crop( ( 20, 20, 28, 32 ) )

        # assemble our output image
        target = Image.new( "RGBA", ( 18, 18 ), self.bg_colour )

        target.paste( head, ( 5, 2, 13, 10 ) )
        target.paste( torso, ( 5, 10, 13, 22 ) )
        target.paste( arm, ( 1, 10, 5, 22 ) )
        target.paste( arm, ( 13, 10, 17, 22 ) )

        # We have to avoid trying this on images without an alpha
        # layer As far as I know MC doesn't show mask/hat layer if
        # there is no alpha layer.
        if 'A' in head_thing.getbands():
            r,g,b,a = head_thing.split()
            target.paste( head_thing, ( 5, 2, 13, 10 ), mask=a )

        done = target.resize( (64, 64) )

        # Return ready buffer
        return (name, done)

# --- Main --
if __name__ == '__main__':
    if len( sys.argv ) <= 2:
        print "usage: mc-mugshot.py http://.../wohaapi/ out_folder"
        exit( 1 )

    url = sys.argv[1]
    out_folder = sys.argv[2]

    shooter = Mugshooter( url, '#D3CCED' )

    if not shooter.get_names():
        sys.stderr.write( "Error: Failed to fetch any usernames from %s/list/users\n" % url )
        exit( 2 )

    while shooter.names:
        nick, img = shooter.process_one()
        
        if img:
            img.save( out_folder + nick + '.png' )
        else:
            sys.stderr.write( "%s doesn't have a skin or we couldn't fetch it\n" % nick )

