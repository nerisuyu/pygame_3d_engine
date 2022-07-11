import pyopencl as cl
import numpy as np
import time
import os


os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
# os.environ['PYOPENCL_CTX'] = '1'
# We must select the platform first, 0 for 'Apple'
# and then the device: 1 for 'Intel Iris Graphics 6100'.
os.environ['PYOPENCL_CTX'] = '0:1'


class matrix_dot_vector:
    def __init__(self):
        os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
        os.environ['PYOPENCL_CTX'] = '0:1'

        all_platforms = cl.get_platforms()
        platform = next((p for p in all_platforms if p.get_devices(device_type=cl.device_type.GPU) != []), None)
        if platform is None:
            raise RuntimeError('No OpenCL GPU device found.')
        my_gpu_devices = platform.get_devices(device_type=cl.device_type.GPU)

        self.ctx = cl.Context(devices=my_gpu_devices)
        self.queue = cl.CommandQueue(self.ctx)

        self.prg = cl.Program(self.ctx, """
            __kernel void multiply(
            __global float *a, __global float *b,__global float *c, __global float *d)
            {
            int gid = get_global_id(0);
            c[gid] = 0.0f; 
            __global float *pA = &a[gid%4*4];
            __global float *pB = &b[gid%4];
            for(int k=0; k<4; k++)
            {
                pB = &b[(gid/4)*4+k];
                c[gid] += (*(pA++))*(*pB);
            }
            barrier(CLK_LOCAL_MEM_FENCE);
            c[gid]= c[gid]/c[gid/4*4+3];
            }
            """).build()

    def calculate(self, matrix, vectors):

        '''v_list = []
        for i in range(0, len(vectors)):
            for j in range(0, 4):
                v_list.append(vectors[i][j])
        b = np.array(v_list).astype(np.float32)
        '''
        start = time.time()
        b = np.array(vectors).astype(np.float32)
        end = time.time()
        print("time= ", end - start)

        m_list = []
        for i in range(0, 4):
            for j in range(0, 4):
                m_list.append(matrix[i][j])


        a = np.array(m_list).astype(np.float32)
        c = np.zeros((len(b)), dtype=np.float32)
        d = np.zeros((len(b)), dtype=np.float32)

        mf = cl.mem_flags
        a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
        b_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
        c_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, c.nbytes)
        d_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, d.nbytes)



        self.prg.multiply(self.queue, c.shape, None,
                          a_buf, b_buf, c_buf,d_buf)


        a_mul_b = np.empty_like(c)
        cl.enqueue_copy(self.queue, a_mul_b, c_buf)


        return a_mul_b

        output=[]
        for i in range(0, len(vectors)):
            output.append(np.array([a_mul_b[i*4],a_mul_b[i*4+1],a_mul_b[i*4+2],a_mul_b[i*4+3]]).astype(np.float64))
        return output


vec1 = np.array([1, 2, 3, 4])
vec2 = np.array([1, 2, 3, 4])
vec3 = np.array([0, 0, 0, 0])
vec4 = np.array([100, 100, 100, 100])
vec5 = np.array([1, 1, 1, 1])
vectors = [vec1, vec2, vec3, vec4, vec5]
matrix = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
mdv = matrix_dot_vector()
print(mdv.calculate(matrix, vectors))
