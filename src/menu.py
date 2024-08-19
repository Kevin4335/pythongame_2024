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
        text = game.font2.render("Exp: " + str(game.score), True, TITLE_TEXT)
        text_rect = text.get_rect(topleft=(24, GAME_HEIGHT + 24))

        # self.screen.blit(self.game_over_png, (0, 0))
        game.screen.blit(text, text_rect)

    def update(self, game):
        
        game.screen.blit(self.menu_background, (0,GAME_HEIGHT))
        self.score_counter(game)
        
    
