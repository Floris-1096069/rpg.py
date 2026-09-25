import numpy as np
from numba import njit

#uses numba jit compiler to speed up calculation work for mode7
#by offloading from interpreter to jit
#I put this in a different module, to completely separate jit and interpreted code
#do not parallelize, only costs cpu usage for same performance
@njit(fastmath=True, parallel=False)
def render_mode7_jit(buffer_array, tileset_array, tile_ids, cos_table, sin_table,
                     offset_x, offset_y, horizon, scale, tile_size, void_color, fog_start, fog_end):

    bh, bw, _ = buffer_array.shape
    map_h, map_w = tile_ids.shape
    map_px_w = map_w * tile_size
    map_px_h = map_h * tile_size

    distances = ((np.arange(horizon, bh) - horizon) / (bh - horizon)) * scale
    distances[distances <= 0] = 1e-6
    row_scales = horizon / distances


    for y in range(horizon, bh):
        row_scale = row_scales[y - horizon]

        fog_t = (row_scale - fog_start) / (fog_end - fog_start)
        if fog_t > 1.0:
            fog_t = 1.0
        elif fog_t < 0.0:
            fog_t = 0.0

        for x in range(bw):
            wx = int(offset_x + cos_table[x] * row_scale)
            wy = int(offset_y + sin_table[x] * row_scale)

            if 0 <= wx < map_px_w and 0 <= wy < map_px_h:
                tile_id = tile_ids[wy // tile_size, wx // tile_size]
                py = wy % tile_size
                px = wx % tile_size
                for c in range(3):
                    tile_c = tileset_array[tile_id, py, px, c]
                    buffer_array[y, x, c] = int(tile_c * (1.0 - fog_t) + void_color[c] * fog_t)
            else:
                for c in range(3):
                    buffer_array[y, x, c] = void_color[c]