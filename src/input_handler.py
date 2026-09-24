import pygame

class InputHandler:
    def __init__(self):
        self.keys_pressed = {}
        self.mouse_buttons_pressed = {}
        self.mouse_position = (0,0)
                
    def update(self):
        self.keys_pressed = {}
        self.mouse_buttons_pressed = {}

        key_states = pygame.key.get_pressed()
        for i in range(len(key_states)):
            if key_states[i]:
                self.keys_pressed[i] = True

        mouse_states = pygame.mouse.get_pressed()
        for i in range(len(mouse_states)):
            if mouse_states[i]:
                self.mouse_buttons_pressed[i] = True
                
        self.mouse_position = pygame.mouse.get_pos()
        
    def get_input_state(self):
        #print(self.mouse_buttons_pressed)
        return {
            "keys" : self.keys_pressed,
            "mouse_buttons" : self.mouse_buttons_pressed,
            "mouse_position" : self.mouse_position
        }
        