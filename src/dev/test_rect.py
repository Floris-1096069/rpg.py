import pygame
from config import Config

class TestRect:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.rect_x = self.config.resolution[0] // 2 - 25
        self.rect_y = self.config.resolution[1] // 2 - 25
        self.rect_speed = 10

    def update(self, input_state):
        keys = input_state["keys"]
        if pygame.K_a in keys or pygame.K_LEFT in keys:
            self.rect_x -= self.rect_speed
        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            self.rect_x += self.rect_speed
        if pygame.K_w in keys or pygame.K_UP in keys:
            self.rect_y -= self.rect_speed
        if pygame.K_s in keys or pygame.K_DOWN in keys:
            self.rect_y += self.rect_speed

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect_x, self.rect_y, 50, 50))