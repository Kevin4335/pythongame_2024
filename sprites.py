import pygame 
from pygame import mixer
from config import *
import math, random

class Spritesheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite
        

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.player
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1
        
        self.image = self.game.character_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.movement()
        self.collide_enemy()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            #camera lock
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
                
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            #camera lock
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
                
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_s]:
            #camera lock
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
                
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_w]:
            #camera lock
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
                
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
            
    def collide_blocks(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    #camera lock
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    #camera lock
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right 
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    #camera lock
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    #camera lock
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom
                    
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies, False)
        if hits:
            pygame.mixer.Sound.play(self.game.blood_sound)

            self.kill()
            self.game.playing = False
        
                    
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,0,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,0,self.width,self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,16,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,16,self.width,self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,32,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,32,self.width,self.height)]
        
        left_animations = [self.game.character_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,48,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,48,self.width,self.height)]
        
        if self.facing == "down":
            if(self.y_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.game = game 
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
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


            
class Block(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.game = game 
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = pygame.image.load(file)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Prop(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.game = game 
        self._layer = PROP_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = pygame.image.load(file)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Door(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.game = game 
        self._layer = DOOR_LAYER
        self.groups = self.game.all_sprites, self.game.doors
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
        
    def update(self):
        
        if(pygame.sprite.spritecollide(self, self.game.player, False)):
            self.image = self.Door_spritesheet.get_sprite(32,0,self.width,self.height)
            
        else:
            self.image = self.Door_spritesheet.get_sprite(0,0,self.width,self.height)
            
        
    
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game 
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = pygame.image.load('./images/Stone_Brick.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class MenuGraphic(pygame.sprite.Sprite):
    def __init__(self,game):
        self.game = game
        self._layer = GROUND_LAYER
        
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 432
        self.width = 480
        self.height = 224
        
        self.image = pygame.image.load('./images/Menu_Graphic.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE


        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 1
        self.movement_loop = 0
        
        
        self.image = self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.facing = random.choice(['left','right', 'up', 'down'])
        self.max_travel = random.randint(16,32)

    def update(self):
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
        elif self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
        elif self.facing == 'up':
            self.y_change -= ENEMY_SPEED
            self.movement_loop-=1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
        elif self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop+=1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
    
    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,0,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,0,self.width,self.height)]
        
        up_animations = [self.game.enemy_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,16,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,16,self.width,self.height)]
        
        right_animations = [self.game.enemy_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,32,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,32,self.width,self.height)]
        
        left_animations = [self.game.enemy_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,48,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,48,self.width,self.height)]
        
        if self.facing == "down":
            if(self.y_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
    def collide_blocks(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or pygame.sprite.spritecollide(self, self.game.doors, False)
            if hits:
                if self.x_change > 0:
                    
                    
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    
                    self.rect.x = hits[0].rect.right 
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or pygame.sprite.spritecollide(self, self.game.doors, False)
            if hits:
                if self.y_change > 0:
                    
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    
                    self.rect.y = hits[0].rect.bottom


class Button:
    def __init__(self, game, x, y, width, height):
        
        
        
        self.x =x 
        self.y = y
        self.width = width 
        self.height = height
        self.game = game
        
        self.image = pygame.image.load('./images/start_button.png')
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        # self.text = self.font.render(self.content, True, self.fg)
        # self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        # self.image.blit(self.text,self.text_rect)
        
    def is_pressed(self, pos,pressed):
        
        if self.rect.collidepoint(pos):
            self.image = pygame.image.load('./images/start_button_pressed.png')
            if pressed[0]:
                pygame.mixer.Sound.play(self.game.click_sound)

                return True
            return False
        self.image = pygame.image.load('./images/start_button.png')
        return False
        
