import pygame
import sys
from sprites import *
from config import *
from tilemaps import *
from props import *
import os
from menu import *
from proc_gen import *
dirname = os.path.dirname(__file__)


class Game:
    def __init__(self):
        pygame.init()

        mixer.init()
        mixer.music.load(os.path.join(
            dirname, "../resources/mossy-sewer.mp3"))
        self.blood_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/blood_sound.wav"))
        self.click_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/click.mp3"))
        self.prop_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/select-sound.mp3"))
        self.ui_hover = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/bloop.mp3"))
        self.door_open = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/open-doors.mp3"))
        
       
        self.coin_sound = pygame.mixer.Sound(os.path.join(dirname, "../resources/coins.mp3"))
        
        self.swing_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/whoosh.mp3"))
        self.hit_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/hit.mp3"))
        self.death_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/death.mp3"))
        self.box_open = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/open_break.mp3"))
        self.wood_attack = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/wood_attack.mp3"))
        self.equip_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/equip.mp3"))
        self.drink_sound = pygame.mixer.Sound(
            os.path.join(dirname, "../resources/drink.mp3"))
        self.blood_sound.set_volume(0.03)
        self.click_sound.set_volume(0.3)
        self.prop_sound.set_volume(0.1)
        self.ui_hover.set_volume(0.02)
        self.door_open.set_volume(0.1)
        self.coin_sound.set_volume(0.05)
        self.swing_sound.set_volume(0.03)
        self.hit_sound.set_volume(0.05)
        self.death_sound.set_volume(0.05)
        self.box_open.set_volume(0.08)
        self.wood_attack.set_volume(0.1)
        self.drink_sound.set_volume(0.1)
        self.equip_sound.set_volume(0.05)
        mixer.music.set_volume(0.05)
        mixer.music.play(loops=-1)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        programIcon = pygame.image.load(
            os.path.join(dirname, "../images/Temp_Icon.png"))
        pygame.display.set_icon(programIcon)
        pygame.display.set_caption('Game')

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(os.path.join(
            dirname, "../fonts/04B_30__.TTF"), 32)
        self.font2 = pygame.font.Font(
            os.path.join(dirname, "../fonts/dogica.ttf"), 16)

        self.running = True
        self.intro_background = pygame.image.load(
            os.path.join(dirname, '../images/pxArt.png'))
        self.character_spritesheet = Spritesheet(
            os.path.join(dirname, '../images/Character.png'))
        self.enemy_spritesheet = Spritesheet(
            os.path.join(dirname, '../images/Enemy1.png'))
        self.damaged = Spritesheet(
            os.path.join(dirname, '../images/damaged.png'))
        
        self.attack_spritesheet = Spritesheet(os.path.join(dirname, '../images/attacks.png'))
        
        self.Wall_spritesheet = pygame.image.load(os.path.join(dirname, '../images/bricks.png'))

        self.score = 0
        self.health = 5
        # self.game_over_png = pygame.image.load('images/hilarious.png')
        self.wall_num = 0
        self.wall_list = []
        
        self.rooms = 0
    
        # self.terrain_spritesheet = Spritesheet('images/Terrain.png)

    def createTilemap(self, tilemap):
        
                    
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    Wall(self, os.path.join(dirname, '../images/bricks.png'), j, i)
                if column == 'b':
                    Ground(self, j, i)
                    Block(self, os.path.join(dirname, '../images/Bed.png'), j, i)
                if column == 'D':
                    Ground(self, j, i)
                    Door(self, os.path.join(dirname, '../images/Door.png'), j, i)
                
                if column == '.':
                    Ground(self, j, i)
                if column == 'e':
                    Enemy(self, j, i)
                    Ground(self, j, i)
                if column == 'c':
                    Prop(self, os.path.join(
                        dirname, '../images/coins.png'), j, i, 'chest')
                    Ground(self, j, i)
                    
                if column == "P":
                    Ground(self, j, i)
                    #Player(self, j, i)
                    
                if column =="■":
                    Ground(self, j, i)
                    Block(self, os.path.join(dirname, '../images/box.png'), j, i)
                if column == "^":
                    Ground(self, j, i)
                    SpecDoor(self,os.path.join(dirname, '../images/Door.png'), j, i, "up")
                    #Player(self, j, i)
                if column == "v":
                    Ground(self, j, i)
                    SpecDoor(self,os.path.join(dirname, '../images/Door.png'), j, i, "down")
                    #Player(self, j, i)
                if column == "<":
                    Ground(self, j, i)
                    SpecDoor(self,os.path.join(dirname, '../images/Door.png'), j, i, "left")
                    #Player(self, j, i)
                if column == ">":
                    Ground(self, j, i)
                    SpecDoor(self,os.path.join(dirname, '../images/Door.png'), j, i,"right")
                    #Player(self, j, i)
                if column == "?":
                    Ground(self, j, i)
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                
                if column == "P":
                    self.real_player = Player(self, j, i)
        

    def new(self):
        # new game starts

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.props = pygame.sprite.LayeredUpdates()
        self.specdoors = pygame.sprite.LayeredUpdates()
        self.walls  = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        
        self.destructables = pygame.sprite.LayeredUpdates()
        
        self.wall_num = 0
        self.wall_list = []
        self.createTilemap(room0)
        self.menu = Menu(self)
        self.score = 0
        self.health = 5
        self.rooms = 0
        
        
        # MenuGraphic(self)

    def events(self):
        # gameloop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(self.swing_sound)
                    if self.real_player.facing == 'up':
                        Attack(self,self.real_player.rect.x, self.real_player.rect.y - TILESIZE)
                    if self.real_player.facing == 'down':
                        Attack(self,self.real_player.rect.x, self.real_player.rect.y + TILESIZE)
                    if self.real_player.facing == 'left':
                        Attack(self,self.real_player.rect.x- TILESIZE, self.real_player.rect.y )
                    if self.real_player.facing == 'right':
                        Attack(self,self.real_player.rect.x+ TILESIZE, self.real_player.rect.y )

    def update(self):
        # gameloop updates
        self.all_sprites.update()
        self.menu.update(self)

    def draw(self):
        # gameloop draw
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        self.menu.update(self)
        self.clock.tick(FPS)

        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:

            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('GAME OVER', True, TITLE_TEXT)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/9))

        restart_button = Button(self, WINDOW_WIDTH/2 - 64,
                                WINDOW_HEIGHT - (2*WINDOW_HEIGHT/9), 128, 64)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            # self.screen.blit(self.game_over_png, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('Supermegaglop II', True, TITLE_TEXT)
        subtitle = self.font2.render('by Kevin Chang', True, TITLE_TEXT)
        title_rect = title.get_rect(x=30, y=30)
        subtitle_rect = title.get_rect(x=30, y=610)
        play_button = Button(self, 300, 500, 128, 64)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()

while g.running:

    g.main()
    g.game_over()

pygame.quit()
sys.exit()
