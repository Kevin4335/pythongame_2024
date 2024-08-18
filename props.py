import pygame
import sys
from sprites import *
from config import *
from tilemaps import *

def score_update(game, num):
    
    if game.score > 99:
        pass
    elif game.score < 0:
        pass
    else:    
        game.score = game.score + num



class Prop(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y, type):
        self.game = game 
        self._layer = PROP_LAYER
        self.groups = self.game.all_sprites, self.game.props
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.Chest_spritesheet = Spritesheet(file)
        self.image = self.Chest_spritesheet.get_sprite(0,0,self.width,self.height)
               
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self, game):
        
        if(pygame.sprite.spritecollide(self, self.game.player, False)):
            pygame.mixer.Sound.play(self.game.prop_sound)
            score_update(game, 1)
            self.kill()
            