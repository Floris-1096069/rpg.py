import pygame

class Menu:
    def __init__(self, screen, text_renderer, input_handler):
        self.screen = screen
        self.text_renderer = text_renderer
        self.input_handler = input_handler
        self.options = [
            {"text": "Start Game", "action": "start_game", "y_offset": -50},
            {"text": "Options", "action": "options", "y_offset": 0},
            {"text": "Quit", "action": "quit", "y_offset": 50},
        ]
        self.selected_option = None
        self.hovered_option = None

    def update(self):
        input_state = self.input_handler.get_input_state()
        mouse_x, mouse_y = input_state["mouse_position"]
        mouse_buttons = input_state["mouse_buttons"]

        self.hovered_option = None
        for option in self.options:
            x = self.screen.get_width() // 2
            y = self.screen.get_height() // 2 + option["y_offset"]

            font_size = 30
            font = pygame.font.Font("src/graphics/assets/fonts/AngelWish.ttf", font_size)
            text_width = font.size(option["text"])[0]  
            option_rect = pygame.Rect(x - text_width // 2, y - 15, text_width, 30) 

            if option_rect.collidepoint(mouse_x, mouse_y):
                self.hovered_option = option["action"]
                if mouse_buttons.get(0, False):
                    self.selected_option = option["action"]
                    return option["action"]

        return None

    def render(self):
        self.screen.fill((20, 20, 40))
        self.text_renderer.render_text("RPG.py", 100, (255, 255, 255), (400, 100), align="center")

        for option in self.options:
            x = self.screen.get_width() // 2
            y = self.screen.get_height() // 2 + option["y_offset"]

            color = (255, 0, 0) if self.hovered_option == option["action"] else (255, 255, 255)
            self.text_renderer.render_text(option["text"], 30, color, (x, y), align="center")
            
            
class TitleScreen:
    def __init__(self, screen, text_renderer):
        self.screen = screen
        self.text_renderer = text_renderer
        self.start_time = pygame.time.get_ticks()
        
    def update(self):
        if (pygame.time.get_ticks() - self.start_time) // 1000 > 3:
            return "menu"
        return None

    def render(self):
        self.screen.fill((0, 0, 0))
        self.text_renderer.render_text("RPG.py", 200, (255, 255, 255), (400, 300), align="center")
        