import math

from config import Config

class Camera:
    def __init__(self, player):
        self.player = player
        self.distance = 60
        self.angle = player.angle
        self.x = player.x - math.cos(self.angle) * self.distance
        self.y = player.y - math.sin(self.angle) * self.distance

    def update(self):
        self.angle = self.player.angle
        self.x = self.player.x - math.cos(self.angle) * self.distance
        self.y = self.player.y - math.sin(self.angle) * self.distance