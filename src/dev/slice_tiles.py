import os
import pygame
from pathlib import Path

pygame.init()
pygame.display.set_mode((1, 1))

ROOT = Path(__file__).resolve().parents[2]
TILE = 64
OUT = ROOT / "src/graphics/assets/tiles/raw2"
OUT.mkdir(parents=True, exist_ok=True)

sheets = {
    "TILES-GROUND.png": "g",
    "TILES-HOUSE.png": "h",
    "TILES-ASSETS.png": "a",
}

for sheet_name, prefix in sheets.items():
    sheet = pygame.image.load(str(ROOT / "src/graphics/assets/tiles" / sheet_name)).convert_alpha()
    n = 0
    for y in range(0, sheet.get_height() - TILE + 1, TILE):
        for x in range(0, sheet.get_width() - TILE + 1, TILE):
            tile = sheet.subsurface((x, y, TILE, TILE)).copy()
            pygame.image.save(tile, str(OUT / f"{prefix}_{y // TILE:02d}_{x // TILE:02d}.png"))
            n += 1
    print(f"{sheet_name}: sliced {n} tiles")