### \todo Argument validation (a storage class should be able to assume all
###       arguments are valid).
import time

class Store :

	def __init__( self, storageClassInstance ) :
		
		self.__store = storageClassInstance
	
	def validate( self ) :
		
		for m in ( 
			"initialize",
			"registerStint",
			"removeStint",
			"stints",
			"contexts",
			"removeContext",
			"transactionBegin",
			"transactionEnd"
		) :
			if not hasattr( self.__store, m ) :
				raise RuntimeError, "Specified storage back end '%s' does not "\
					"implement the required method '%s'" % ( self.__store, m )
		
		self.__store.initialize()
		
		return True
	
	def registerStint( self, stint ) :
	
		self.__store.registerStint( stint )		
			
	def removeStint( self, user, context ) :
		
		if context :
			self.__store.removeStint( user, context )
		else :
			for c in self.contexts( user ) :
				self.__store.removeStint( user, c )
	
	def stints( self, user=None ) :
		
		if user :
		
			stints = []
		
			stints = self.__store.stints()
			for s in stints :
				if s.user == user :
					stints.append( s )
			return stints
		
		else :
		
			return self.__store.stints()

	def contexts( self, user=None ) :
		
		if user :
		
			contexts = []
		
			stints = self.__store.stints()
			for s in stints :
				if s.user == user :
					contexts.append( s.context )
		
			return contexts
		
		else :
		
			return self.__store.contexts()
	
	def removeContext( self, context ) :
	
		self.__store.removeContext( context )
		
	def transactionBegin( self, transactionId=None, lock=False ) :
	
		if not transactionId :
			transactionId = time.time()
		
		self.__lastTransaction = transactionId
		self.__store.transactionBegin( transactionId, lock )
	
	def transactionEnd( self, transactionId=None ) :
		
		if not transactionId :
			transactionId = self.__lastTransaction
			
		if not transactionId :
			raise RuntimeError, "Unable to determine the last transaction ID"
			
		self.__store.transactionEnd( transactionId )
		
	
		
		