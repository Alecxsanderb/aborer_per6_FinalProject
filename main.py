# file created by: Alec Borer

'''
my goal is to create a mob that chases the player. it/they will grab the player and try to drag the player off the map. 
'''

# import libs
import pygame as pg
import os
import time
# import settings 
from settings import *
from sprites import *
# from pg.sprite import Sprite
# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
# create game class in order to pass properties to the sprites file
class Game:
    def __init__(self):
        # init game window et.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.running = True

        # timer stuff
        self.timeelapsed = 0
        self.survivecounter = pg.USEREVENT+1
        pg.time.set_timer(self.survivecounter, 1000)

    # start new game, create all sprites
    def new(self):
        # began creating main menu and option for two players, but did not get to finish
        self.menu = False
        self.end = False
        self.score = 0
        self.time = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.mc = pg.sprite.Group()
        self.ground = Platforms(WIDTH - 400, 30, 200, HEIGHT - 100, GREEN, "normal")
        self.player = Player(self, self.ground)
        self.enemy = Mob(self, self.player, 25, 25, RED)
        self.enemies.add(self.enemy)
        self.all_sprites.add(self.enemy)
        self.mc.add(self.player)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)
        # where the game runs
        self.run() 

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # does actions if buttons are pressed
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # this section resets the game if R is pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.player.living = False
                    self.player.grabvalue = 10
                    self.timeelapsed = 0
                    self.new()
                if event.key == pg.K_SPACE and not self.player.grabbedstate and not self.player.escaped:
                    self.player.grabvalue -= 1
            if self.player.living:
                if event.type == self.survivecounter:
                    self.timeelapsed += 1
            if self.player.escaped:
                if event.type == self.player.grabtimecounter:
                    self.player.timesincegrabbed += 1
    
    # updates game
    def update(self):
        # draws sprites
        self.all_sprites.update()
        # this section essentially makes platforms solid for the player, has stuff set up for variants but they aren't used
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if hits[0].variant == "normal":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                if hits[0].variant == "bouncy":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -20
        # this section gives the mob the ability to collide with platforms
        if self.enemy.vel.y > 0:
            landing = pg.sprite.spritecollide(self.enemy, self.platforms, False)
            if landing:
                if landing[0]:
                    self.enemy.pos.y = landing[0].rect.top
                    self.enemy.vel.y = 0
        # this section ends the game if the player falls off the screen
        if not self.player.living:
            self.end = True
        self.difficulty()

    # draws the different screens
    def draw(self):
        if self.menu and not self.end:
            self.main_screen()
        if not self.menu and not self.end:
            self.screen.fill(TEAL)
            self.all_sprites.draw(self.screen)
            self.timer()
        if not self.menu and self.end:
            self.timer()
            self.end_screen()
        pg.display.flip()
    
    # create text
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    
    # unused method to get mouse position
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)
    
    # how the timer is created
    def timer(self):
        # while the game is running
        if self.player.living:
            self.draw_text("Time: " + str(self.timeelapsed), 50, WHITE, WIDTH/2, 30)
        # after the game ends
        else:
            self.draw_text("Time: " + str(self.timeelapsed), 50, WHITE, WIDTH/2, HEIGHT/2)

    # main screen that I have not gotten working yet
    def main_screen(self):
        self.screen.fill(TEAL)
        self.draw_text("Menu", 150, WHITE, WIDTH/2, HEIGHT/2 - 150)
        self.draw_text("Press 1 for 1 player", 30, WHITE, WIDTH/2 - 200, HEIGHT/2 + 100)
        self.draw_text("Press 2 for 2 players", 30, WHITE, WIDTH/2 + 200, HEIGHT/2 + 100)

    # end screen
    def end_screen(self):
        if not self.player.living:
            self.screen.fill(BLACK)
            self.draw_text("Game Over", 200, WHITE, WIDTH/2, HEIGHT/2 - 250)
            self.timer()
            self.draw_text("Press R to restart", 50, WHITE, WIDTH/2, HEIGHT/2 + 150)

    # method that increases the speen of the enemy as time goes on
    def difficulty(self):
        if self.player.living:
            self.enemy.enemyspeed *= 1.001
        if not self.player.living:
            self.enemy.enemyspeed = 0

# instantiate the game class
g = Game()

# start game loop
while g.running:
    g.new()

pg.quit()