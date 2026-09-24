import pygame

class TextRenderer:
    def __init__(self, screen, font_path="src/graphics/assets/fonts/AngelWish.ttf"):
        self.screen = screen
        self.font_path = font_path
        self.font_cache = {}

    def render_text(self, text, size, color, position, align="left"):
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(self.font_path, size)
        font = self.font_cache[size]

        text_surface = font.render(text, True, color)

        if align == "center":
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)
        elif align == "right":
            text_rect = text_surface.get_rect(right=position[0], y=position[1])
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, position)