from OpenGL.GL import *
from PyQt4 import QtGui
import OpenGL.GL.shaders
from PyQt4.QtOpenGL import *
import numpy
import ctypes
import time
from Primitives import vec2 , vec3
vertex_shader = """
#version 330
in vec3 position;
in vec2 texcoord;
uniform float angle;
out vec2 frag_texcoord;
void main()
{
	float cosx = cos( angle );
	float sinx = sin( angle );
	mat3 rot_mat = mat3(
		cosx , 0.0 , sinx ,
		0.0 , 1.0 , 0.0 ,
		-sinx , 0.0 , cosx
	);
	frag_texcoord = texcoord;
	gl_Position = vec4( rot_mat * position * 0.8 , 1.0 );
}
"""

fragment_shader = """
#version 330
in vec2 frag_texcoord;
void main()
{
   gl_FragColor = vec4( frag_texcoord , 1.0f , 1.0f );
}
"""
class Vertex( object ) :
	def __init__( self , attributes = [] ) :
		self.attributes = attributes
		#self.neighbors = [ ]
	"""def addNeighbor(self , vertex):
		self.neighbors.append(vertex)
		return self"""
	def getPos(self):
		return self.attributes[ 0 ]
	def lerp(self,vertex,x):
		out = Vertex()
		for i in range( 0 , len( self.attributes ) ) :
			out.attributes.append( self.attributes[ i ].lerp( vertex.attributes[ i ] ) )
		return out
class Face:
	def __init__(self,vertecies):
		self.vertecies = vertecies
		self.normal = vertecies[ 1 ]\
			.sub( vertecies[ 0 ] ).vecx(
			vertecies[ 2 ]
			.sub( vertecies[ 0 ] )
		).norm()
class FaceMesh:
	def __init__(self,faces):
		self.faces = faces
class VertexMesh:
	def __init__(self, vertex_layout , vertecies , indecies):
		self.vertex_layout = vertex_layout
		self.vertecies = vertecies
		self.indecies = indecies
	def getFaceCount(self):
		return len( self.indecies ) / 3
	def getFace(self,i):
		return [ self.vertecies[ self.indecies[ i * 3 ] ] ,
				self.vertecies[ self.indecies[ i * 3 + 1 ] ] ,
				self.vertecies[ self.indecies[ i * 3 + 2 ] ] ]
def sliceMesh( mesh , pos , norm ) :
	faces = []
	vertecies = set()
	for i in range( 0 , mesh.getFaceCount() ) :
		face = mesh.getFace( i )
		above = []
		beneath = []
		for vertex in face :
			dist = vertex.attributes[ 0 ].sub( pos ).dot( norm )
			if lside < 0.0 :
				beneath.append( [ vertex , dist ] )
			else :
				above.append( [ vertex , dist ] )
		if len( beneath ) != 3 and bc != 0 :
			if len( beneath ) == 1 :
				k0 = above[ 0 ][ 1 ] / ( above[ 0 ][ 1 ] + beneath[ 0 ][ 1 ] )
				vertex0 = above[ 0 ][ 0 ].lerp( beneath[ 0 ][ 0 ] , k0 )
				k1 = above[ 1 ][ 1 ] / ( above[ 1 ][ 1 ] + beneath[ 0 ][ 1 ] )
				vertex1 = above[ 1 ][ 0 ].lerp( beneath[ 0 ][ 0 ] , k0 )
				faces.append( [ above[ 0 ][ 0 ] , vertex0 , vertex1 ] )
				faces.append( [ above[ 1 ][ 0 ] , above[ 0 ][ 0 ] , vertex1 ] )
				vertecies.add( above[ 0 ][ 0 ] )
				vertecies.add( above[ 1 ][ 0 ] )
				vertecies.add( vertex0 )
				vertecies.add( vertex1 )
			else :
				k0 = above[ 0 ][ 1 ] / ( above[ 0 ][ 1 ] + beneath[ 0 ][ 1 ] )
				vertex0 = above[ 0 ][ 0 ].lerp( beneath[ 0 ][ 0 ] , k0 )
				k1 = above[ 0 ][ 1 ] / ( above[ 0 ][ 1 ] + beneath[ 1 ][ 1 ] )
				vertex1 = above[ 0 ][ 0 ].lerp( beneath[ 1 ][ 0 ] , k0 )
				faces.append( [ above[ 0 ][ 0 ] , vertex0 , vertex1 ] )
				vertecies.add( above[ 0 ][ 0 ] )
				vertecies.add( vertex0 )
				vertecies.add( vertex1 )
		else :
			faces.append( face )
			vertecies.add( face[ 0 ] )
			vertecies.add( face[ 1 ] )
			vertecies.add( face[ 2 ] )
	for face in faces :

class MeshGL( object ) :
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
		for ( id , vertex ) in Mesh.vertecies.iteritems() :
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
		glDeleteBuffers( 1 , [ self.vbo ] )
		glDeleteVertexArrays( 1 , [ self.vao ] )
	def draw( self ) :
		glBindVertexArray( self.vao )
		glDrawElements( GL_LINES , self.index_size , GL_UNSIGNED_INT , None )
		glBindVertexArray( 0 )
def loadObj( filename ) :
	positions = [ ]
	texcoords = [ ]
	vertecies = { }
	indecies = [ ]
	indecies_map = { }
	vertex_counter = 0
	fh = open( filename )
	for line in fh :
		if line[ 0 ] == '#' : continue
		line = line.strip( ).split( ' ' )
		if line[ 0 ] == 'v' :
			positions.append( vec3( float( line[ 1 ] ) , float( line[ 2 ] ) , float( line[ 3 ] ) ) )
		elif line[ 0 ] == 'vt' :
			texcoords.append( vec2( float( line[ 1 ] ) , float( line[ 2 ] ) ) )
		elif line[ 0 ] == 'f' :
			face = line[ 1 : ]
			for i in range( 0 , len( face ) ):
				face[ i ] = face[ i ].split( '/' )
				for j in range( 0 , len( face[ i ] ) ) :
					face[ i ][ j ] = int( face[ i ][ j ] ) - 1
			for i in range( 0 , len( face ) ):
				vertecies[ face[ i ][ 1 ] ] = Vertex( [ positions[ face[ i ][ 0 ] ] , texcoords[ face[ i ][ 1 ] ] ] )
			if len( face ) == 4 :
				indecies.append( face[ 0 ][ 1 ] )
				indecies.append( face[ 1 ][ 1 ] )
				indecies.append( face[ 2 ][ 1 ] )
				indecies.append( face[ 0 ][ 1 ] )
				indecies.append( face[ 2 ][ 1 ] )
				indecies.append( face[ 3 ][ 1 ] )
			elif len( face ) == 3 :
				indecies.append( face[ 0 ][ 1 ] )
				indecies.append( face[ 1 ][ 1 ] )
				indecies.append( face[ 2 ][ 1 ] )

	for i in range( 0 , len( indecies ) / 3 ) :
		i0 = indecies[ i * 3 ]
		i1 = indecies[  i * 3 + 1 ]
		i2 = indecies[ i * 3 + 2 ]
		"""vertecies[ i0 ].addNeighbor( vertecies[ i1 ] ).addNeighbor( vertecies[ i2 ] )
		vertecies[ i1 ].addNeighbor( vertecies[ i0 ] ).addNeighbor( vertecies[ i2 ] )
		vertecies[ i2 ].addNeighbor( vertecies[ i1 ] ).addNeighbor( vertecies[ i0 ] )"""
	return VertexMesh( { "position" : 3 , "texcoord" : 2 } , vertecies , indecies )
mesh = loadObj( "lhead.obj " )
slice( mesh , vec3( 0.0 , 0.0 , 0.0 ) , vec3( 0.0 , 0.0 , 1.0 ) )
class WfWidget( QGLWidget ) :
	def __init__( self , glformat , parent = None ) :
		super( WfWidget , self ).__init__( glformat , parent )
		self.mesh = MeshGL( )
		self.shader = 0
		self.time = time.clock()
		self.dt = 0.0
		self.last_time = self.time
	def updateTime(self):
		self.time = time.clock()
		self.dt = self.time - self.last_time
		self.last_time = self.time
	def paintGL( self ) :
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.updateTime()
		glUseProgram( self.shader )
		glUniform1f( glGetUniformLocation( self.shader , "angle" ) , self.time )
		self.mesh.draw( )
		self.update()

	def resizeGL( self , w , h ) :
		glViewport( 0 , 0 , w , h )
	def initializeGL( self ) :
		glClearColor( 0.0 , 0.0 , 0.0 , 1.0 )
		glClearDepth( 1.0 )
		glEnable( GL_DEPTH_TEST )
		glClear( GL_COLOR_BUFFER_BIT )
		self.shader = OpenGL.GL.shaders.compileProgram(
			OpenGL.GL.shaders.compileShader( vertex_shader , GL_VERTEX_SHADER ) ,
			OpenGL.GL.shaders.compileShader( fragment_shader , GL_FRAGMENT_SHADER )
		)
		self.mesh.init( self.shader , mesh )
if __name__ == '__main__' :
	app = QtGui.QApplication( [ "Winfred's PyQt OpenGL" ] )
	glformat = QGLFormat( )
	glformat.setVersion( 3 , 0 )
	glformat.setProfile( QGLFormat.CoreProfile )
	glformat.setSampleBuffers( True )
	widget = WfWidget( glformat )
	widget.show( )
	app.exec_( )
