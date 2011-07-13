class Memory :

	def __init__( self ) :
	
		self.__contexts = {}
		self.__stints = {}
		
	def initialize( self ) :	
	
		pass
		
	def registerStint( self, stint ) :
	
		h = stint.context.hash()
		self.__contexts[ h ] = context
		self.__stints[ ( stint.user, h ) ] = stint
	
	def removeStint( self, user, context ) :
		
		key = ( user, context.hash() )
		if key in self.__stints :
			del self.__stints[ key ]
		
	def stints( self ) :
		
		return self.__stints.values()
		
	def removeContext( self, context ) :
	
		h = context.hash()
		if h in self.__contexts :
			del self.__contexts[ h ]

	def contexts( self ) :
	
		return self.__contexts.values() 
		
	def transactionBegin( self, transactionId, lock=False ) :
	
		pass
	
	def transactionEnd( self, transactionId ) :
		
		pass