# file created by: Alec Borer

'''
sources:
used some of Domineco's code for the timers

'''

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
        self.image = pg.Surface((15,15))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False 
        self.living = True
        self.hit = False

        # variables for getting grabbed and escaping
        self.grabbedstate = True
        self.grabvalue = 10
        self.escaped = False
        self.increasegrabvalue = 0

        # timer for player escaping
        self.timesincegrabbed = 0
        self.grabtimecounter = pg.USEREVENT+1
        pg.time.set_timer(self.grabtimecounter, 1000)

        # timer for player escaping
        self.punchlife = 0
        self.punchcounter = pg.USEREVENT+1
        pg.time.set_timer(self.punchcounter, 1000)

    # inputs for players, is capable of distinguishing between two players 
    def input(self):
        # player 1 controls
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = +PLAYER_ACC
        if keystate[pg.K_w]:
            self.jump()

    # jump method 
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    
    # method to keep it on screen, or end the game if the player falls off
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
    
    def check_for_grab(self):
        mhits = pg.sprite.spritecollide(self, self.game.enemies, False)
        if mhits:
        #    print("got grabbed")
           self.grabbedstate = False

    def punch(self):
        self.hit = True
        self.attk = Projectile(self, 60, 15, self.pos.x, self.pos.y, 0, 0, WHITE)
        self.game.all_sprites.add(self.attk)
        self.game.playerpunch.add(self.attk)
 
    # update and physics
    def update(self):
        if self.punchlife >= 5:
            self.hit = False
            self.punchlife = 0
            self.attk.pos = (100000, 100000)
            print("dead")
        if self.grabvalue <= 0:
            self.escaped = True
            self.grabbedstate = True
            self.pos = vec(self.pos.x , self.pos.y)
            # print("escaped")
        if self.escaped:
            self.inbounds()
            self.acc = vec(0, PLAYER_GRAV)
            self.acc.x = self.vel.x * PLAYER_FRICTION
            self.input()
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.midbottom = self.pos
            # print(str(self.timesincegrabbed))
            if self.timesincegrabbed >= 1:
                self.escaped = False
                self.timesincegrabbed = 0
                self.increasegrabvalue += 1
                self.grabvalue = 10
                self.grabvalue += self.increasegrabvalue
        if not self.escaped:
            self.check_for_grab()
            if self.grabbedstate:
                # print("not grabbed")
                # print(str(self.grabvalue))
                self.inbounds()
                self.acc = vec(0, PLAYER_GRAV)
                self.acc.x = self.vel.x * PLAYER_FRICTION
                self.input()
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc
                self.rect.midbottom = self.pos
            if not self.grabbedstate and not self.escaped:
                # print("grabbed")
                self.inbounds()
                self.pos = self.game.enemy.pos
                self.rect.midbottom = self.pos
            


# mob class
class Mob(Sprite):
    def __init__(self, game, player, width, height, color):
        # properties of mob
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
        self.pos = vec(randint(200, 1100), randint(0, 600))
        self.vel = vec( 3*randint(-5,5)/randint(1,20), 3*randint(-5,5)/randint(1,20))
        self.acc = vec(0,0)
        self.cofric = 0.5
        self.canjump = True
        self.enemyspeed = .1

    # method to keep it on screen and get it back on the platform if it falls off
    def inbounds(self):
        if self.pos.x > WIDTH - 40:
            # print("I am off the right side of the screen")
            self.pos.x = WIDTH - 40
            self.vel.x *= -1
        if self.pos.x < 25:
            # print("I am off the right side of the screen")
            self.pos.x = 25
            self.vel.x *= -1
        if self.pos.y < 25:
            # print("I am off the right side of the screen")
            self.pos.y = 25
            self.vel.y *= -1
        if self.pos.y >= HEIGHT:
            self.pos = vec(randint(200, 1100), randint(0, 600))

    # how mob chases player
    def chase(self):
        # if the player is right of the mob, move right
        if self.player.pos.x > self.pos.x:
            self.vel.x += self.enemyspeed
        # if the player is to the left of the mob, move left
        if self.player.pos.x < self.pos.x:
            self.vel.x -= self.enemyspeed
        # randomly jump
        r = randint(0,60)
        if r == 1:
            self.jump()
        
    # jumps if in contact with ground
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -MOB_JUMP

    def kamikaze(self):
        if not self.player.grabbedstate and not self.player.escaped:
            if self.pos.x <= WIDTH/2:
                self.vel.x -= self.enemyspeed
            if self.pos.x >= WIDTH/2:
                self.vel.x += self.enemyspeed

    def upattack(self):
        self.attack = Projectile(self, 3, 30, self.pos.x, self.pos.y, 0, -15, RED)
        self.game.bullets.add(self.attack)
        self.game.all_sprites.add(self.attack)

    # mob behavior
    def behavior(self):
        # print(self.vel)
        self.inbounds()
        self.chase()
        self.kamikaze()
        if self.player.pos.y <= (self.pos.y - 40):
            n = randint(0, 60)
            if n == 1:
                self.upattack()
        self.pos += self.vel
        self.rect.center = self.pos

    # update and physics
    def update(self):
        self.behavior()
        self.acc = vec(0, MOB_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos



# platform class
class Platform(Sprite):
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

class Projectile(Sprite):
    def __init__(self, mob, width, height, x, y, movementx, movementy, color):
        Sprite.__init__(self)
        self.mob = mob
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.mob.pos.x, self.mob.pos.x)
        self.pos = vec(x, y)
        self.vel = vec( movementx, movementy)
        self.acc = vec(0,0)

    def update(self):
        self.acc = vec(0, 0)
        self.acc.x = self.vel.x
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.pos.y <= -50:
            # print("dead")
            self.kill()
        if self.pos.y >= HEIGHT + 50:
            # print("dead")
            self.kill()
        if self.pos.x <= -50:
            # print("dead")
            self.kill()
        if self.pos.x >= WIDTH + 50:
            # print("dead")
            self.kill()