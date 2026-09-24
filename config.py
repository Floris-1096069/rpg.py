import pygame

class Config:
    def __init__(self):
        self.fps = 60
        self.resolution = (800, 600)
        self.key_bindings = {
            "rotate_left": [pygame.K_a, pygame.K_LEFT],
            "rotate_right": [pygame.K_d, pygame.K_RIGHT],
            "move_forward": [pygame.K_w, pygame.K_UP],
            "move_backward": [pygame.K_s, pygame.K_DOWN],
        }