import pygame, sys, math, random
from sprites import *
from config import *
from tilemaps import *

class Game: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        programIcon = pygame.image.load('./images/Temp_Icon.png')
        pygame.display.set_icon(programIcon)
        pygame.display.set_caption('BIH Gates I')
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('./fonts/04B_30__.TTF', 32)
        
        self.running = True;
        
        self.character_spritesheet = Spritesheet('./images/Character.png')
        #self.terrain_spritesheet = Spritesheet('./images/Terrain.png)
    def createTilemap(self, tilemap):
        for i ,row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    Wall(self, './images/bricks.png', j, i)
                if column == 'c':
                    Ground(self, j, i)
                    Block(self, './images/Bed.png', j, i)
                if column == 'D':
                    Ground(self, j, i)
                    Door(self, './images/Door.png', j, i)
                if column == "P":
                    Player(self, j, i)
                    Ground(self, j, i)
                if column == '.':
                    Ground(self, j, i)
                    

    def new(self):
        #new game starts
        
        self.playing = True;
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        
        self.createTilemap(tilemap2)
        
        MenuGraphic(self)

    def events(self):
        #gameloop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        
    def update(self):
        #gameloop updates
        self.all_sprites.update()
        
    def draw(self):
        #gameloop draw
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
        
        
    def main(self): 
        #game loop 
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    def game_over(self):
        pass
    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()
    
pygame.quit()
sys.exit()

