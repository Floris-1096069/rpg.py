import os
import numpy as np
import pygame

class TileMap:
    TILE_SIZE = 32
    
    TILE_CHARS = {
        ".": 1,
        "#": 2,
        "p": 3,
        "$": 4,
    }
    
    SOLID_IDS = {2}
    
    def __init__(self, map_path, tileset_dir):
        self.tile_ids, self.spawn = self._load_map(map_path)
        self.tileset_array = self._load_tileset(tileset_dir)

    def _load_map(self, path):
        with open(path) as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        width = len(lines[0])
        for i, line in enumerate(lines):
            if len(line) != width:
                raise ValueError(f"{path}: row {i} is {len(line)} chars, expected {width}")

        tile_ids = np.zeros((len(lines), width), dtype=np.int64)
        spawn_tile = None

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "P":
                    if spawn_tile is not None:
                        raise ValueError(f"{path}: multiple spawn points")
                    spawn_tile = (x, y)
                    char = "."
                if char not in self.TILE_CHARS:
                    raise ValueError(f"{path}: unknown tile char '{char}' at ({x}, {y})")
                tile_ids[y, x] = self.TILE_CHARS[char]

        if spawn_tile is None:
            raise ValueError(f"{path}: no spawn point 'P'")

        spawn = (
            (spawn_tile[0] + 0.5) * self.TILE_SIZE,
            (spawn_tile[1] + 0.5) * self.TILE_SIZE,
        )
        return tile_ids, spawn

    def _load_tileset(self, tileset_dir):
        used_ids = sorted(set(self.tile_ids.flatten().tolist()))
        max_id = max(used_ids)
        ts = self.TILE_SIZE
        tileset_array = np.zeros((max_id + 1, ts, ts, 3), dtype=np.uint8)
        background = pygame.Surface((ts, ts))
        background.fill((0, 0, 0))

        for tile_id in used_ids:
            path = os.path.join(tileset_dir, f"{tile_id}.png")
            if not os.path.isfile(path):
                raise FileNotFoundError(f"missing tile image: {path}")
            surface = pygame.image.load(path).convert_alpha()
            if surface.get_size() != (ts, ts):
                factor = ts // surface.get_width()
                surface = pygame.transform.scale_by(surface, factor)
            background.blit(surface, (0, 0))
            tileset_array[tile_id] = pygame.surfarray.array3d(background).transpose(1, 0, 2)
            background.fill((0, 0, 0))

        return tileset_array

    @property
    def width(self):
        return self.tile_ids.shape[1] * self.TILE_SIZE

    @property
    def height(self):
        return self.tile_ids.shape[0] * self.TILE_SIZE

    def tile_at(self, world_x, world_y):
        tx = int(world_x) // self.TILE_SIZE
        ty = int(world_y) // self.TILE_SIZE
        if not (0 <= tx < self.tile_ids.shape[1] and 0 <= ty < self.tile_ids.shape[0]):
            return None
        return int(self.tile_ids[ty, tx])

    def is_passable(self, world_x, world_y):
        tile = self.tile_at(world_x, world_y)
        return tile is not None and tile not in self.SOLID_IDS