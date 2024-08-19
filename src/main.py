import pygame
import sys
from sprites import *
from config import *
from tilemaps import *
from props import *
import os
from menu import *

dirname = os.path.dirname(__file__)


class Game:
    def __init__(self):
        pygame.init()

        mixer.init()
        mixer.music.load(os.path.join(
            dirname, "../resources/swamptheme1var.mp3"))
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
        self.blood_sound.set_volume(0.03)
        self.click_sound.set_volume(0.3)
        self.prop_sound.set_volume(0.1)
        self.ui_hover.set_volume(0.02)
        self.door_open.set_volume(0.1)
        mixer.music.set_volume(0.07)
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

        self.score = 0
        # self.game_over_png = pygame.image.load('images/hilarious.png')

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
                if column == "P":
                    Player(self, j, i)
                    Ground(self, j, i)
                if column == '.':
                    Ground(self, j, i)
                if column == 'e':
                    Enemy(self, j, i)
                    Ground(self, j, i)
                if column == 'c':
                    Prop(self, os.path.join(
                        dirname, '../images/chest.png'), j, i, 'chest')
                    Ground(self, j, i)

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

        self.createTilemap(tilemap2)
        self.menu = Menu(self)
        self.score = 0
        # MenuGraphic(self)

    def events(self):
        # gameloop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

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
