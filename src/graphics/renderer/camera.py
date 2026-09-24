import math
import pygame

class Camera:
    def __init__(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 5
        self.rotation_speed = 0.05
        
    def update(self, input_state):
        keys = input_state["keys"]
        if pygame.K_a in keys or pygame.K_LEFT in keys:
            self.angle -= self.rotation_speed
        if pygame.K_d in keys or pygame.K_RIGHT in keys:
            self.angle += self.rotation_speed

        if pygame.K_w in keys or pygame.K_UP in keys:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
        if pygame.K_s in keys or pygame.K_DOWN in keys:
            self.x -= self.speed * math.cos(self.angle)
            self.y -= self.speed * math.sin(self.angle)