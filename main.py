# file created by: Alec Borer

'''
my goal is to create a mob that chases the player. game will be like tag and score will be based on time
'''

# import libs
import pygame as pg
import random
import os
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

    def new(self):
        # start new game
        self.score = 0
        self.time = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.mc = pg.sprite.Group()
        self.player = Player(self)
        self.ground = Platforms(WIDTH - 400, 30, 200, HEIGHT - 200, GREEN, "normal")
        self.enemy = Mob(self, self.player, 75, 75, RED)
        self.enemies.add(self.enemy)
        self.mc.add(self.player)
        self.all_sprites.add(self.enemy)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)
        self.run() 
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.player.living = False
    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if hits[0].variant == "normal":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                if hits[0].variant == "bouncy":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -20
        if self.enemy.vel.y > 0:
            landing = pg.sprite.spritecollide(self.enemy, self.platforms, False)
            

    def draw(self):
        self.screen.fill(TEAL)
        self.all_sprites.draw(self.screen)
        self.timer()
        self.draw_text("Score: " + str(self.score), 50, WHITE, WIDTH/2, 750)
        self.end_screen()
        pg.display.flip()
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)
    def timer(self):
        if self.player.living:
            self.time = pg.time.get_ticks()
            self.draw_text("Time: " + str(self.time/1000), 50, WHITE, WIDTH/2, 30)
        else:
            self.draw_text("Time: " + str(self.time/1000), 50, WHITE, WIDTH/2, 30)
    def end_screen(self):
        if not self.player.living:
            self.screen.fill(BLACK)
            self.draw_text("Game Over", 200, WHITE, WIDTH/2, HEIGHT/2 - 250)
            self.timer()
            self.draw_text("Press R to restart", 50, WHITE, WIDTH/2, HEIGHT/2 + 150)

# instantiate the game class
g = Game()

# start game loop
while g.running:
    g.new()

pg.quit()