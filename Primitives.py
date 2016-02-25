import math
class vec3 :
	def __init__( self ) :
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
	def __init__( self , x , y , z ) :
		self.x = x
		self.y = y
		self.z = z
	def add( self , a ) :
		return vec3( self.x + a.x , self.y + a.y , self.z + a.z )
	def mul( self , a ) :
		return vec3( self.x * a , self.y * a , self.z * a )
	def div( self , a ) :
		return self.mul( 1.0 / a )
	def sub( self , a ) :
		return self.add( a.mul( -1.0 ) )
	def dot( self , a ) :
		return self.x * a.x + self.y * a.y + self.z * a.z
	def mod2( self ) :
		return self.dot( self )
	def mod( self ) :
		return math.sqrt( self.mod2( ) )
	def norm( self ) :
		return self.div( self.mod( ) )
	def vecx( self , a ) :
		return vec3( self.y * a.z - self.z * a.y , self.z * a.x - self.x * a.z , self.x * a.y - self.y * a.x )
	def asFloatArr(self):
		return [ self.x , self.y , self.z ]
	def lerp(self, a , x):
		ix = 1.0 - x
		return vec3( ix * self.x + a.x * x , ix * self.y + a.y * x , ix * self.z + a.z * x )
	def __str__( self ) :
		return "{" + self.x.__str__( ) + "," + self.y.__str__( ) + "," + self.z.__str__( ) + "}"
class vec2 :
	def __init__( self ) :
		self.x = 0.0
		self.y = 0.0
	def __init__( self , x , y ) :
		self.x = x
		self.y = y
	def copyIn( self , a ) :
		self.x = a.x
		self.y = a.y
	def copy( self ) :
		return vec2( self.x , self.y )
	def add( self , a ) :
		return vec2( self.x + a.x , self.y + a.y )
	def mul( self , a ) :
		return vec2( self.x * a , self.y * a )
	def div( self , a ) :
		return self.mul( 1.0 / a )
	def sub( self , a ) :
		return self.add( a.mul( -1.0 ) )
	def dot( self , a ) :
		return self.x * a.x + self.y * a.y
	def mod2( self ) :
		return self.dot( self )
	def mod( self ) :
		return math.sqrt( self.mod2( ) )
	def norm( self ) :
		return self.div( self.mod( ) )
	def asFloatArr(self):
		return [ self.x , self.y ]
	def lerp(self, a , x):
		ix = 1.0 - x
		return vec2( ix * self.x + a.x * x , ix * self.y + a.y * x )
	def __str__( self ) :
		return "{" + self.x.__str__( ) + "," + self.y.__str__( ) + "," + self.z.__str__( ) + "}"
class Ray :
	def __init__( self ) :
		self.p = vec3( )
		self.v = vec3( )
class Camera :
	def __init__( self ) :
		self.p = vec3( )
		self.look = vec3( )
		self.up = vec3( )
		self.left = vec3( )
		self.itanx = 1.0
		self.itany = 1.0
class Material :
	def __init__( self ) :
		self.metallness = 1.0
		self.roughness = 0.0
		self.fresnel = 1.0
		self.specular = 1.0
		self.color = vec3( )
class Collision :
	def __init__( self ) :
		self.p = vec3( )
		self.n = vec3( )
		self.mat = Material
class Object :
	def __init__( self ) :
		self.pos = vec3( )
		self.aabb = vec3( )
	def collide( self , ray ) :
		return [ ]
class Sphere( Object ) :
	def __init__( self , r ) :
		self.r = r
		self.aabb.x = 0.5 * r
		self.aabb.y = 0.5 * r
		self.aabb.y = 0.5 * r
