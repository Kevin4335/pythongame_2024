import pygame 
from pygame import mixer
from config import *
import math, random
import os   
from sprites import *
from props import *
dirname = os.path.dirname(__file__)

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
        self.enemy_spritesheet = Spritesheet(
            os.path.join(dirname, '..','images', 'Enemy1.png'))
        self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.facing = random.choice(['left','right', 'up', 'down'])
        self.max_travel = random.choice([32, 48, 64, 128])
        
        self.distance_to_player =0
        self.relative_x = 0
        self.relative_y = 0
        
        self.down_animations = [self.enemy_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(32,0,self.width,self.height)]
        
        self.up_animations = [self.enemy_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,16,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(32,16,self.width,self.height)]
        
        self.right_animations = [self.enemy_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,32,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(32,32,self.width,self.height)]
        
        self.left_animations = [self.enemy_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,48,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(32,48,self.width,self.height)]

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
        
        self.die()
         
    def distance_calc(self):
        self.relative_x = self.rect.x - PLAYER_X
        self.relative_y = self.rect.y - PLAYER_Y
        self.distance_to_player = (math.sqrt((self.relative_x)**2+(self.relative_y)**2))
        
    def die(self):
        if self.health <=0:
            pygame.mixer.Sound.play(self.game.death_sound)
            self.kill()
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
                self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
    def collide_blocks(self,direction):
        spec_door_hit  = pygame.sprite.spritecollide(self, self.game.specdoors, False)
        collide_spec_door = []
        if spec_door_hit:
            
            if spec_door_hit[0].activated == False:
                collide_spec_door = spec_door_hit
                
        if direction == "x":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            
            if hits:
                
                if self.x_change > 0:
                    self.facing = random.choice(['left', 'up', 'down'])
                    
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.facing = random.choice(['right', 'up', 'down'])
                    self.rect.x = hits[0].rect.right 
            
                    
        if direction == "y":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            if hits:
                if self.y_change > 0:
                    self.facing = random.choice(['left','right', 'up'])
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.facing = random.choice(['left','right','down'])
                    self.rect.y = hits[0].rect.bottom


class EnemyMage(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = x
        self.j = y
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.health = 1

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE


        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 1
        self.movement_loop = 0
        self.self_speed = ENEMY_SPEED
        
        self.mage_spritesheet = Spritesheet(
            os.path.join(dirname, '..', 'images', 'Enemy2.png'))
        self.image = self.mage_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.facing = random.choice(['left','right', 'up', 'down'])
        self.max_travel = random.choice([32, 48, 64, 128])
        
        self.distance_to_player =0
        self.relative_x = 0
        self.relative_y = 0
        self.last = pygame.time.get_ticks()
        self.casting_cooldown = 1000 
        self.down_animations = [self.mage_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.mage_spritesheet.get_sprite(16,0,self.width,self.height),
                           self.mage_spritesheet.get_sprite(32,0,self.width,self.height)]
        
        self.up_animations = [self.mage_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.mage_spritesheet.get_sprite(16,16,self.width,self.height),
                           self.mage_spritesheet.get_sprite(32,16,self.width,self.height)]
        
        self.right_animations = [self.mage_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.mage_spritesheet.get_sprite(16,32,self.width,self.height),
                           self.mage_spritesheet.get_sprite(32,32,self.width,self.height)]
        
        self.left_animations = [self.mage_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.mage_spritesheet.get_sprite(16,48,self.width,self.height),
                           self.mage_spritesheet.get_sprite(32,48,self.width,self.height)]

    def update(self):
        self.distance_calc()
        if self.distance_to_player <96:
            
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
        
        self.die()
        
         
    def distance_calc(self):
        self.relative_x = self.rect.x - PLAYER_X
        self.relative_y = self.rect.y - PLAYER_Y
        self.distance_to_player = (math.sqrt((self.relative_x)**2+(self.relative_y)**2))
        
    def die(self):
        if self.health <=0:
            pygame.mixer.Sound.play(self.game.death_sound)
            self.kill()
    def movement_active(self):
        
        if abs(self.relative_x) >= abs(self.relative_y):
            if self.relative_x <0:
                self.facing = 'right'
            elif self.relative_x >0:
                self.facing = 'left'
        
        if abs(self.relative_y) >= abs(self.relative_x):           
            if self.relative_y <0:
                self.facing = 'down'
            elif self.relative_y >0:
                self.facing = 'up'
        
            
        self.now = pygame.time.get_ticks()
        if self.now - self.last >= self.casting_cooldown:
            self.last = self.now
            Bullet(self.game, self.rect.x, self.rect.y)
            
            
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
                self.image = self.mage_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.mage_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.mage_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.mage_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop>=3:
                    self.animation_loop = 1
                    
    def collide_blocks(self,direction):
        spec_door_hit  = pygame.sprite.spritecollide(self, self.game.specdoors, False)
        collide_spec_door = []
        if spec_door_hit:
            
            if spec_door_hit[0].activated == False:
                collide_spec_door = spec_door_hit
                
        if direction == "x":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            
            if hits:
                
                if self.x_change > 0:
                    self.facing = random.choice(['left', 'up', 'down'])
                    
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.facing = random.choice(['right', 'up', 'down'])
                    self.rect.x = hits[0].rect.right 
            
                    
        if direction == "y":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            if hits:
                if self.y_change > 0:
                    self.facing = random.choice(['left','right', 'up'])
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.facing = random.choice(['left','right','down'])
                    self.rect.y = hits[0].rect.bottom


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = x
        self.j = y
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x 
        self.y = y 
        self.width = 8
        self.height = 8
        self.health = 1

        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 1
        self.movement_loop = 0
        self.self_speed = ENEMY_SPEED + 1
        self.bullet_spritesheet = Spritesheet(
            os.path.join(dirname, '..', 'images', 'bullet.png'))
        self.image = self.bullet_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
        self.distance_to_player =0
        self.relative_x = 0
        self.relative_y = 0
        self.last = pygame.time.get_ticks()
        self.death_timer = 2000 
        
        
    def update(self):
        self.distance_calc()
        self.movement_active()
                
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.collide_blocks()
        
        self.x_change = 0
        self.y_change = 0
        if self.health <=0:
            self.kill()
            
        self.now = pygame.time.get_ticks()
        if self.now - self.last >= self.death_timer:
            self.last = self.now
            self.kill()
         
    def distance_calc(self):
        self.relative_x = self.rect.x - PLAYER_X - random.choice([-60,-28,-12,-4,4,8,16,32,64])
        self.relative_y = self.rect.y - PLAYER_Y - random.choice([-60,-28,-12,-4,4,8,16,32,64])
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
    
    def collide_blocks(self):
 
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or pygame.sprite.spritecollide(self, self.game.specdoors, False) or pygame.sprite.spritecollide(self, self.game.doors, False)
        player_hits = pygame.sprite.spritecollide(self, self.game.player, False)   
        if hits:
            self.kill()
        
        if player_hits:
            self.game.real_player.damage()
            self.kill()
        
            
            
class Bombguy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = x
        self.j = y
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.health = 2

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE


        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 0
        self.movement_loop = 0
        self.self_speed = ENEMY_SPEED
        self.enemy_spritesheet = Spritesheet(
            os.path.join(dirname, '..', 'images', 'Enemy3.png'))
        self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.facing = random.choice(['left','right', 'up', 'down'])
        self.max_travel = random.choice([32, 48, 64, 128])
        
        self.distance_to_player =0
        self.relative_x = 0
        self.relative_y = 0
        
        self.down_animations = [self.enemy_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,0,self.width,self.height),]
        
        self.up_animations = [self.enemy_spritesheet.get_sprite(0,16,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,16,self.width,self.height),]
        
        self.right_animations = [self.enemy_spritesheet.get_sprite(0,32,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,32,self.width,self.height),]
        
        self.left_animations = [self.enemy_spritesheet.get_sprite(0,48,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(16,48,self.width,self.height),]

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
        
        self.die()
         
    def distance_calc(self):
        self.relative_x = self.rect.x - PLAYER_X
        self.relative_y = self.rect.y - PLAYER_Y
        self.distance_to_player = (math.sqrt((self.relative_x)**2+(self.relative_y)**2))
        if self.distance_to_player <= 16:
            pygame.mixer.Sound.play(self.game.explode_sound)
            Explosion(self.game,self.rect.x-16,self.rect.y-16)
            self.kill()
        
    def die(self):
        if self.health <=0:
            pygame.mixer.Sound.play(self.game.explode_sound)
            Explosion(self.game,self.rect.x-16,self.rect.y-16)
            self.kill()
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
                self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.07
                if self.animation_loop>=2:
                    self.animation_loop = 0
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,16,self.width,self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.07
                if self.animation_loop>=2:
                    self.animation_loop = 0
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,48,self.width,self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.07
                if self.animation_loop>=2:
                    self.animation_loop = 0
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,32,self.width,self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.07
                if self.animation_loop>=2:
                    self.animation_loop = 0
                    
    def collide_blocks(self,direction):
        spec_door_hit  = pygame.sprite.spritecollide(self, self.game.specdoors, False)
        collide_spec_door = []
        if spec_door_hit:
            
            if spec_door_hit[0].activated == False:
                collide_spec_door = spec_door_hit
                
        if direction == "x":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            
            if hits:
                
                if self.x_change > 0:
                    self.facing = random.choice(['left', 'up', 'down'])
                    
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.facing = random.choice(['right', 'up', 'down'])
                    self.rect.x = hits[0].rect.right 
            
                    
        if direction == "y":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            if hits:
                if self.y_change > 0:
                    self.facing = random.choice(['left','right', 'up'])
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.facing = random.choice(['left','right','down'])
                    self.rect.y = hits[0].rect.bottom


class Explosion(pygame.sprite.Sprite):
    
    def __init__(self,game, x,y):
        self.game = game 
        self._layer = ATTACKS_LAYER
        self.groups = self.game.all_sprites,self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x = x
        self.y = y
        self.width = 48
        self.height = 48
        
        self.animation_loop = 0
        
        self.image = self.game.explode_spritesheet.get_sprite(0,0,self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.hit = False
        self.explode = [
            self.game.explode_spritesheet.get_sprite(0,0,self.width,self.height),
            self.game.explode_spritesheet.get_sprite(48,0,self.width,self.height),
            self.game.explode_spritesheet.get_sprite(96,0,self.width,self.height),
            
        ]
    
    def update(self):
        
        
        self.collide()
        self.animate()
        
        
    def collide(self):
        
        
        player_hit = pygame.sprite.spritecollide(self, self.game.player, False)
        if player_hit and (self.hit == False):
            self.game.real_player.damage()
            self.game.real_player.damage()
            self.hit = True
            pygame.mixer.Sound.play(self.game.hit_sound)
            
        box_hit = pygame.sprite.spritecollide(self,self.game.destructables, False)
        if box_hit:
            for box in box_hit:
                box.health = box.health -1
    
    def animate(self):
        
        self.image=self.explode[math.floor(self.animation_loop)]
        self.animation_loop+=0.5
        
        if self.animation_loop >=3:
            self.kill()
                

class BombBoss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = x
        self.j = y
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.health = 25

        self.x = x * TILESIZE 
        self.y = y * TILESIZE
        self.width = TILESIZE *3
        self.height = TILESIZE *3


        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 1
        self.movement_loop = 0
        self.self_speed = ENEMY_SPEED
        self.enemy_spritesheet = Spritesheet(
            os.path.join(dirname, '..', 'images', 'BombBoss.png'))
        self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.facing = random.choice(['left','right', 'up', 'down'])
        self.max_travel = random.choice([32, 48, 64, 128])
        
        self.distance_to_player =0
        self.relative_x = 0
        self.relative_y = 0
        
        self.move = [self.enemy_spritesheet.get_sprite(0,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(48,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(96,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(144,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(192,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(240,0,self.width,self.height),
                           self.enemy_spritesheet.get_sprite(288,0,self.width,self.height),]
        self.last = pygame.time.get_ticks()
        self.casting_cooldown = 2000 
        
    

    def update(self):
        self.distance_calc()
        if self.distance_to_player <164:
            self.spawnAts()
              
        self.movement_idle()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        self.x_change = 0
        self.y_change = 0
        
        self.die()
         
    def distance_calc(self):
        self.relative_x = self.rect.x - PLAYER_X
        self.relative_y = self.rect.y - PLAYER_Y
        self.distance_to_player = (math.sqrt((self.relative_x)**2+(self.relative_y)**2))
    
    def spawnAts(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last >= self.casting_cooldown:
            self.last = self.now
            Bombguy(self.game, (self.rect.x // 16) + 1, (self.rect.y // 16) + 1 )
    
    def die(self):
        if self.health <=0:
            pygame.mixer.Sound.play(self.game.explode_sound)
            Explosion(self.game,self.rect.x-16,self.rect.y-16)
            Explosion(self.game,self.rect.x-8,self.rect.y-16)
            Explosion(self.game,self.rect.x-32,self.rect.y-32)
            Explosion(self.game,self.rect.x-16,self.rect.y-32)
            Explosion(self.game,self.rect.x,self.rect.y)
            for i in range(0,32):
                rand_pos_x = random.randint(4,46)
                rand_pos_y = random.randint(4,46)
                Prop(self.game, os.path.join(
                                        dirname, '..', 'images', 'coins.png'), self.rect.x + rand_pos_x, self.rect.y +rand_pos_y , 'coin')
            self.kill()
    
    
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
                self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.move[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop>=7:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if(self.y_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.move[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop>=7:
                    self.animation_loop = 1
                    
        if self.facing == "left":
            if(self.x_change == 0):
                self.image =self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.move[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop>=7:
                    self.animation_loop = 1
                    
        if self.facing == "right":
            if(self.x_change == 0):
                self.image = self.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
            else:
                self.image = self.move[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop>=7:
                    self.animation_loop = 1
                    
    def collide_blocks(self,direction):
        spec_door_hit  = pygame.sprite.spritecollide(self, self.game.specdoors, False)
        collide_spec_door = []
        if spec_door_hit:
            
            if spec_door_hit[0].activated == False:
                collide_spec_door = spec_door_hit
                
        if direction == "x":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            
            if hits:
                
                if self.x_change > 0:
                    self.facing = random.choice(['left', 'up', 'down'])
                    
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.facing = random.choice(['right', 'up', 'down'])
                    self.rect.x = hits[0].rect.right 
            
                    
        if direction == "y":
            
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) or collide_spec_door
            if hits:
                if self.y_change > 0:
                    self.facing = random.choice(['left','right', 'up'])
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.facing = random.choice(['left','right','down'])
                    self.rect.y = hits[0].rect.bottom
