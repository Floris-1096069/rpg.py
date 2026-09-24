import pygame
import numpy as np
import math

from graphics.renderer.renderer_jit import render_mode7_jit

class Renderer:
    def __init__(self, texture, buffer, screen, camera):
        self.buffer = buffer
        self.screen = screen
        self.texture = texture
        self.camera =camera
        self.buffer_width = buffer.get_width()
        self.buffer_height = buffer.get_height()
        self.horizon = 50
        self.scale = 1
        self.fov = math.pi / 3

    def mode7(self):
        self.offset_x = self.camera.x
        self.offset_y = self.camera.y
        self.angle = self.camera.angle
        surfarray = pygame.surfarray

        #Fill sky
        self.buffer.fill((135, 206, 235), (0, 0, self.buffer_width, self.horizon))

        #Convert surfaces to arrays
        texture_array = np.transpose(surfarray.pixels3d(self.texture), (1, 0, 2))
        buffer_array = np.transpose(surfarray.pixels3d(self.buffer), (1, 0, 2))

        #Precompute trig tables
        cos_table = []
        sin_table = []
        for x in range(self.buffer_width):
            angle_offset = (x - self.buffer_width / 2) / self.buffer_width * self.fov
            cos_table.append(math.cos(self.angle + angle_offset))
            sin_table.append(math.sin(self.angle + angle_offset))

        #Render Mode7
        render_mode7_jit(
            buffer_array, texture_array, cos_table, sin_table,
            self.offset_x, self.offset_y, self.horizon, self.scale
        )

        #Clean up
        del texture_array, buffer_array

    def upscale(self):
        scaled = pygame.transform.scale(self.buffer, self.screen.get_size())
        self.screen.blit(scaled, (0, 0))