# file created by: Alec Borer

import pygame as pg

from pygame.sprite import Sprite

from settings import *

vec = pg.math.Vector2

# player class


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
    def input(self):
        keystate = pg.key.get_pressed()

        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keystate[pg.K_s]:
            self.acc.y = +PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = +PLAYER_ACC
        if keystate[pg.K_SPACE]:
            self.pos = WIDTH/2, HEIGHT/2

    # method to keep it on screen
    def inbounds(self):
        if self.pos.x > WIDTH - 25:
            # print("I am off the right side of the screen")
            self.pos.x = WIDTH - 25
            self.vel.x = 0
        if self.pos.y > HEIGHT - 25:
            # print("I am off the right side of the screen")
            self.pos.y = HEIGHT - 25
            self.vel.y = 0
        if self.pos.x < 25:
            # print("I am off the right side of the screen")
            self.pos.x = 25
            self.vel.x = 0
        if self.pos.y < 25:
            # print("I am off the right side of the screen")
            self.pos.y = 25
            self.vel.y = 0

    def update(self):
        self.inbounds()
        self.acc = self.vel * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

class Mob(Sprite):
    def __init__(self, width, height):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        
    
    # method to keep it on screen
    def inbounds(self):
        if self.pos.x > WIDTH - 40:
            # print("I am off the right side of the screen")
            self.pos.x = WIDTH - 40
            self.vel.x = 0
        if self.pos.y > HEIGHT - 40:
            # print("I am off the right side of the screen")
            self.pos.y = HEIGHT - 40
            self.vel.y = 0
        if self.pos.x < 25:
            # print("I am off the right side of the screen")
            self.pos.x = 25
            self.vel.x = 0
        if self.pos.y < 25:
            # print("I am off the right side of the screen")
            self.pos.y = 25
            self.vel.y = 0

    def behavior(self):
        # print(self.vel)
        self.acc.y = MOB_ACC

    def update(self):
        self.inbounds()
        self.acc = self.vel * MOB_FRICTION
        self.behavior()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

