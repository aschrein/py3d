from Primitives import *
class Vertex( object ) :
	def __init__( self , attributes = [] ) :
		self.attributes = attributes
		self.neighbors = [ ]
	def addNeighbor(self , vertex):
		self.neighbors.append(vertex)
		return self
	def getPos(self):
		return self.attributes[ 0 ]
	def lerp(self,vertex,x):
		out = Vertex( [] )
		for i in range( 0 , len( self.attributes ) ) :
			out.attributes.append( self.attributes[ i ].lerp( vertex.attributes[ i ] , x ) )
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
def genCilinder(r) :
	indecies = []
	vertecies = []
	dphi = math.pi * 2.0 / r
	vertex_counter = 0
	vertecies.append( Vertex( [ vec3( 1.0 , 0.0 , 0.0 ) ] ) )
	vertecies.append( Vertex( [ vec3( 1.0 , 1.0 , 0.0 ) ] ) )
	vertex_counter = 2
	for i in range( 1 , r ) :
		phi = i * dphi
		vertecies.append( Vertex( [ vec3( math.cos( phi ) , 0.0 , math.sin( phi ) ) ] ) )
		vertecies.append( Vertex( [ vec3( math.cos( phi ) , 1.0 , math.sin( phi ) ) ] ) )
		indecies.extend( [
			vertex_counter - 2 , vertex_counter - 1 , vertex_counter ,
			vertex_counter , vertex_counter + 1 , vertex_counter - 1
		] )
		vertex_counter += 2
	indecies.extend( [
			vertex_counter - 2 , vertex_counter - 1 , 0 ,
			0 , 1 , vertex_counter - 1
		] )
	return VertexMesh( { "position" : 3 } , vertecies , indecies )
def sliceMesh( mesh , pos , norm ) :
	faces = []
	vertecies = set()
	border_vertecies = []
	for i in range( 0 , mesh.getFaceCount() ) :
		face = mesh.getFace( i )
		above = []
		beneath = []
		for vertex in face :
			dist = vertex.getPos().sub( pos ).dot( norm )
			if dist < 0.0 :
				beneath.append( [ vertex , -dist ] )
			else :
				above.append( [ vertex , dist ] )
		if len( beneath ) != 0 :
			if len( beneath ) == 1 :
				k0 = above[ 0 ][ 1 ] / ( above[ 0 ][ 1 ] + beneath[ 0 ][ 1 ] )
				vertex0 = above[ 0 ][ 0 ].lerp( beneath[ 0 ][ 0 ] , k0 )
				k1 = above[ 1 ][ 1 ] / ( above[ 1 ][ 1 ] + beneath[ 0 ][ 1 ] )
				vertex1 = above[ 1 ][ 0 ].lerp( beneath[ 0 ][ 0 ] , k1 )
				border_vertecies.append( vertex0 )
				border_vertecies.append( vertex1 )
				faces.append( [ above[ 0 ][ 0 ] , vertex0 , vertex1 ] )
				faces.append( [ above[ 1 ][ 0 ] , above[ 0 ][ 0 ] , vertex1 ] )
				vertecies.add( above[ 0 ][ 0 ] )
				vertecies.add( above[ 1 ][ 0 ] )
				vertecies.add( vertex0 )
				vertecies.add( vertex1 )
			if len( beneath ) == 2 :
				k0 = above[ 0 ][ 1 ] / ( above[ 0 ][ 1 ] + beneath[ 0 ][ 1 ] )
				vertex0 = above[ 0 ][ 0 ].lerp( beneath[ 0 ][ 0 ] , k0 )
				k1 = above[ 0 ][ 1 ] / ( above[ 0 ][ 1 ] + beneath[ 1 ][ 1 ] )
				vertex1 = above[ 0 ][ 0 ].lerp( beneath[ 1 ][ 0 ] , k1 )
				border_vertecies.append( vertex0 )
				border_vertecies.append( vertex1 )
				faces.append( [ above[ 0 ][ 0 ] , vertex0 , vertex1 ] )
				vertecies.add( above[ 0 ][ 0 ] )
				vertecies.add( vertex0 )
				vertecies.add( vertex1 )
		else :
			faces.append( face )
			vertecies.add( face[ 0 ] )
			vertecies.add( face[ 1 ] )
			vertecies.add( face[ 2 ] )
	index_map = {}
	counter = 0
	vertecies_out = []
	indecies_out = []
	for vertex in vertecies :
		index_map[ vertex ] = counter
		vertecies_out.append( vertex )
		counter += 1
	for face in faces :
		for vertex in face :
			indecies_out.append( index_map[ vertex ] )
	return VertexMesh( mesh.vertex_layout , vertecies_out , indecies_out )