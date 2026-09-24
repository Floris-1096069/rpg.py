import math

from config import Config

class Camera:
    def __init__(self, x=0, y=0, angle=0):
        config = Config()
        self.x = x
        self.y = y
        self.angle = angle
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
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
        if self._is_action_pressed("move_backward", keys):
            self.x -= self.speed * math.cos(self.angle)
            self.y -= self.speed * math.sin(self.angle)

    def _is_action_pressed(self, action, keys):
        for key in self.keybindings.get(action, []):
            if key in keys:
                return True
        return False