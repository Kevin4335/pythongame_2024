import pygame 
from pygame import mixer
from config import *
import math, random
import os
from tilemaps import *
from sprites import *
from props import *
from enemies import *
from maps import down_maps 
from maps import left_maps
from maps import right_maps
from maps import up_maps


class SpecDoor(pygame.sprite.Sprite):
    def __init__(self, game, file, x, y, type):
        self.game = game 
        self._layer = DOOR_LAYER
        self.groups = self.game.all_sprites, self.game.specdoors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.type = type
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
        self.activated = 0
        self.rows = 0
        self.cols = 0
        self.room = room0      
        self.room_size = 0  
        
    def activate(self):
        if self.activated == 0:
            for wall in self.game.walls:
                wall.pseudoUpdate()
            
            self.create_room()
        
    
        self.activated = 1
    
    def create_room(self):
        if self.type == "right":
            self.room = random.choice(right_maps.right_maps)
        elif self.type == "down":
            self.room = random.choice(down_maps.down_maps)
        elif self.type == "left":
            self.room = random.choice(left_maps.left_maps)
        elif self.type == "up":
            self.room = random.choice(up_maps.up_maps)
        self.new_start_x =-1
        self.new_start_y = -1
        
        self.createTiles()
    
    def update(self):
        
        collide_non_player = pygame.sprite.spritecollide(self, self.game.enemies, False)
        # if(collide_non_player and self.activated ==0):
        #     collide_non_player[0].kill()
        
        if(pygame.sprite.spritecollide(self, self.game.player, False) or (collide_non_player and self.activated ==1) ):
            self.image = self.Door_spritesheet.get_sprite(32,0,self.width,self.height)
            if self.opened == 0:
                pygame.mixer.Sound.play(self.game.door_open)
            
            
            self.activate()
            self.opened = 1
        else:
            self.image = self.Door_spritesheet.get_sprite(0,0,self.width,self.height)
            self.opened = 0
        
                        
    def createTiles(self):
        
        for i, row in enumerate(self.room):
            self.rows = self.rows +1
            for j, column in enumerate(row):
                self.cols = j
                if column == "?":
                    self.new_start_x = j
                    self.new_start_y = i
        
        self.check_collide_tiles(self.rows, self.cols)
        
        self.rows = 0
        self.cols =0
        for i, row in enumerate(self.room):
            self.rows = self.rows +1
            for j, column in enumerate(row):
                self.cols = j
                if column == "?":
                    self.new_start_x = j
                    self.new_start_y = i
                if column == ".":
                    self.room_size = self.room_size +1
            
        self.tile_generate()
        
    def tile_generate(self):
        if self.room != plugD and self.room != plugL and self.room != plugR and self.room != plugU:
            
            self.game.rooms = self.game.rooms + 1
        j_modifier = 0
        i_modifier = 0
        
        if self.type == "down":
            j_modifier = (self.rect.x/16) - self.new_start_x
            i_modifier = (self.rect.y/16) + self.new_start_y
        elif self.type == "right":
            j_modifier = (self.rect.x/16) + self.new_start_x
            i_modifier = (self.rect.y/16) - self.new_start_y
        elif self.type == "left":
            j_modifier = (self.rect.x/16) - self.new_start_x
            i_modifier = (self.rect.y/16) - self.new_start_y
        elif self.type == "up":
            j_modifier = (self.rect.x/16) - self.new_start_x
            i_modifier = (self.rect.y/16) - self.new_start_y
        
        
        num_loots = random.randint(3, 15)
        num_enemies = random.randint(1,5)
        num_boxes = random.randint(0,5)
        for i, row in enumerate(self.room):
                for j, column in enumerate(row):                                                                               
                    if column == "B":
                        Wall(self.game, os.path.join(dirname, '../images/bricks.png'), j+ j_modifier, i + i_modifier )
                    if column == 'b':
                        Ground(self.game, j+ j_modifier, i + i_modifier )
                        Block(self.game, os.path.join(dirname, '../images/Bed.png'), j + j_modifier, i + i_modifier )
                    if column == 'D':
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        Door(self.game, os.path.join(dirname, '../images/Door.png'), j + j_modifier, i + i_modifier )
                    
                    if column == '.':
                        
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        
                        
                        loot_gen = False
                        loot_gen = random.choices(
                                population=[True, False],
                                weights=[(num_loots/self.room_size)*100.0,(1-(num_loots/self.room_size))*100.0],
                                k=1
                            )
                        enemy_gen = False
                        enemy_gen = random.choices(
                                population=[True, False],
                                weights=[(num_enemies/self.room_size)*100.0,(1-(num_enemies/self.room_size))*100.0],
                                k=1
                            )
                        box_gen = False
                        box_gen = random.choices(
                                population=[True, False],
                                weights=[(num_boxes/self.room_size)*100.0,(1-(num_boxes/self.room_size))*100.0],
                                k=1
                            )
                        if loot_gen[0] == True:
                            if num_loots>0:
                                Prop(self.game, os.path.join(
                                    dirname, '../images/coins.png'), (j + j_modifier)*16, (i + i_modifier)*16 , 'coin')
                                num_loots = num_loots -1
                        elif enemy_gen[0] == True:
                            if num_enemies>0:
                                enemy_type_gen = random.choices(
                                    population=["1", "2", "3"],
                                    weights=[40,20,40],
                                    k=1
                                )
                                if enemy_type_gen[0] == "1":
                                    
                                    Enemy(self.game, j + j_modifier, i + i_modifier )
                                elif enemy_type_gen[0] == "2":
                                    EnemyMage(self.game, j + j_modifier, i + i_modifier )
                                elif enemy_type_gen[0] == "3":
                                    Bombguy(self.game, j + j_modifier, i + i_modifier )
                                num_enemies = num_enemies -1
                        elif box_gen[0] == True:
                            if num_boxes>0:
                                Box(self.game, os.path.join(dirname, '../images/box.png'), j + j_modifier, i + i_modifier)
                                num_boxes = num_boxes -1
                    if column == 'e':
                        
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        #Enemy(self.game, j + j_modifier, i + i_modifier )
                    if column == '#':
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        BombBoss(self.game, j + j_modifier, i + i_modifier )
                    if column == ',':
                        Ground(self.game, j + j_modifier, i + i_modifier )
                    if column == 'c':
                        Prop(self.game, os.path.join(
                            dirname, '../images/coins.png'), j + j_modifier, i + i_modifier , 'coin')
                        Ground(self.game, j + j_modifier, i + i_modifier )
                    if column == '$':
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        Pedestal(self.game, os.path.join(
                            dirname, '../images/pedestal.png'), j + j_modifier, i + i_modifier + 1)
                        
                        shop_gen = random.choices(
                                    population=["AD+", "P+", "S+"],
                                    weights=[32,35,33],
                                    k=1
                                )
                        Purchasable(self.game, j + j_modifier, i + i_modifier, shop_gen[0])
                    if column == "P":
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        #Player(self, j, i)
                    if column =="■":
                        Ground(self.game, j + j_modifier, i + i_modifier)
                        Box(self.game, os.path.join(dirname, '../images/box.png'), j + j_modifier, i + i_modifier)
                    if column == "^":
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j + j_modifier, i + i_modifier , 'up')
                        #Player(self, j, i)
                    if column == "v":
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j + j_modifier, i + i_modifier ,"down")
                        #Player(self, j, i)
                    if column == "<":
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j + j_modifier, i + i_modifier ,"left")
                        #Player(self, j, i)
                    if column == ">":
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j + j_modifier, i + i_modifier ,"right")
                        #Player(self, j, i)
                    if column == "?":
                        Ground(self.game, j + j_modifier, i + i_modifier )

        
    def check_collide_tiles(self, rows, cols):
        #print("##############################")
        #print(self.game.wall_list)
        self.rows = rows
        self.cols = cols
        #print(self.rect.y)
        crash = False
        #print(self.new_start_y)
        if self.type == "left":
            #print(self.game.wall_list)

            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    x_crash = self.rect.x-16-self.game.SPEED -(self.c * 16)               
                    y_crash = self.rect.y +((self.r-self.new_start_y)*16)
                    if crash:
                        break
                    #print((y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-self.game.SPEED)%16 == 0:
                                temp_modifier = self.game.SPEED
                            else:
                                temp_modifier = -self.game.SPEED
                        if wall == (x_crash+ temp_modifier, y_crash ) :
                            self.room = plugL
                            
                            
                            crash = True
                            break
        if self.type == "right":
            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    x_crash = self.rect.x+16 +self.game.SPEED+(self.c * 16)               
                    y_crash = self.rect.y +((self.r-self.new_start_y)*16)
                    if crash:
                        break
                    #print((y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-self.game.SPEED)%16 == 0:
                                temp_modifier = self.game.SPEED
                            else:
                                temp_modifier = -self.game.SPEED
                                
                        if wall == (x_crash+ temp_modifier, y_crash ) :
                            self.room = plugR
                            
                            crash = True
                            break
        if self.type == "up":
            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    
                    
                    y_crash = self.rect.y-16 -(self.r * 16)                 
                    x_crash = self.rect.x +((self.c-self.new_start_x)*16) 
                    if crash:
                        break
                    #print((x_crash,y_crash))
                    
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[1]-self.game.SPEED)%16 == 0:
                                temp_modifier = self.game.SPEED
                            else:
                                temp_modifier = -self.game.SPEED
                        if wall == (x_crash , y_crash+ temp_modifier) :
                            self.room = plugU
                            
                            
                            crash = True
                            break
                        
        if self.type == "down":

                for self.r in range(self.rows):
                    if crash:
                        break
                    for self.c in range(self.cols):
                        
                        
                        y_crash = self.rect.y+16+self.game.SPEED +(self.r * 16)                 
                        x_crash = self.rect.x +((self.c-self.new_start_x)*16)
                        if crash:
                            break
                        #print((x_crash,y_crash))
                        for wall in self.game.wall_list:
                            if crash:
                                break
                            
                            temp_modifier = 0
                            if wall[1]%16 != 0:
                                if (wall[1]-self.game.SPEED)%16 == 0:
                                    temp_modifier = self.game.SPEED
                                else:
                                    temp_modifier = -self.game.SPEED
                            if wall == (x_crash, y_crash + temp_modifier) :
                                self.room = plugD
                                
                                crash = True
                                break

                