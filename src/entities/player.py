import math
import pygame
from config import Config

class Player:
    RADIUS = 10
    SPEED = 5
    ROTATION_SPEED = 0.07
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.x, self.y = tilemap.spawn
        self.angle = 0
        self.keybindings = Config().key_bindings
        self.sprite = pygame.image.load("src/graphics/assets/sprites/player.png").convert_alpha()

    def update(self, input_state):
        keys = input_state["keys"]

        if self._is_action_pressed("rotate_left", keys):
            self.angle -= self.ROTATION_SPEED
        if self._is_action_pressed("rotate_right", keys):
            self.angle += self.ROTATION_SPEED

        if self._is_action_pressed("move_forward", keys):
            self._try_move(self.SPEED)
        if self._is_action_pressed("move_backward", keys):
            self._try_move(-self.SPEED)

    def _circle_free(self, nx, ny):
        if not self.tilemap.is_passable(nx, ny):
            return False
        r = self.RADIUS
        for i in range(8):
            a = i * math.pi / 4
            if not self.tilemap.is_passable(nx + r * math.cos(a), ny + r * math.sin(a)):
                return False
        return True

    def _try_move(self, distance):
        nx = self.x + distance * math.cos(self.angle)
        ny = self.y + distance * math.sin(self.angle)

        if self._circle_free(nx, ny):
            self.x, self.y = nx, ny
        elif self._circle_free(nx, self.y):
            self.x = nx
        elif self._circle_free(self.x, ny):
            self.y = ny

    def _is_action_pressed(self, action, keys):
        for key in self.keybindings.get(action, []):
            if key in keys:
                return True
        return False

    def draw(self, screen, renderer, camera):
        buffer_y = renderer.world_to_buffer_row(camera.distance)
        scale_y = screen.get_height() / renderer.buffer_height
        screen_x = screen.get_width() // 2
        screen_y = int(buffer_y * scale_y)

        px_per_world = screen.get_width() / (camera.distance * renderer.fov)
        target_world_width = 24
        sprite = pygame.transform.scale(
            self.sprite,
            (int(target_world_width * px_per_world),
             int(self.sprite.get_height() * (target_world_width * px_per_world) / self.sprite.get_width())),
        )
        rect = sprite.get_rect(midbottom=(screen_x, screen_y))
        screen.blit(sprite, rect)