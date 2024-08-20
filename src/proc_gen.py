import pygame 
from pygame import mixer
from config import *
import math, random
import os
from tilemaps import *
from sprites import *
from props import *
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
        self.minorPlugged = False
        self.veryPlugged= False
        
        
        
    def activate(self):
        if self.activated == 0:
            self.create_room()
        
    
        self.activated = 1
    
    def create_room(self):
        if self.type == "right":
            self.room = random.choice([testR1])
        elif self.type == "down":
            self.room = random.choice([testD1])
        elif self.type == "left":
            self.room = random.choice([testL1])
        elif self.type == "up":
            self.room = random.choice([testU1])
        self.new_start_x =-1
        self.new_start_y = -1
        
        self.createTiles()
    
    def update(self):
        if(self.veryPlugged == True):
            self.image = self.game.Wall_spritesheet
            self.groups = self.game.all_sprites, self.game.blocks
        else:
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
        if self.minorPlugged:
            for i, row in enumerate(self.room):
                self.rows = self.rows +1
                for j, column in enumerate(row):
                    self.cols = j
                    if column == "?":
                        self.new_start_x = j
                        self.new_start_y = i
            
            self.check_collide_tiles(self.rows, self.cols)
        
        if self.veryPlugged == False:
            if self.type == "down":
                for i, row in enumerate(self.room):
                    for j, column in enumerate(row):
                        if column == "B":
                            Wall(self.game, os.path.join(dirname, '../images/bricks.png'), j+ (self.rect.x/16) - self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                        if column == 'b':
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            Block(self.game, os.path.join(dirname, '../images/Bed.png'), j, i+ (self.rect.y/16)+self.new_start_y+1)
                        if column == 'D':
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            Door(self.game, os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                        
                        if column == '.':
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                        if column == 'e':
                            Enemy(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                        if column == 'c':
                            Prop(self.game, os.path.join(
                                dirname, '../images/coins.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1, 'chest')
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            
                        if column == "P":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            #Player(self, j, i)
                        if column == "^":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1, 'up')
                            #Player(self, j, i)
                        if column == "v":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1,"down")
                            #Player(self, j, i)
                        if column == "<":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1,"left")
                            #Player(self, j, i)
                        if column == ">":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1,"right")
                            #Player(self, j, i)
                        if column == "?":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)+self.new_start_y+1)

            elif self.type == "right":
                for i, row in enumerate(self.room):
                    for j, column in enumerate(row):
                        if column == "B":
                            Wall(self.game, os.path.join(dirname, '../images/bricks.png'), j+ (self.rect.x/16) + self.new_start_x+1 , i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'b':
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            Block(self.game, os.path.join(dirname, '../images/Bed.png'), j, i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'D':
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            Door(self.game, os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                        
                        if column == '.':
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'e':
                            Enemy(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'c':
                            Prop(self.game, os.path.join(
                                dirname, '../images/coins.png'), j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y, 'chest')
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            
                        if column == "P":
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            #Player(self, j, i)
                        if column == "^":
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y, 'up')
                            #Player(self, j, i)
                        if column == "v":
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y,"down")
                            #Player(self, j, i)
                        if column == "<":
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y,"left")
                            #Player(self, j, i)
                        if column == ">":
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y,"right")
                            #Player(self, j, i)
                        if column == "?":
                            Ground(self.game, j+ (self.rect.x/16)+self.new_start_x+1, i+ (self.rect.y/16)-self.new_start_y)
            elif self.type == "left":
                for i, row in enumerate(self.room):
                    for j, column in enumerate(row):
                        if column == "B":
                            Wall(self.game, os.path.join(dirname, '../images/bricks.png'), j+ (self.rect.x/16) - self.new_start_x-1 , i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'b':
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            Block(self.game, os.path.join(dirname, '../images/Bed.png'), j, i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'D':
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            Door(self.game, os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                        
                        if column == '.':
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'e':
                            Enemy(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                        if column == 'c':
                            Prop(self.game, os.path.join(
                                dirname, '../images/coins.png'), j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y, 'chest')
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            
                        if column == "P":
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            #Player(self, j, i)
                        if column == "^":
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y, 'up')
                            #Player(self, j, i)
                        if column == "v":
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y,"down")
                            #Player(self, j, i)
                        if column == "<":
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y,"left")
                            #Player(self, j, i)
                        if column == ">":
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y,"right")
                            #Player(self, j, i)
                        if column == "?":
                            Ground(self.game, j+ (self.rect.x/16) - self.new_start_x-1, i+ (self.rect.y/16)-self.new_start_y)

            elif self.type == "up":
                for i, row in enumerate(self.room):
                    for j, column in enumerate(row):                                                                               
                        if column == "B":
                            Wall(self.game, os.path.join(dirname, '../images/bricks.png'), j+ (self.rect.x/16) - self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                        if column == 'b':
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            Block(self.game, os.path.join(dirname, '../images/Bed.png'), j, i+ (self.rect.y/16)-self.new_start_y )
                        if column == 'D':
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            Door(self.game, os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                        
                        if column == '.':
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                        if column == 'e':
                            Enemy(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                        if column == 'c':
                            Prop(self.game, os.path.join(
                                dirname, '../images/coins.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y , 'chest')
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            
                        if column == "P":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            #Player(self, j, i)
                        if column == "^":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y , 'up')
                            #Player(self, j, i)
                        if column == "v":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y ,"down")
                            #Player(self, j, i)
                        if column == "<":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y ,"left")
                            #Player(self, j, i)
                        if column == ">":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )
                            SpecDoor(self.game,os.path.join(dirname, '../images/Door.png'), j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y ,"right")
                            #Player(self, j, i)
                        if column == "?":
                            Ground(self.game, j+ (self.rect.x/16)-self.new_start_x, i+ (self.rect.y/16)-self.new_start_y )

            
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
                    x_crash = self.rect.x-18 -(self.c * 16)               
                    y_crash = self.rect.y +((self.r-self.new_start_y)*16)
                    if crash:
                        break
                    #print((y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-2)%16 == 0:
                                temp_modifier = 2
                            else:
                                temp_modifier = -2
                        if wall == (x_crash, y_crash + temp_modifier) :
                            self.room = plugL
                            if self.minorPlugged == True:
                                self.veryPlugged = True
                            self.minorPlugged = True
                            
                            crash = True
                            break
        if self.type == "right":
            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    x_crash = self.rect.x+18 +(self.c * 16)               
                    y_crash = self.rect.y +((self.r-self.new_start_y)*16)
                    if crash:
                        break
                    #print((y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-2)%16 == 0:
                                temp_modifier = 2
                            else:
                                temp_modifier = -2
                                
                        if wall == (x_crash, y_crash + temp_modifier) :
                            self.room = plugR
                            if self.minorPlugged == True:
                                self.veryPlugged = True
                            self.minorPlugged = True
                            crash = True
                            break
        if self.type == "up":
            
            for self.r in range(self.rows):
                if crash:
                    break
                for self.c in range(self.cols):
                    
                    
                    y_crash = self.rect.y-18 -(self.r * 16)                 
                    x_crash = self.rect.x +((self.c-self.new_start_x)*16)
                    if crash:
                        break
                    #print((x_crash,y_crash))
                    for wall in self.game.wall_list:
                        if crash:
                            break
                        
                        temp_modifier = 0
                        if wall[0]%16 != 0:
                            if (wall[0]-2)%16 == 0:
                                temp_modifier = 2
                            else:
                                temp_modifier = -2
                        if wall == (x_crash + temp_modifier, y_crash) :
                            self.room = plugU
                            if self.minorPlugged == True:
                                
                                self.veryPlugged = True
                            self.minorPlugged = True
                            
                            crash = True
                            break
                        
        if self.type == "down":

                for self.r in range(self.rows):
                    if crash:
                        break
                    for self.c in range(self.cols):
                        
                        
                        y_crash = self.rect.y+18 +(self.r * 16)                 
                        x_crash = self.rect.x +((self.c-self.new_start_x)*16)
                        if crash:
                            break
                        #print((x_crash,y_crash))
                        for wall in self.game.wall_list:
                            if crash:
                                break
                            
                            temp_modifier = 0
                            if wall[0]%16 != 0:
                                if (wall[0]-2)%16 == 0:
                                    temp_modifier = 2
                                else:
                                    temp_modifier = -2
                            if wall == (x_crash + temp_modifier, y_crash) :
                                self.room = plugD
                                if self.minorPlugged == True:
                                    self.veryPlugged = True
                                self.minorPlugged = True
                                crash = True
                                break

                