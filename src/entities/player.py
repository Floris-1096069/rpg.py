import pygame

class Player:
    def __init__(self, camera):
        self.camera = camera
        self.sprite = pygame.image.load("src/graphics/assets/sprites/player.png").convert_alpha()

    def draw(self, screen):
        scale_factor = 0.3
        scaled_width = int(self.sprite.get_width() * scale_factor)
        scaled_height = int(self.sprite.get_height() * scale_factor)
        scaled_sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
    
        sprite_rect = scaled_sprite.get_rect(center=(screen.get_width() // 2, screen.get_height() // 1.2 ))
        screen.blit(scaled_sprite, sprite_rect)