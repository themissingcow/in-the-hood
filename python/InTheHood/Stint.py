from datetime import datetime

class Stint :

	def __init__( self ) :
	
		self.user = None
		self.context = None
		self.timestamp = None
		self.expires = None
		
	def __str__( self ) :
	
		return "%s @ %s: %s" % ( self.user, self.timestamp, self.context )
		
	def expired( self, refTime=None ) :
	
		if self.expires is None :
			return False
	
		if refTime is None :
			refTime = datetime.now()
			
		return True if self.expires < refTime else False