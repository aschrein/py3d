from Primitives import *
from MeshUtil import *
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