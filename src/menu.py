from config import *
from tilemaps import *
from props import *
import os

dirname = os.path.dirname(__file__)

class Menu():
    
    def __init__(self,game):
        self.menu_background = pygame.image.load(os.path.join(dirname, "../images/Menu_Graphic.png"))
        game.screen.blit(self.menu_background, (0,GAME_HEIGHT))
        
        self.last = pygame.time.get_ticks()
        self.upgrade_last = pygame.time.get_ticks()
        self.warning_cooldown = 3000 
        
    def score_counter(self, game):
        self.text = game.font2.render("$$$: " + str(game.score), True, TITLE_TEXT)
        self.text_rect = self.text.get_rect(topleft=(24, GAME_HEIGHT + 24))

        # self.screen.blit(self.game_over_png, (0, 0))
        game.screen.blit(self.text, self.text_rect)

    def health_counter(self, game):
        health_text = str(game.health)
        
            
        self.text = game.font2.render("You feel " + str(health_text), True, TITLE_TEXT)
        self.text_rect = self.text.get_rect(topleft=(24, GAME_HEIGHT + 48))
        
        game.screen.blit(self.text, self.text_rect)
    
    def update(self, game):
        
        game.screen.blit(self.menu_background, (0,GAME_HEIGHT))
        self.score_counter(game)
        self.health_counter(game)
        self.money_warn(game)
        self.upgrade_warn(game)
    def money_warn(self,game):
        self.text = game.font2.render("Not enough coins!", True, TITLE_TEXT)
        self.text_rect = self.text.get_rect(topleft=(24, GAME_HEIGHT + 72))
        
        self.now = pygame.time.get_ticks()
        
        
        if self.now - self.last <= self.warning_cooldown and game.money_warn == True:
            
            
            game.screen.blit(self.text, self.text_rect)
        else:
            game.money_warn = False
            self.last = self.now
            
    def upgrade_warn(self, game):
        self.text = game.font2.render("Already have this!", True, TITLE_TEXT)
        self.text_rect = self.text.get_rect(topleft=(24, GAME_HEIGHT + 72))
        
        self.upgrade_now = pygame.time.get_ticks()
        
        if self.upgrade_now - self.upgrade_last <= self.warning_cooldown and game.upgrade_warn == True:
            
            
            game.screen.blit(self.text, self.text_rect)
        else:
            game.upgrade_warn = False
            self.upgrade_last = self.upgrade_now
        
            
        
    
