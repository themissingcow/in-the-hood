#  Copyright (c) 2011, Tom Cowland. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#  
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#  
#      * Neither the name Tom Cowland nor the names of any
#        other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
		
	
		
		