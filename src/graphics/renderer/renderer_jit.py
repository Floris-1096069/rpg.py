import numpy as np
from numba import njit

#uses numba jit compiler to speed up calculation work for mode7
#by offloading from interpreter to jit
#I put this in a different module, to completely separate jit and interpreted code
#do not parallelize, only costs cpu usage for same performance
@njit(fastmath=True, parallel=False)
def render_mode7_jit(buffer_array, tileset_array, tile_ids, cos_table, sin_table,
                     offset_x, offset_y, horizon, scale, tile_size, void_color):

    bh, bw, _ = buffer_array.shape
    map_h, map_w = tile_ids.shape
    map_px_w = map_w * tile_size
    map_px_h = map_h * tile_size

    distances = ((np.arange(horizon, bh) - horizon) / (bh - horizon)) * scale
    distances[distances <= 0] = 1e-6
    row_scales = horizon / distances

    for y in range(horizon, bh):
        row_scale = row_scales[y - horizon]
        for x in range(bw):
            wx = int(offset_x + cos_table[x] * row_scale)
            wy = int(offset_y + sin_table[x] * row_scale)

            if 0 <= wx < map_px_w and 0 <= wy < map_px_h:
                tile_id = tile_ids[wy // tile_size, wx // tile_size]
                py = wy % tile_size
                px = wx % tile_size
                buffer_array[y, x, 0] = tileset_array[tile_id, py, px, 0]
                buffer_array[y, x, 1] = tileset_array[tile_id, py, px, 1]
                buffer_array[y, x, 2] = tileset_array[tile_id, py, px, 2]
            else:
                buffer_array[y, x, 0] = void_color[0]
                buffer_array[y, x, 1] = void_color[1]
                buffer_array[y, x, 2] = void_color[2]