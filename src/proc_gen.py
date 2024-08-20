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
        
    def activate(self):
        if self.activated == 0:
            self.create_room()
        
    
        self.activated = 1
    
    def create_room(self):
        if self.type == "right":
            self.room = random.choice([roomR1, roomR2, roomR3])
        elif self.type == "down":
            self.room = random.choice([roomD1, roomD2, roomD3])
        elif self.type == "left":
            self.room = random.choice([roomL1, roomL2, roomL3])
        elif self.type == "up":
            self.room = random.choice([roomU1, roomU2, roomU3])
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
        
        for i, row in enumerate(self.room):
            for j, column in enumerate(row):
                if column == "?":
                    self.new_start_x = j
                    self.new_start_y = i
                    
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

