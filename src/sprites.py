import pygame 
from pygame import mixer
from config import *
import math, random
import os

dirname = os.path.dirname(__file__)




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
        self.i = x
        self.j = y
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
        
        self.health = game.health
        self.collided = False
        
        self.last = pygame.time.get_ticks()
        self.damage_cooldown = 1000 
        
        self.down_animations = [self.game.character_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,0,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,0,self.width,self.height)]
        
        self.up_animations = [self.game.character_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,16,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,16,self.width,self.height)]
        
        self.right_animations = [self.game.character_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,32,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,32,self.width,self.height)]
        
        self.left_animations = [self.game.character_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(16,48,self.width,self.height),
                           self.game.character_spritesheet.get_sprite(32,48,self.width,self.height)]
        
        
        #initial camera lock
        for sprite in self.game.all_sprites:
            sprite.rect.x = PLAYER_X + sprite.rect.x - self.x
            sprite.rect.y = PLAYER_Y + sprite.rect.y - self.y
            
        
    def update(self):
        self.movement()
        
        self.animate()
        
        self.collide_enemy()
        
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
            self.now = pygame.time.get_ticks()
            if self.now - self.last >= self.damage_cooldown:
                self.last = self.now
                
                pygame.mixer.Sound.play(self.game.blood_sound)
                
                self.game.health = self.game.health-1
                
                
                self.flicker()
                
                if self.game.health <=0:
                    
                    self.kill()
                    self.game.playing = False
                
            self.collided = True
        else:
            self.collided = False
        
    def flicker(self):
        self.alast = pygame.time.get_ticks()
        self.flicker_timer = 100
        # print("HI!")
        
        self.image = self.game.damaged.get_sprite(0,0,self.width,self.height)
        
                
                    
    def animate(self):
        
        if self.facing == "down":
            if(self.y_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.game.character_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.i = x
        self.j = y
        self.game = game 
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.Wall_spritesheet = Spritesheet(file)
        self.image = self.Wall_spritesheet.get_sprite(0,0,self.width,self.height)
               
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.wall_num = self.game.wall_num
        self.game.wall_list.append((self.rect.x, self.rect.y))
        
        self.game.wall_num = self.game.wall_num +1
        
        
    def pseudoUpdate(self):
        self.game.wall_list[self.wall_num] = (self.rect.x, self.rect.y)


            
class Block(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.i = x
        self.j = y
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


class Door(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y):
        self.i = x
        self.j = y
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
        
        self.opened = 0
        
        
        
    def update(self):
        
        
        if(pygame.sprite.spritecollide(self, self.game.player, False)):
            self.image = self.Door_spritesheet.get_sprite(32,0,self.width,self.height)
            if self.opened == 0:
                pygame.mixer.Sound.play(self.game.door_open)
                
            self.opened = 1
        else:
            self.image = self.Door_spritesheet.get_sprite(0,0,self.width,self.height)
            self.opened = 0
            
        
    
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = x
        self.j = y
        self.game = game 
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = pygame.image.load(os.path.join(dirname, "../images/Stone_Brick.png"))
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
        
        self.image = pygame.image.load(os.path.join(dirname, '../images/Menu_Graphic.png'))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = x
        self.j = y
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.health = 3

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE


        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 1
        self.movement_loop = 0
        self.self_speed = ENEMY_SPEED
        
        self.image = self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.facing = random.choice(['left','right', 'up', 'down'])
        self.max_travel = random.choice([32, 48, 64, 128])
        
        self.distance_to_player =0
        self.relative_x = 0
        self.relative_y = 0
        
        self.down_animations = [self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,0,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,0,self.width,self.height)]
        
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,16,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,16,self.width,self.height)]
        
        self.right_animations = [self.game.enemy_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,32,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,32,self.width,self.height)]
        
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(16,48,self.width,self.height),
                           self.game.enemy_spritesheet.get_sprite(32,48,self.width,self.height)]

    def update(self):
        self.distance_calc()
        if self.distance_to_player <72:
            
            self.movement_active()
        else:          
            self.movement_idle()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
        
        if self.health <=0:
            self.kill()
         
    def distance_calc(self):
        self.relative_x = self.rect.x - PLAYER_X
        self.relative_y = self.rect.y - PLAYER_Y
        self.distance_to_player = (math.sqrt((self.relative_x)**2+(self.relative_y)**2))
        
        
    def movement_active(self):
        
        
        if self.relative_x <0:
            self.facing = 'right'
            self.movement_forward()
        elif self.relative_x >0:
            self.facing = 'left'
            self.movement_forward()
        
                   
        if self.relative_y <0:
            self.facing = 'down'
            self.movement_forward()
        elif self.relative_y >0:
            self.facing = 'up'
            self.movement_forward()

    def movement_forward(self):
        if self.facing == 'left':
            self.x_change -= self.self_speed
            self.movement_loop-=1
            # if self.movement_loop <= -self.max_travel:
            #     self.max_travel = random.choice([32, 48, 64, 128])
        elif self.facing == 'right':
            self.x_change += self.self_speed
            self.movement_loop+=1
            # if self.movement_loop >= self.max_travel:
            #     self.max_travel = random.choice([32, 48, 64, 128])
        elif self.facing == 'up':
            self.y_change -= self.self_speed
            self.movement_loop-=1
            # if self.movement_loop <= -self.max_travel:
            #     self.max_travel = random.choice([32, 48, 64, 128])
        elif self.facing == 'down':
            self.y_change += self.self_speed
            self.movement_loop+=1
            # if self.movement_loop >= self.max_travel:
            #     self.max_travel = random.choice([32, 48, 64, 128])
    def movement_idle(self):
        if self.facing == 'left':
            self.x_change -= self.self_speed
            self.movement_loop-=1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
                self.max_travel = random.choice([32, 48, 64, 128])
        elif self.facing == 'right':
            self.x_change += self.self_speed
            self.movement_loop+=1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
                self.max_travel = random.choice([32, 48, 64, 128])
        elif self.facing == 'up':
            self.y_change -= self.self_speed
            self.movement_loop-=1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
                self.max_travel = random.choice([32, 48, 64, 128])
        elif self.facing == 'down':
            self.y_change += self.self_speed
            self.movement_loop+=1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left','right', 'up', 'down'])
                self.max_travel = random.choice([32, 48, 64, 128])
    
    def animate(self):
       
        
        if self.facing == "down":
            if(self.y_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.game.enemy_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
    def collide_blocks(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or pygame.sprite.spritecollide(self, self.game.doors, False) or pygame.sprite.spritecollide(self, self.game.specdoors, False)
            if hits:
                if self.x_change > 0:
                    self.facing = random.choice(['left', 'up', 'down'])
                    
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.facing = random.choice(['right', 'up', 'down'])
                    self.rect.x = hits[0].rect.right 
            
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or pygame.sprite.spritecollide(self, self.game.doors, False) or pygame.sprite.spritecollide(self, self.game.specdoors, False)
            if hits:
                if self.y_change > 0:
                    self.facing = random.choice(['left','right', 'up'])
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.facing = random.choice(['left','right','down'])
                    self.rect.y = hits[0].rect.bottom


class Button:
    def __init__(self, game, x, y, width, height):
        
        
        
        self.x =x 
        self.y = y
        self.width = width 
        self.height = height
        self.game = game
        self.collided = False
        self.image = pygame.image.load(os.path.join(dirname, '../images/start_button.png'))
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        # self.text = self.font.render(self.content, True, self.fg)
        # self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        # self.image.blit(self.text,self.text_rect)
        
    def is_pressed(self, pos,pressed):
        
        
        if self.rect.collidepoint(pos):
            self.image = pygame.image.load(os.path.join(dirname, '../images/start_button_pressed.png'))
            if self.collided == False:
                pygame.mixer.Sound.play(self.game.ui_hover)
            self.collided = True
            
            if pressed[0]:
                pygame.mixer.Sound.play(self.game.click_sound)

                return True
            return False
        self.image = pygame.image.load(os.path.join(dirname, '../images/start_button.png'))
        self.collided = False
        return False

class Attack(pygame.sprite.Sprite):
    
    def __init__(self,game, x,y):
        self.game = game 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites,self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.animation_loop = 0
        
        self.image = self.game.attack_spritesheet.get_sprite(0,0,self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.hit = False
        self.right_animations = [
            self.game.attack_spritesheet.get_sprite(0,32,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(16,32,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(32,32,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(48,32,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(64,32,self.width,self.height),
        ]
        self.down_animations = [
            self.game.attack_spritesheet.get_sprite(0,16,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(16,16,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(32,16,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(48,16,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(64,16,self.width,self.height),
        ]
        self.left_animations = [
            self.game.attack_spritesheet.get_sprite(0,48,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(16,48,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(32,48,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(48,48,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(64,48,self.width,self.height),
        ]
        self.up_animations = [
            self.game.attack_spritesheet.get_sprite(0,0,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(16,0,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(32,0,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(48,0,self.width,self.height),
            self.game.attack_spritesheet.get_sprite(64,0,self.width,self.height),
        ]
    
    def update(self):
        self.animate()
        self.collide()
        
    def collide(self):
        
        
        enemy_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if enemy_hit and (self.hit == False):
            self.hit = True
            enemy_hit[0].health =enemy_hit[0].health-1
            pygame.mixer.Sound.play(self.game.hit_sound)
    
    def animate(self):
        direction = self.game.real_player.facing
        
        
        
        if direction == 'up':
            self.image=self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.8
            
            if self.animation_loop >=5:
                self.kill()
                
        if direction == 'down':
            self.image=self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.8
            
            if self.animation_loop >=5:
                self.kill()
        
        if direction == 'left':
            self.image=self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.8
            
            if self.animation_loop >=5:
                self.kill()
                
        if direction == 'right':
            self.image=self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop+=0.8
            
            if self.animation_loop >=5:
                self.kill()

