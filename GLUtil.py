from OpenGL.GL import *
import numpy
import OpenGL.GL.shaders
class MeshGL:
	def __init__( self ) :
		self.vao = 0
		self.vbo = 0
	def init( self , program , Mesh ) :
		from numpy import frombuffer
		vertex_count = len( Mesh.vertecies )
		vertex_size_in_floats = 0
		for ( name , float_count ) in Mesh.vertex_layout.iteritems() :
			vertex_size_in_floats += float_count
		buffer_size = vertex_size_in_floats * vertex_count * 4
		self.vao = glGenVertexArrays( 1 )
		glBindVertexArray( self.vao )
		self.vbo = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER , self.vbo )
		glBufferData( GL_ARRAY_BUFFER , buffer_size , None , GL_STATIC_DRAW )
		raw_mapping = glMapBufferRange( GL_ARRAY_BUFFER , 0 , buffer_size , GL_MAP_WRITE_BIT )
		float_mapping = ctypes.cast( raw_mapping , ctypes.POINTER( ctypes.c_float * ( vertex_count * vertex_size_in_floats ) ) )[ 0 ]
		buffer_pos = 0
		for vid in range( 0 , len( Mesh.vertecies ) ) :
			vertex = Mesh.vertecies[ vid ]
			for i in range( 0 , len( vertex.attributes ) ) :
				attribute = vertex.attributes[ i ]
				float_arr = attribute.asFloatArr()
				for f in float_arr :
					float_mapping[ buffer_pos ] = f
					buffer_pos += 1
		glUnmapBuffer( GL_ARRAY_BUFFER )
		offset = 0
		for ( name , float_count ) in Mesh.vertex_layout.iteritems() :
			attribute_location = glGetAttribLocation( program , name )
			if attribute_location < 0 :
				continue
			glEnableVertexAttribArray( attribute_location )
			glVertexAttribPointer( attribute_location , float_count , GL_FLOAT , False , vertex_size_in_floats * 4 , ctypes.c_void_p( offset ) )
			offset += float_count * 4

		self.ibo = glGenBuffers( 1 )
		self.index_size = len( Mesh.indecies )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER , self.ibo )
		arr = numpy.array( Mesh.indecies , dtype = numpy.uint32 )
		glBufferData( GL_ELEMENT_ARRAY_BUFFER , len( arr ) * 4 , arr , GL_STATIC_DRAW )
		glBindVertexArray( 0 )
		glDisableVertexAttribArray( 0 )
		glBindBuffer( GL_ARRAY_BUFFER , 0 )
		glBindBuffer( GL_ELEMENT_ARRAY_BUFFER , 0 )
	def release(self):
		glDeleteBuffers( 2 , [ self.vbo , self.ibo ] )
		glDeleteVertexArrays( 1 , [ self.vao ] )
	def draw( self , mode = "SOLID" ) :
		if mode == "SOLID" :
			glPolygonMode( GL_FRONT_AND_BACK , GL_FILL )
		else :
			glPolygonMode( GL_FRONT_AND_BACK , GL_LINE )
		glBindVertexArray( self.vao )
		glDrawElements( GL_TRIANGLES , self.index_size , GL_UNSIGNED_INT , None )
		glBindVertexArray( 0 )