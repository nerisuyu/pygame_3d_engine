# L-29 MCS 572 Fri 28 Oct 2016 : matmatmulocl.py

"""
Illustration of a matrix-matrix multiplication with PyOpenCL.
We set the environment variable to see compiler warnings
and to run on the graphics card.
"""

import pyopencl as cl
import numpy as np

import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
# os.environ['PYOPENCL_CTX'] = '1'
# We must select the platform first, 0 for 'Apple'
# and then the device: 1 for 'Intel Iris Graphics 6100'.
os.environ['PYOPENCL_CTX'] = '0:1'

(n, m, p) = (3, 4, 5)

a = np.random.randint(2, size=(n*m))
b = np.random.randint(2, size=(m*p))
c = np.zeros((n*p), dtype=np.float32)

a = a.astype(np.float32)
b = b.astype(np.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

prg = cl.Program(ctx, """
    __kernel void multiply(
    const ushort n, const ushort m, const ushort p,
    __global float *a, __global float *b, __global float *c)
    {
      int gid = get_global_id(0);
      c[gid] = 0.0f;
      int rowC = gid/p;
      int colC = gid%p;
      __global float *pA = &a[rowC*m];
      __global float *pB = &b[colC];
      for(int k=0; k<m; k++)
      {
         pB = &b[colC+k*p];
         c[gid] += (*(pA++))*(*pB);
      }
      
    }
    """).build()

prg.multiply(queue, c.shape, None, 
             np.uint16(n), np.uint16(m), np.uint16(p),
             a_buf, b_buf, c_buf)

a_mul_b = np.empty_like(c)
cl.enqueue_copy(queue, a_mul_b, c_buf)

print("matrix A:")
print(a.reshape(n, m))
print("matrix B:")
print(b.reshape(m, p))
print("multiplied A*B:")
print(a_mul_b.reshape(n, p))