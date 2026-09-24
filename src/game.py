import pygame
from enum import Enum

from config import Config
from graphics.renderer.camera import Camera
from graphics.renderer.text_renderer import TextRenderer
from src.input_handler import InputHandler
from dev.test_rect import TestRect
from graphics.renderer.renderer import Renderer
from src.entities.player import Player

class Game:
    class State(Enum):
        TITLE = "title"
        MENU = "menu"
        GAME = "game"
        OPTIONS = "options"
        SAVE = "save"
        LOAD = "load"
        
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('PythonRPG')
        self.config = Config()
        
        #Logic
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = Game.State.TITLE
        
        #Input
        self.input_handler = InputHandler()

        #Graphics
        self.screen = pygame.Surface(self.config.resolution)
        self.display = pygame.display.set_mode(self.config.resolution)
        buffer_width = self.config.resolution[0] // 2
        buffer_height = self.config.resolution[1] // 2
        self.buffer = pygame.Surface((buffer_width, buffer_height))
        self.texture = pygame.image.load("src/graphics/assets/floor_1.png").convert()
        self.camera = Camera()
        self.player = Player(self.camera)
        self.renderer = Renderer(self.texture, self.buffer, self.screen, self.camera)

        self.title_renderer = TextRenderer(
            "PythonRPG", 100, (255, 255, 255),
            (self.config.resolution[0] // 2, 200), #x - y
            self.screen, align="center"
        )
        
        
    def handle_input(self):
        self.input_handler.update()
        self.input_state = self.input_handler.get_input_state()

    def handle_quit(self):
        keys = self.input_state["keys"]
        if pygame.K_ESCAPE in keys:
            self.running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
    def clear(self):
        self.screen.fill((0, 0, 0))
        
    def change_state(self):
        keys = self.input_state["keys"]
        if pygame.K_m in keys:
            self.current_state = Game.State.GAME
            
    def title_screen(self):
        self.title_renderer.render_text()
    
    def menu_screen(self):
        pass
    
    def options_screen(self):
        pass
    
    def game_screen(self):
        if self.current_state == Game.State.GAME:
            self.camera.update(self.input_state)
            self.renderer.mode7()
            self.renderer.upscale()
            self.player.draw(self.screen)
            
    def screen_selector(self):
        if Game.State.TITLE:
            self.title_screen()
        if Game.State.GAME:
            self.game_screen()
            
            
    def draw(self):
        self.display.blit(self.screen, (0,0))
        pygame.display.update()
        
    #Gameloop
    def run(self):
        while self.running:              
            self.handle_input()
            self.handle_quit()
            self.clear()        
            self.change_state()
            self.screen_selector()
            self.draw()
            self.clock.tick(self.config.fps)