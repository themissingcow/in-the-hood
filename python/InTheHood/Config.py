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

import os

class Config :

	def __init__( self, configFile=None ) :
		
		self.__config = {}
		
		if not configFile :
			configFile = "%s/defaults.py" % os.path.abspath( os.path.dirname( __file__ ) )
		
		if os.path.isfile( configFile ) :
			execfile( configFile )
		else :
			raise RuntimeError, "Unable to locate default config file (%s)" \
				% configFile
	
	def setKey( self, key, value ) :
	
		"""
		Sets the specified key to the given value,
		overwriting any existing entry
		"""
		
		self.__config[ key ] = value
	
	def getKey( self, key, default=None ) :
	
		"""
		Retrieves the value of the requested key from the
		current config, or None if it has not been set.
		"""
		
		return self.__config[ key ] if key in self.__config else default
	
	def getKeys( self, root ) :
		
		"""
		Retrieves all the keys in a given root
		"""
		keys = []
		
		for k in self.__config.keys() :
			if k.startswith( root ) :
				keys.append( k )
		
		return sorted( keys )	
			
	