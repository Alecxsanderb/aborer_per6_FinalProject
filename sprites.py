# file created by: Alec Borer
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint

vec = pg.math.Vector2

# player class


class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # properties of Player
        self.game = game
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False 
        self.living = True
    def input(self):
        keystate = pg.key.get_pressed()
        # if keystate[pg.K_s]:
        #     self.acc.y = +PLAYER_ACC
        # if keystate[pg.K_w]:
        #     self.acc.y = -PLAYER_ACC
        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = +PLAYER_ACC
        if keystate[pg.K_SPACE]:
            self.jump()
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    # method to keep it on screen
    def inbounds(self):
        if self.pos.x > WIDTH - 25:
            # print("I am off the right side of the screen")
            self.pos.x = WIDTH - 25
            self.vel.x *= 0
        if self.pos.y > HEIGHT - 25:
            # print("I am off the right side of the screen")
            self.living = False
        if self.pos.x < 25:
            # print("I am off the right side of the screen")
            self.pos.x = 25
            self.vel.x *= 0
        if self.pos.y < 25:
            # print("I am off the right side of the screen")
            self.pos.y = 25
            self.vel.y *= 0
    def mob_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.vel.x *= -1.5
            self.vel.y += self.vel.x/2

    def update(self):
        self.mob_collide()
        self.inbounds()
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Mob(Sprite):
    def __init__(self, game, player, width, height, color):
        Sprite.__init__(self)
        self.player = player
        self.game = game
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.pos = vec(randint(200, 1100), randint(0, 800))
        self.vel = vec( 3*randint(-5,5)/randint(1,20), 3*randint(-5,5)/randint(1,20))
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = True
        self.enemyspeed = .1
    # method to keep it on screen
    def inbounds(self):
        if self.pos.x > WIDTH - 40:
            # print("I am off the right side of the screen")
            self.pos.x = WIDTH - 40
            self.vel.x *= -1
        if self.pos.y > HEIGHT - 40:
            # print("I am off the right side of the screen")
            self.pos.y = HEIGHT/2
            self.vel.y = 0
        if self.pos.x < 25:
            # print("I am off the right side of the screen")
            self.pos.x = 25
            self.vel.x *= -1
        if self.pos.y < 25:
            # print("I am off the right side of the screen")
            self.pos.y = 25
            self.vel.y *= -1

    def player_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.mc, False)
        if hits:
            self.vel.x += self.player.vel.x/3
            self.vel.y += self.vel.x/2

    def chase(self):
        if self.player.pos.x > self.pos.x:
            self.vel.x += self.enemyspeed
        if self.player.pos.x < self.pos.x:
            self.vel.x -= self.enemyspeed
        if self.player.pos.y < self.pos.y:
                self.jump()
        
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -MOB_JUMP

    def behavior(self):
        # print(self.vel)
        self.inbounds()
        self.chase()
        self.player_collide()
        self.pos += self.vel
        self.rect.center = self.pos
    def update(self):
        self.behavior()
        self.acc = vec(0, MOB_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Platforms(Sprite):
    def __init__(self, width, height, x, y, color, variant):
        Sprite.__init__(self)
        # properties of Platforms
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.image.fill(self.color)
        self.variant = variant
        