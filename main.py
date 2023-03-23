# file created by: Alec Borer

# import libs
import pygame as pg
import random
import os
# import settings 
from settings import *
from sprites import *
# from pg.sprite import Sprite

# create game class in order to pass properties to the sprites file

class Game:
    def __init__(self):
        # init game window et.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(WIDTH,HEIGHT)
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock
        self.running = True
    
    def new(self):
        # start new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(Player)
        for i in range(0, 10):
            m = Mob(20, 20, (0,255,0))
            self.all_sprites.add(m)
            self.enemies.add(m)
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
            if event.type == pg.QUIT():
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
    def update(self):
        pass
    def draw(self):
        pass

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

def get_mouse_now():
    x,y = pg.mouse.get_pos()
    return (x,y)


# init pg and create window
pg.init()
# init sound mixer
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My first game...")
clock = pg.time.Clock() 

# creates groups
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()
player = Player()

# adds the player to all_sprites so it can be more efficiently drawn and updated
all_sprites.add(player)

# enemy1 = Mob(80, 80)
# enemy2 = Mob(80, 80)
# enemy3 = Mob(80, 80)
# enemy4 = Mob(80, 80)

# all_sprites.add(enemy1)
# all_sprites.add(enemy2)
# all_sprites.add(enemy3)
# all_sprites.add(enemy4)
# all_sprites.add(testSprite)

# creates a for loop that creates 20 mobs
# randomizes size and color of said mobs and adds them to enemies and all_sprites groups
# for i in range(0, 25):
#     m = Mob(randint(30,90), randint(30,90), [randint(0,255), randint(0,255), randint(0,255)], 1)
#     enemies.add(m)
#     all_sprites.add(m)

# game loop

while RUNNING:
    #  keep loop running at the right speed
    clock.tick(FPS)
    ### process input events section of game loop
    for event in pg.event.get():
        # check for window closing
        if event.type == pg.QUIT:
            RUNNING = False
            # break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and not PAUSED:
                PAUSED = True
                print(PAUSED)
            elif event.key == pg.K_ESCAPE and PAUSED:
                PAUSED = False
            if event.key == pg.K_SPACE and not PAUSED:
                for i in range(0, 250):
                    m = Mob(randint(30,90), randint(30,90), [randint(0,255), randint(0,255), randint(0,255)])
                    enemies.add(m)
                    # all_sprites.add(m)
            if event.key == pg.K_f and not FREEZE:
                FREEZE = True
                print(FREEZE)
            elif event.key == pg.K_f and FREEZE:
                FREEZE = False
                print(FREEZE)

    # print(get_mouse_now())
    ### update section of game loop (if updates take longer the 1/30th of a second, you will get laaaaag...)

    # if player his enemies do something
    blocks_hit_list = pg.sprite.spritecollide(player, enemies, True)
    
    for block in blocks_hit_list:
        SCORE += 1
        # print(SCORE)
        pass
    
    # draw and render section of game loop
    if not PAUSED and not FREEZE:
        enemies.update()
        all_sprites.update()
        screen.fill(TEAL)
        enemies.draw(screen)
        all_sprites.draw(screen)
        draw_text("Score: " + str(SCORE), 75, WHITE, WIDTH/2, HEIGHT - 100)
    if not PAUSED and FREEZE:
        all_sprites.update()
        screen.fill(TEAL)
        enemies.draw(screen)
        all_sprites.draw(screen)
        draw_text("Score: " + str(SCORE), 75, WHITE, WIDTH/2, HEIGHT - 100)
    elif PAUSED:
        screen.fill(BLACK)
        draw_text("Paused", 100, WHITE, WIDTH/2, HEIGHT/2 - 50)
        draw_text("Press escape to resume", 20, WHITE, WIDTH/2 , HEIGHT/2 + 100)
    # double buffering draws frames for entire screen
    pg.display.flip()
    # pg.display.update() -> only updates a portion of the screen
# ends program when loops evaluates to false
pg.quit()