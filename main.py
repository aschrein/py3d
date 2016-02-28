from OpenGL.GL import *
from PyQt4 import QtGui
import OpenGL.GL.shaders
from PyQt4.QtOpenGL import *
import numpy
import ctypes
import time
from Primitives import vec2 , vec3
from MeshUtil import *
from GLUtil import *
from FileUtil import *
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
uniform vec4 color;
in vec2 frag_texcoord;
void main()
{
   gl_FragColor = color;//vec4( color , 0.2f );
}
"""

mesh_origin = loadObj( "lhead.OBJ" )#genCilinder(160)
#slice( mesh , vec3( 0.0 , 0.0 , 0.0 ) , vec3( 0.0 , 0.0 , 1.0 ) )
class WfWidget( QGLWidget ) :
	def __init__( self , glformat , parent = None ) :
		super( WfWidget , self ).__init__( glformat , parent )
		self.meshgl_origin = MeshGL( )
		self.meshgl = MeshGL( )
		self.shader = 0
		self.time = time.clock()
		self.dt = 0.0
		self.last_time = self.time
	def updateTime(self):
		self.time = time.clock()
		self.dt = self.time - self.last_time
		self.last_time = self.time
	def paintGL( self ) :
		glClearColor( 0.5 , 0.5 , 0.5 , 1.0 )
		glClearDepth( 1.0 )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.updateTime()
		#self.time = 2.1
		glUseProgram( self.shader )
		glUniform1f( glGetUniformLocation( self.shader , "angle" ) , self.time * -0.02 )

		import math

		glUniform4f( glGetUniformLocation( self.shader , "color" ) , 1.0 , 1.0 , 1.0 , 0.05 )
		self.meshgl_origin.draw( "WIRE" )

		cosx = math.cos( self.time * 0.1 )
		sinx = math.sin( self.time * 0.1 )
		mesh = sliceMesh( mesh_origin ,
			vec3( 0.0 , sinx , cosx ).mul( 0.01 ) ,
			vec3( 0.0 , -sinx , -cosx ) )
		mesh = sliceMesh( mesh ,
			vec3( 0.0 , -sinx , -cosx ).mul( 0.01 ) ,
			vec3( 0.0 , sinx , cosx ) )
		self.meshgl.release()
		self.meshgl.init( self.shader , mesh )
		glLineWidth( 4.0 )
		glUniform4f( glGetUniformLocation( self.shader , "color" ) , 0.0 , 0.0 , 0.0 ,1.0 )
		self.meshgl.draw( "WIRE" )
		glUniform4f( glGetUniformLocation( self.shader , "color" ) , 1.0 , 0.0 , 0.0 ,1.0 )
		self.meshgl.draw( "FILL" )

		self.update()

	def resizeGL( self , w , h ) :
		glViewport( 0 , 0 , w , h )
	def initializeGL( self ) :
		glDisable( GL_DEPTH_TEST )
		glDepthMask( GL_FALSE )
		glEnable( GL_BLEND )
		glBlendFunc( GL_SRC_ALPHA , GL_ONE_MINUS_SRC_ALPHA )
		glEnable( GL_ALPHA_TEST )
		glAlphaFunc( GL_GREATER , 0.0 )
		glClear( GL_COLOR_BUFFER_BIT )
		self.shader = OpenGL.GL.shaders.compileProgram(
			OpenGL.GL.shaders.compileShader( vertex_shader , GL_VERTEX_SHADER ) ,
			OpenGL.GL.shaders.compileShader( fragment_shader , GL_FRAGMENT_SHADER )
		)
		self.meshgl_origin.init( self.shader , mesh_origin )
		self.meshgl.init( self.shader , mesh_origin )
if __name__ == '__main__' :
	app = QtGui.QApplication( [ "Winfred's PyQt OpenGL" ] )
	glformat = QGLFormat( )
	glformat.setVersion( 3 , 0 )
	glformat.setSampleBuffers( True )
	glformat.setSamples( 8 )
	glformat.setProfile( QGLFormat.CoreProfile )
	glformat.setSampleBuffers( True )
	widget = WfWidget( glformat )
	widget.show( )
	app.exec_( )
