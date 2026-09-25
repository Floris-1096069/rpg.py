import math

from config import Config

class Camera:
    def __init__(self, tilemap):
        config = Config()
        self.tilemap = tilemap
        self.x, self.y = tilemap.spawn
        self.angle = 0
        self.speed = 5  
        self.rotation_speed = 0.07
        self.keybindings = config.key_bindings
        
    def update(self, input_state):
        keys = input_state["keys"]

        if self._is_action_pressed("rotate_left", keys):
            self.angle -= self.rotation_speed
        if self._is_action_pressed("rotate_right", keys):
            self.angle += self.rotation_speed

        if self._is_action_pressed("move_forward", keys):
            self._try_move(self.speed)
        if self._is_action_pressed("move_backward", keys):
            self._try_move(-self.speed)

    def _try_move(self, distance):
        nx = self.x + distance * math.cos(self.angle)
        ny = self.y + distance * math.sin(self.angle)

        if self.tilemap.is_passable(nx, ny):
            self.x, self.y = nx, ny
        elif self.tilemap.is_passable(nx, self.y):
            self.x = nx
        elif self.tilemap.is_passable(self.x, ny):
            self.y = ny

    def _is_action_pressed(self, action, keys):
        for key in self.keybindings.get(action, []):
            if key in keys:
                return True
        return False