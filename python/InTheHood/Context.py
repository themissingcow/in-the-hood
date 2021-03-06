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