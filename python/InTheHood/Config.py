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
			
	