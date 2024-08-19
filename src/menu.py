from config import *
from tilemaps import *
from props import *
import os

dirname = os.path.dirname(__file__)

class Menu():
    
    def __init__(self,game):
        self.menu_background = pygame.image.load(os.path.join(dirname, "../images/Menu_Graphic.png"))
        game.screen.blit(self.menu_background, (0,GAME_HEIGHT))
        
    def score_counter(self, game):
        self.text = game.font2.render("Exp: " + str(game.score), True, TITLE_TEXT)
        self.text_rect = self.text.get_rect(topleft=(24, GAME_HEIGHT + 24))

        # self.screen.blit(self.game_over_png, (0, 0))
        game.screen.blit(self.text, self.text_rect)

    def health_counter(self, game):
        health_text = ""
        if game.health == 5 :
            health_text = "great"
        elif game.health == 4:
            health_text = "okay"
        elif game.health == 3:
            health_text = "bad"
        elif game.health == 2:
            health_text = "painful"
        elif game.health == 1:
            health_text = "terrible"
        else:
            health_text = "DEAD"
            
        self.text = game.font2.render("You feel " + str(health_text), True, TITLE_TEXT)
        self.text_rect = self.text.get_rect(topleft=(24, GAME_HEIGHT + 48))
        
        game.screen.blit(self.text, self.text_rect)
    
    def update(self, game):
        
        game.screen.blit(self.menu_background, (0,GAME_HEIGHT))
        self.score_counter(game)
        self.health_counter(game)
        
    
