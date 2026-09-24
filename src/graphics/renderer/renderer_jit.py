import numpy as np
from numba import njit

#uses numba jit compiler to speed up calculation work for mode7
#by offloading from interpreter to jit
#I put this in a different module, to completely separate jit and interpreted code
#do not parallelize, only costs cpu usage for same performance
@njit(fastmath=True, parallel=False)
def render_mode7_jit(buffer_array, texture_array, cos_table, sin_table,
                     offset_x, offset_y, horizon, scale):

    bh, bw, _ = buffer_array.shape
    th, tw, _ = texture_array.shape

    #calculate row_scales once/frame
    distances = ((np.arange(horizon, bh) - horizon) / (bh - horizon)) * scale
    distances[distances <= 0] = 1e-6
    row_scales = horizon / distances

    #singlethreadedly compute scanlines xoxo
    for y in range(horizon, bh):
        row_scale = row_scales[y - horizon]

        for x in range(bw):
            tx = int(offset_x + cos_table[x] * row_scale) % tw
            ty = int(offset_y + sin_table[x] * row_scale) % th
            buffer_array[y, x, 0] = texture_array[ty, tx, 0]
            buffer_array[y, x, 1] = texture_array[ty, tx, 1]
            buffer_array[y, x, 2] = texture_array[ty, tx, 2]