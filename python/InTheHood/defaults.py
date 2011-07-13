from datetime import timedelta

self.setKey( "hood/name", "The Massif" )

#from Backend import Memory as m
from Backend.MySql import MySql as m
sql = m( "localhost", "inthehood", "inTheHood", "inTheHood" )

self.setKey( "global/store", sql )

self.setKey( "global/janitorInterval", 300 )

self.setKey( "checkin/defaultTimeout", timedelta( minutes=30 ) )

self.setKey( "hood/defaultContext/host", "os.getenv('HOST')" )
self.setKey( "hood/defaultContext/directory", "os.getenv('PWD')" )



