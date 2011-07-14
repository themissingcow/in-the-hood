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

from Config import Config
from Store import Store
from Context import Context
from Stint import Stint

from datetime import datetime
from time import time
import os

class Hood( object ) :

	def __init__( self, config=None ) :
		
		"""
		Create a new 'hood' for people to hang out in. The 'config' argument
		can optionally point to a python file that defines config.
		"""
		
		self.config = Config( config )
		
		store = self.config.getKey( "global/store" )
		if isinstance( store, str ) :
			store = eval( "import %s as store; return store" % store )
			
		self.__store = Store( store )
		self.__store.validate()

	def defaultContext( self ) :
	
		keys = self.config.getKeys( "hood/defaultContext" )
		
		c = {}
		
		for k in keys :
			v = eval( str(self.config.getKey(k)) )
			if v :
				c[ k.split("/")[-1] ] = v
		
		return Context( c )

	
	def checkin( self, user, context, timeout=None ) :
		
		"""
		Check a user into a context, the optional 'timeout' parameter
		should be an object that supports + with a datetime object.
		Contexts are simply { "str" : value, ... } dicts.
		Checking in starts a 'sting' in the context.
		"""
		
		if timeout is None :
			timeout = self.config.getKey( "checkin/defaultTimeout" )
		
		now = datetime.now()
		expiry = now + timeout if timeout else None
		
		if not isinstance( context, Context ) :
			context = Context( context )
		
		stint = Stint()
		stint.user = user
		stint.context = context
		stint.timestamp = now
		stint.expires = expiry
		
		self.__store.transactionBegin()
		
		self.__store.registerStint( stint )
		
		self.__store.transactionEnd()

		
	def checkout( self, user, context=None ) :
		
		"""
		Checks a user out of the specified context, or all contexts if
		context is None.
		"""
		
		if context and not isinstance( context, Context ) :
			context = Context( context )
			
		self.__store.transactionBegin()
		
		self.__store.removeStint( 
			user = user, 
			context = context
		)
		
		self.__store.transactionEnd()


	def contexts( self, user=None, readable=False ) :
	
		"""
		Returns a list of Contexts the 'hood' is aware of.
		"""
		self.__store.transactionBegin()
		
		if readable :
			return [ str(c) for c in self.__store.contexts( user ) ]
		else :
			return self.__store.contexts( user )
			
		self.__store.transactionEnd()

		
	def stints( self, user=None, context=None, expired=False, readable=False ) :
		
		"""
		Returns a list of all the stints currently in the 'hood'.
		"""
		
		self.__store.transactionBegin()
		
		stints = self.__store.stints()
		
		if user :
			stints = [ s for s in stints if s.user ==user ]
		
		self.__store.transactionEnd()
		
		if not expired :		
			stints = [ s for s in stints if not s.expired() ]
	
		
		if context :
			
			if not isinstance( context, Context ) :
				context = Context( context )
			
			validStints = []
			for s in stints:
				stintRelevant = False
				for k in context.attribtues :		
					if k in s.context.attribtues :
						stintRelevant = True
						if s.context.attribtues[k] != context.attribtues[k] :
							stintRelevant = False
							break
				if stintRelevant :
					validStints.append( s )
			stints = validStints
		
		if readable :
			return [ str(s) for s in stints ]
		else :
			return stints
	
		
	def janitor( self ) :
	
		"""Cleans out any expired stints, and empty contexts."""

		self.__store.transactionBegin( lock=True )

		now = datetime.now()

		activeContexts = set()
		for s in self.__store.stints() :
			
			if s.expired( now ) :
			
				self.__store.removeStint(
					user = s.user,
					context = s.context
				 )
	
			else :
			
				activeContexts.add( s.context.hash() )
		
		for c in self.__store.contexts() :
			if c.hash() not in activeContexts :
				self.__store.removeContext( c )
				
		self.__store.transactionEnd()
				
		