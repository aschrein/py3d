import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import math
mod = SourceModule( """
     __global__ void doublify(float *a)
     {
       int idx = threadIdx.x + threadIdx.y*4;
       a[idx] *= 2;
     }
     """ )
"""a = numpy.random.randn( 4 , 4 )

a = a.astype( numpy.float32 )

a_gpu = cuda.mem_alloc( a.size * a.dtype.itemsize )

cuda.memcpy_htod( a_gpu , a )

#

func = mod.get_function( "doublify" )
func( a_gpu , block = (4 , 4 , 1) )

a_doubled = numpy.empty_like( a )
cuda.memcpy_dtoh( a_doubled , a_gpu )
print "original array:"
print a
print "doubled with kernel:"
print a_doubled

# alternate kernel invocation -------------------------------------------------

func( cuda.InOut( a ) , block = (4 , 4 , 1) )
print "doubled with InOut:"
print a"""

# part----------------------------------------------------------------------
import pycuda.gpuarray as gpuarray
a_gpu = gpuarray.to_gpu( numpy.random.randn( 4 , 4 ).astype( numpy.float32 ) )
a_doubled = ( a_gpu ).get( )

print "original array:"
print a_gpu
print "doubled with gpuarray:"
print a_doubled
