import pygame

class TextRenderer:
    def __init__(self, text, size, color, position, screen ,align="left"):
        self.text = text
        self.font = pygame.font.Font("src/graphics/assets/fonts/AngelWish.ttf", size)
        self.color = color
        self.position = position
        self.screen = screen
        self.align = align
        
    def render_text(self):
        text_surface = self.font.render(self.text, True, self.color)
        if self.align == "center":
            text_rect = text_surface.get_rect(center=self.position)
            self.screen.blit(text_surface, text_rect)
        elif self.align == "right":
            text_rect = text_surface.get_rect(right=self.position[0], y=self.position[1])
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, self.position)

    def update_text(self, new_text):
        self.text = new_text