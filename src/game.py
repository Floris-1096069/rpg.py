import pygame
from enum import Enum

from config import Config
from graphics.renderer.camera import Camera
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
        self.test_rect = TestRect(self.screen, self.config)

        buffer_width = self.config.resolution[0] // 2
        buffer_height = self.config.resolution[1] // 2
        self.buffer = pygame.Surface((buffer_width, buffer_height))
        self.texture = pygame.image.load("src/graphics/assets/floor_1.png").convert()
        self.camera = Camera()
        self.player = Player(self.camera)
        self.renderer = Renderer(self.texture, self.buffer, self.screen, self.camera)
        
        
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

    def game_screen(self):
        if self.current_state == Game.State.GAME:
            self.camera.update(self.input_state)
            self.renderer.mode7()
            self.renderer.upscale()
            self.player.draw(self.screen)
            #self.test_rect.update(self.input_state)
            #self.test_rect.draw()
            
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
            self.game_screen()
            self.draw()
            self.clock.tick(self.config.fps)