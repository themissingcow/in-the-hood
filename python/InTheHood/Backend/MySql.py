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

import MySQLdb
import _mysql
import pickle

class MySql :

	def __init__( self, host, databaseName, user, password=None, prefix=None, checkDb=True ) :
		
		"""
		checkDb=False disables table checking upon initialization
		"""
		
		self.host = host
		self.database = databaseName
		self.user = user
		self.password = password
		
		self.checkDb = checkDb
	
		self.stintsTable = "%s_stints" % prefix if prefix else "stints"
		self.contextsTable = "%s_contexts" % prefix if prefix else "contexts"	
		
		self.__connection = None
		self.__cursor = None
		self.__locked = False

	def initialize( self ) :	
	
		if self.checkDb :
		
			self._connect()
			
			self.__cursor.execute( """show tables;""" );
			tables = [ r[0] for r in self.__cursor.fetchall() ]
			
			if self.stintsTable not in tables :
					
				self.__cursor.execute(
					"""CREATE TABLE  `%s` ( `id` TEXT, `data` TEXT );""" % ( self.stintsTable, )
				)
			
			if self.contextsTable not in tables :	
			
				self.__cursor.execute(
					"""CREATE TABLE  `%s` ( `id` TEXT, `data` TEXT );""" % ( self.contextsTable, )
				)
			
			self._disconnect()

		
	def registerStint( self, stint ) :
	
		self._registerContext( stint.context )
		self._registerStint( stint )


	def removeStint( self, user, context ) :
		
		key = "%s%s" % ( user, context.hash() ) 
		self.__cursor.execute( 
			"""DELETE FROM %s WHERE `id`='%s'""" % (
				self.stintsTable, 
				_mysql.escape_string(key) 
			)
		)

		
	def stints( self ) :
		
		return self._fetch( self.stintsTable, dataOnly=True )
	

	def removeContext( self, context ) :
	
		h = context.hash()
		self.__cursor.execute( 
			"""DELETE FROM %s WHERE `id`='%s'""" % (
				self.contextsTable, 
				_mysql.escape_string(h) 
			)
		)


	def contexts( self ) :
		
		return self._fetch( self.contextsTable, dataOnly=True )

	
	def transactionBegin( self, transactionId, lock=False ) :
		
		if not self.__connection :
			self._connect()
	
		if lock :
			self.__cursor.execute( 
				"""LOCK TABLE %s WRITE, %s WRITE;""" %
				( self.stintsTable, self.contextsTable )
			);
			self.__locked = True
		else :
			self.__locked = False
					
	
	def transactionEnd( self, transactionId ) :

		if self.__locked :
			self.__cursor.execute( """UNLOCK TABLES;""" );
			
		if self.__connection :
		 	self._disconnect()
		
	def _connect( self ) :
	
		if not self.__connection :
			self.__connection = MySQLdb.connect(
				host = self.host,
				user = self.user,
				passwd = self.password,
				db = self.database
			)
		
		if not self.__cursor :
			self.__cursor = self.__connection.cursor()
	
	
	def _disconnect( self ) :
		
		if self.__connection :
			self.__connection.close()
			
		self.__connection = None
		self.__cursor = None

			
	def _registerContext( self, context ) :
	
		self._insertIfNotExists(
			self.contextsTable, 
			context.hash(), 
			context
		)
	
	
	def _registerStint( self, stint ) :
	
		self._insertIfNotExists( 
			self.stintsTable, 
			"%s%s" % ( stint.user, stint.context.hash() ), 
			stint
		)
			
			
	def _insertIfNotExists( self, table, key, data ) :
		
		self.__cursor.execute( 
			"""SELECT count(`id`) FROM %s WHERE `id`='%s'""" % (
				table, 
				_mysql.escape_string(key) 
			)
		)
		
		r = self.__cursor.fetchone()
		if not r or r[0] == 0 :		
			self.__cursor.execute(
				"""INSERT INTO %s ( `id`, `data` ) VALUES ( '%s', '%s' );""" % (
					 table,
					_mysql.escape_string( key ), 
					_mysql.escape_string( pickle.dumps(data) )
				)
			) 
			
	
	def _fetch( self, table, where=None, dataOnly=False ) :
		
		if where :
			self.__cursor.execute( """SELECT * FROM %s WHERE %s""" % ( table, where ) )
		else :
			self.__cursor.execute( """SELECT * FROM %s""" % table )	

		r = self.__cursor.fetchall()
		
		if r :
			if dataOnly  :
				return [ pickle.loads(i[1]) for i in r ]
			else :
				return [ ( i[0], pickle.loads(i[1]) ) for i in r ]
		else :
			return []
	
