#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A simple authenticating proxy against mindcraft (evil game but fun project)
# Copyright (C) 2011  Patrik Lembke <blambi@chebab.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socket, threading, select, time, ConfigParser, struct, os, random, urllib

class Client( threading.Thread ):
    def __init__( self, client_stuff, server_info ):
        self.sock = client_stuff[0]
        self.host = client_stuff[1][0]
        self.port = client_stuff[1][1]
        threading.Thread.__init__( self )
        self.server_sock = None
        self.server_info = server_info
        self.user = ""

        self.time_signin = 0
        self.time_signout = 0
        self.running = True
        self.in_game = False
        self.jailed = False
        self.lock = threading.Lock()
        self.api = WohaAPI()

    def lowlevel_send( self, data ):
        """So we don't overwelm the port client"""
        #if debug:
        #    print "sock->client: %s" % repr( data )

        self.lock.acquire()
        self.sock.sendall( data )
        self.lock.release()

    def build_string( self, string ):
        """Returns a string prefixed by a short"""
        return "%s%s" %( struct.pack( ">h", len( string ) ),
                         string.encode( 'utf-16-be' ) )

    def parse_string( self, raw_string ):
        """returns a decoded string"""
        return raw_string.decode( 'utf-16-be' )

    def send_chat( self, message, colour='f' ):
        """Use the colours dict for colour..."""

        if colour != 'f': # just standard...
            message = u"§%c%s" %( colour, message ) # HACK but works

        self.lowlevel_send( "\x03%s" % self.build_string( message ) )

    def send_kick( self, message ):
        """This kicks the current user, but you have to close him etc,
        string will be magled correctly so use raw strings. Dosn't
        work where we kill it :/"""
        self.lowlevel_send( "\xFF%s" % self.build_string( message ) )

        if self.server_sock:
            self.server_sock.sendall( "\xFF%s" % # maybe not that nice but hmm
                                      self.build_string( "Closed" ) )

    def run( self ):
        print "New thread started! %s" % threading.currentThread()
        global accountant

        buff = "kaka"
        pre_mode = True

        while buff != "" and self.running:
            buff = self.sock.recv( 1024 )
            resp = ""

            if pre_mode:
                #print "data: %s" % repr( buff )

                if buff[0] == "\x02" and self.user == "":
                    # Parse 0x02 package
                    print "init 0x02"
                    name = self.parse_string( buff[3:] )
                    print "got name: '%s'" % name

                    self.api.auth( name )

                    if self.api.banned:
                        print "Kick since it a banned one"
                        self.send_kick( "Your banned: %s" % self.api.reason )
                        break

                    if not self.api.whitelisted:
                        print "Dropping it since unknown"
                        self.send_kick( messages['not-whitelisted'] )
                        break

                    else:
                        # check if jailed
                        self.jailed = self.api.jailed
                        print "jailed? %s" % self.jailed

                        # prepare for proxy mode
                        pre_mode = False
                        self.user = name
                        self.time_signin = int( time.strftime( "%s" ) )
                        break

                if buff[0] == "\xfe" and self.user == "":
                    # Server polling
                    if os.path.exists( "serverscreen.motd" ):
                        motd = open( "serverscreen.motd", 'r' ).readlines()[0]
                    else:
                        motd = ""
                    self.send_kick( u"%s§%d§%d" %( motd, len( accountant.get_online() ), 20 ) )
                    break

                else:
                    print "unknown data: %s" % repr( buff )

                if resp:
                    self.lowlevel_send( resp )


        if not pre_mode:
            self.proxy_mode() # enter it :D

        print "Thread %s exiting" % threading.currentThread()
        try:
            self.sock.shutdown( socket.SHUT_RDWR )
            self.sock.close()
        except:
            pass

        if self.user != "":
            # log out
            self.api.logout( self.user )

    def proxy_mode( self ):
        print "Entering proxy mode for %s" % self.user
        # create a connection against server here add it to select inputs
        self.server_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        try:
            self.server_sock.connect( self.server_info )
        except socket.error, why:

            if why[0] in ( 111, 113 ): # Connection Refused, Not reachable
                self.send_kick( "Sorry there is a connection error to the server." )
            else:
                self.send_kick( "Unknown error type (%d), but hey maybe meta is drunk" % why[0] )
            print "Server connection error: %s" % why
            return

        # make handshake
        print "sending handshakes to server"
        self.server_sock.send( "\x02%s" % self.build_string( self.user ) )

        # inputs
        inputs = [ self.sock, self.server_sock ] # add server sock

        # enter select loop
        first_pos_and_look = True

        while self.running: # break when done
            inp_ready, out_ready, xtr_ready = select.select( inputs, [], [] )

            for inp in inp_ready: # stuff that got datas for us :D
                if inp == self.sock: # from client
                    try:
                        buff = self.sock.recv( 1024 )
                    except:
                        buff = ""

                    if not buff:
                        print "%s quit" % self.user
                        self.running = False
                        self.in_game = False
                        break

                    if buff[0] == '\x0D' and first_pos_and_look:
                        print "Telling %s what other users are online" % self.user
                        first_pos_and_look = False
                        self.in_game = True
                        self.send_motd_or_warning()
                        self.send_online_users()

                    elif buff[0] == '\x03':

                        chat_str = self.parse_string( buff[1:] )[1:]

                        if chat_str.startswith( '/' ) and \
                                self.handle_chat_command( chat_str[1:] ):
                            buff = False # this is a proxy command and
                                         # server should not care...

                        if debug:
                            for x in chat_str:
                                print ord( x ),
                            print
                        print "<%s> %s" %( self.user, chat_str )


                    elif self.jailed and ( buff[0] == '\x0F' or buff[0] == '\x0E' ):
                        print "%s tried to place or dig while jailed" % self.user
                        self.send_chat( messages['jail'], colours['red'] )
                        continue

                    if buff:
                        self.server_sock.sendall( buff ) # send to the server


                    elif inp == self.server_sock:
                        buff = self.server_sock.recv( 1024 )

                    if not buff:
                        print "server quit %s" % self.user
                        self.running = False
                        self.in_game = False
                        break

                    # Just send all trough
                    self.lowlevel_send( buff )

        # close server con
        self.server_sock.shutdown( socket.SHUT_RDWR )
        self.server_sock.close()

    def send_online_users( self ):
        online_users = map( lambda x: x.user, connections )
        user_buf = list()

        for pos_user in online_users:
            if pos_user:
                user_buf.append( pos_user )

                if len( user_buf ) == 6:
                    self.send_chat( "Online: %s" %(
                        ", ".join( user_buf ) ),
                        colours['purple'] )
                    user_buf = list()
        if user_buf:
            # some left overs
            self.send_chat( "Online: %s" %(
                ", ".join( user_buf ) ),
                colours['purple'] )

    def send_motd_or_warning( self ):
        """Sends motd if file exists and isn't empty, if multi line
        only first line, if not sends a random line from our fortune
        jar, if we got a warning for this player send it instead."""
        motd = False

        if self.api.warning:
            # This user got a warning currently
            self.send_chat( self.api.warning, colours['red'] )
            return

        if os.path.isfile( "motd" ):
            rows = open( "motd", 'r' ).readlines()[:1]

            if rows and len( rows[0] ) > 5: # not empty or near empty
                motd = True
                self.send_chat( rows[0], colours['red'] )

        if not motd and os.path.isfile( "fortune" ):
            fortunes = filter( lambda x: len( x ) > 5,
                        open( "fortune", 'r' ).readlines() )
            fortunes = map(lambda x: x.rstrip('\n'), fortunes)

            if fortunes: # only if fortunes isn't empty
                self.send_chat( random.choice( fortunes ), colours['cyan'] )

    def kill_connection( self, why ):
        """Kicks and kills the connection, to be used by the main thread"""
        self.send_kick( why )
        self.running = False
        self.in_game = False


    # -- Command handling
    def handle_chat_command( self, command ):
        if not debug: # Not stable yet
            return False
        # Returns true if we handle this internally.
        aliases = { 'who': self.chat_cmd_who,
                    'online': self.chat_cmd_who,
                    'motd': self.chat_cmd_motd }

        # split into arguments and op parts
        if command.find( ' ' ) == -1: # no args
            cmd = command
            args = []

        else:
            cmd, args = command.split( ' ', 1 )
            args = args.split( ' ' )

        if not aliases.has_key( cmd ):
            print "%s not a command here... passing on" % cmd
            return False

        aliases[cmd]( args )

        return True


    def chat_cmd_who( self, args ):
        self.send_online_users()

    def chat_cmd_motd( self, args ):
        self.send_motd()

class WohaAPI:
    def __init__( self ):
        global wohaapi_url
        self.url = wohaapi_url
        self.warning = str()
        self.banned = False
        self.jailed = False
        self.reason = str()
        self.whitelisted = False

    def __llget( self, url ):
        ret = urllib.urlopen( url ).read()
        if debug:
            print "API: %s -> %s" %( url, ret )
        return ret

    def auth( self, username ):
        resp = self.__llget( self.url + "auth/" + username + "/" )
        flags = resp.split( "|" )[1:]

        #if resp == "NOT_WHITELISTED": Noo need to catch this one
        #    return

        if resp.startswith( "BANNED" ):
            self.banned = True
            self.reason = resp.split( ':', 1 )[1]

        elif resp.startswith( "OK" ):
            self.whitelisted = True

            for flag in flags:
                if flag == "JAILED":
                    self.jailed = True
                elif flag.startswith( "WARNING" ):
                    self.warning = flag.split( ':' )[1]

    def logout( self, username ):
        resp = self.__llget( self.url + "logout/" + username + "/" )

    def ping( self, usernames ):
        """Returns false if one or more of the pinged users have timedout"""
        pingstr = "|".join( usernames )
        resp = self.__llget( self.url + "ping/" + pingstr )

        # do stuff!
        if resp == "PONG":
            return True
        return False


class Accountant( threading.Thread ):
    def __init__( self ):
        # add db stuff here later?
        print "Accountant is waking up"
        self.time_log = list()
        self.last_seen = list()
        self.api = WohaAPI()
        self.lock = threading.Lock()
        self.time_lock = threading.Lock()
        threading.Thread.__init__( self )

    def run( self ):
        print "Accountant is up and running"

        self.stop_it = False
        online_counter = 60 # used below to as how often we should
                            # write who is online
        while not self.stop_it:
            time.sleep( 1 ) # really enough

            online_counter -= 1
            if online_counter <= 0:
                online_counter = 60
                self.write_online_list()
                self.wohaapi_ping()

        print "Accountant dieing"

    def get_online( self ):
        return map( lambda x: x.user,
                    filter( lambda x: x.in_game, connections ) )

    def write_online_list( self ):
        self.time_lock.acquire()
        online_users = self.get_online()

        if online_users and self.last_seen != online_users:
            print "Accountant sees that %s is online, and is writing that down" %( ", ".join( online_users ) )

        # hack
        if self.last_seen != online_users:
            online_file = open( "online", 'w+' )
            self.last_seen = list()

            for pos_user in online_users:
                if pos_user:
                    online_file.write( pos_user + "\n" )
                    self.last_seen.append( pos_user )
            online_file.close()

        self.time_lock.release()

    def wohaapi_ping( self ):
        print "Accountant PINGs wohaapi server"
        self.time_lock.acquire()
        online_users = self.get_online()

        if online_users:
            self.api.ping( online_users )

        self.time_lock.release()


## helpers
def safe_conf( sect, opt, default = None, is_int = False ):
    if not conf.has_option( sect, opt ) and default == None:
        print "Error in wohasock.conf option missed in section %s, option %s" %(
            sect, opt)
        exit( 1 )

    elif not conf.has_option( sect, opt ):
        return default

    if not is_int:
        return conf.get( sect, opt )
    else:
        return conf.getint( sect, opt )

colours = { 'black': '0', 'dark blue': '1', 'dark green': '2',
            'dark cyan': '3', 'dark red': '4', 'purple': '5',
            'gold': '6', 'gray': '7', 'dark gray': '8',
            'blue': '9', 'bright green': 'a', 'cyan': 'b',
            'red': 'c', 'pink': 'd', 'yellow': 'e', 'white': 'f' }

# --- main ---

# Read in config file
conf = ConfigParser.ConfigParser()
conf.read( "wohasock.conf" )

connections = list()
#server_info = ( "gruvdrift.se", 25565 ) # testing
server_info = ( safe_conf( "server", "host", default = "" ),
                safe_conf( "server", "port", is_int = True ) )
bind_info = ( safe_conf( "proxy", "host", default = "" ),
              safe_conf( "proxy", "port", is_int = True ) )
debug = bool( safe_conf( "proxy", "debug", False, True ) )

messages = {
    "jail": safe_conf( "messages", "jail", default = "Your in jail!" ),
    "not-whitelisted": safe_conf( "messages", "not-whitelisted", default = "Sorry not in whitelist :(" )
    }

wohaapi_url = safe_conf( "config", "wohaapi-url" )

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, True )

try:
    sock.bind( bind_info )
    sock.listen( True )
except socket.error, why:
    print "Noes, wohasock failed since: %s" % why
    exit( 1 )

print "wohasock up clients will be sent to %s:%d" %( server_info[0],
                                                     server_info[1] )
print "wohaapi at %s" % wohaapi_url

if debug:
    print "In debug mode"

accountant = Accountant()
accountant.start()

try:
    while True:
        client_stuff = sock.accept()
        print "New connection from %s:%d" %( client_stuff[1][0], client_stuff[1][1] )
        connections.append( Client( client_stuff, server_info ) )
        connections[-1].start()

        connections = filter( lambda x: x.isAlive(), connections )
        print "%d active threads" % threading.activeCount()

except KeyboardInterrupt:
    print "Keyboard smashed the place up, so we have to kill threads now"
    accountant.stop_it = True

    for client in connections:

        if client.in_game:
            if client.user:
                print "Killing connection for %s" % client.user
            client.kill_connection( "Server going down, sorry.." )

sock.shutdown( socket.SHUT_RDWR )
sock.close()
