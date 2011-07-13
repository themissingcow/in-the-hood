from datetime import datetime

class Context :

	def __init__( self, rawContext ) :
	
		self.last = datetime.now()
		
		self.attribtues = {}
		for k in rawContext.keys() :
		
			if not rawContext[ k ] :
				continue
		
			self.attribtues[ k ] = rawContext[ k ]	
	
	def hash( self ) :
	
		import md5
		flat = ""
		for k in self.attribtues.keys() :
			flat += str(k) + str(self.attribtues[k])
		return md5.md5(  flat ).hexdigest()
		
	def __str__( self ) :
	
		text = "  ".join(
			[ "%s: %s" % ( k, self.attribtues[k] ) for k in self.attribtues.keys() ]
		)
		return "[ %s ] %s" % ( text, self.last )
		
		
	def touch( self ) :
	
		self.last = datetime.now()