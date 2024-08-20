import pygame 
from pygame import mixer
from config import *
import math, random
import os
from tilemaps import *
from sprites import *
from props import *

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
        
        self.room = room0        
        
    def activate(self):
        if self.activated == 0:
            
            for wall in self.game.walls:
                wall.pseudoUpdate()
            self.create_room()
        
    
        self.activated = 1
    
    def create_room(self):
        if self.type == "right":
            self.room = random.choice([right_maps.a])
        elif self.type == "down":
            self.room = random.choice([down_maps.a, down_maps.b])
        elif self.type == "left":
            self.room = random.choice([left_maps.a])
        elif self.type == "up":
            self.room = random.choice([up_maps.a])
        self.new_start_x =-1
        self.new_start_y = -1
        
        self.createTiles()
    
    def update(self):
        
        if(pygame.sprite.spritecollide(self, self.game.player, False)):
            self.image = self.Door_spritesheet.get_sprite(32,0,self.width,self.height)
            if self.opened == 0:
                pygame.mixer.Sound.play(self.game.door_open)
            
            
            self.activate()
            self.opened = 1
        else:
            self.image = self.Door_spritesheet.get_sprite(0,0,self.width,self.height)
            self.opened = 0
        
                        
    def createTiles(self):
        self.rows = 0
        self.cols = 0
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
            
        self.tile_generate()
        
    def tile_generate(self):
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
                    if column == 'e':
                        Enemy(self.game, j + j_modifier, i + i_modifier )
                        Ground(self.game, j + j_modifier, i + i_modifier )
                    if column == 'c':
                        Prop(self.game, os.path.join(
                            dirname, '../images/coins.png'), j + j_modifier, i + i_modifier , 'chest')
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        
                    if column == "P":
                        Ground(self.game, j + j_modifier, i + i_modifier )
                        #Player(self, j, i)
                    if column =="■":
                        Ground(self, j + j_modifier, i + i_modifier)
                        Block(self, os.path.join(dirname, '../images/box.png'), j + j_modifier, i + i_modifier)
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
                    x_crash = self.rect.x-16-PLAYER_SPEED -(self.c * 16)               
                    y_crash = self.rect.y +((self.r-self.new_start_y)*16)
                    if crash:
                        break
                    #print((y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-PLAYER_SPEED)%16 == 0:
                                temp_modifier = PLAYER_SPEED
                            else:
                                temp_modifier = -PLAYER_SPEED
                        if wall == (x_crash, y_crash + temp_modifier) :
                            self.room = plugL
                            
                            
                            crash = True
                            break
        if self.type == "right":
            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    x_crash = self.rect.x+16 +PLAYER_SPEED +(self.c * 16)               
                    y_crash = self.rect.y +((self.r-self.new_start_y)*16)
                    if crash:
                        break
                    #print((y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-PLAYER_SPEED)%16 == 0:
                                temp_modifier = PLAYER_SPEED
                            else:
                                temp_modifier = -PLAYER_SPEED
                                
                        if wall == (x_crash, y_crash + temp_modifier) :
                            self.room = plugR
                            
                            crash = True
                            break
        if self.type == "up":
            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    
                    
                    y_crash = self.rect.y-16- PLAYER_SPEED -(self.r * 16)                 
                    x_crash = self.rect.x +((self.c-self.new_start_x)*16) 
                    if crash:
                        break
                    #print((x_crash,y_crash))
                    
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-PLAYER_SPEED)%16 == 0:
                                temp_modifier = PLAYER_SPEED
                            else:
                                temp_modifier = -PLAYER_SPEED
                        if wall == (x_crash + temp_modifier, y_crash) :
                            self.room = plugU
                            
                            
                            crash = True
                            break
                        
        if self.type == "down":

                for self.r in range(self.rows):
                    if crash:
                        break
                    for self.c in range(self.cols):
                        
                        
                        y_crash = self.rect.y+16+PLAYER_SPEED +(self.r * 16)                 
                        x_crash = self.rect.x +((self.c-self.new_start_x)*16)
                        if crash:
                            break
                        #print((x_crash,y_crash))
                        for wall in self.game.wall_list:
                            if crash:
                                break
                            
                            temp_modifier = 0
                            if wall[0]%16 != 0:
                                if (wall[0]-PLAYER_SPEED)%16 == 0:
                                    temp_modifier = PLAYER_SPEED
                                else:
                                    temp_modifier = -PLAYER_SPEED
                            if wall == (x_crash + temp_modifier, y_crash) :
                                self.room = plugD
                                
                                crash = True
                                break

                