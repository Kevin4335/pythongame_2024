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
        self.type = type
        self.x = x
        self.y = y 
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.Chest_spritesheet = Spritesheet(file)
        self.image = self.Chest_spritesheet.get_sprite(0,0,self.width,self.height)
               
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        
        if self.type == "coin":
            if(pygame.sprite.spritecollide(self, self.game.player, False)):
                pygame.mixer.Sound.play(self.game.coin_sound)
                score_update(self.game, 1)
                self.kill()
        elif self.type=="1Pot":
            if(pygame.sprite.spritecollide(self, self.game.player, False)):
                pygame.mixer.Sound.play(self.game.drink_sound)
                self.game.health = self.game.health + 1
                self.kill()
            

class Box(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.i = x
        self.j = y
        self.game = game 
        self._layer = DOOR_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.destructables
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.Door_spritesheet = Spritesheet(file)
        self.image = self.Door_spritesheet.get_sprite(0,0,self.width,self.height)
               
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.health = 3    
        
        
    def update(self):
        
        
        self.die()
            
    def die(self):
        
        if self.health <=0:
            
            pygame.mixer.Sound.play(self.game.box_open)
            Prop(self.game, os.path.join(
                dirname, '../images/potion_1.png'),self.rect.x ,self.rect.y , '1Pot')
            self.kill()
            
        
    