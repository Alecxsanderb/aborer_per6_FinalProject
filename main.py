# file created by: Alec Borer

# import libs
import pygame
import random
import os
# import settings 
from settings import *
from sprites import *
# from pygame.sprite import Sprite

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
    x,y = pygame.mouse.get_pos()
    return (x,y)


# init pygame and create window
pygame.init()
# init sound mixer
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game...")
clock = pygame.time.Clock() 

# creates groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
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
for i in range(0, 1000):
    m = Mob(randint(30,90), randint(30,90), [randint(0,255), randint(0,255), randint(0,255)])
    enemies.add(m)
    all_sprites.add(m)

# game loop

while RUNNING:
    #  keep loop running at the right speed
    clock.tick(FPS)
    ### process input events section of game loop
    for event in pygame.event.get():
        # check for window closing
        if event.type == pygame.QUIT:
            RUNNING = False
            # break
    # print(get_mouse_now())
    ### update section of game loop (if updates take longer the 1/30th of a second, you will get laaaaag...)
    enemies.update()
    all_sprites.update()

    # if player his enemies do something
    blocks_hit_list = pygame.sprite.spritecollide(player, enemies, True)
    
    for block in blocks_hit_list:
        SCORE += 1
        print(SCORE)
        pass
    
    # draw and render section of game loop
    screen.fill(TEAL)
    enemies.draw(screen)
    all_sprites.draw(screen)
    draw_text("Score: " + str(SCORE), 75, WHITE, WIDTH/2, HEIGHT - 100)
    # double buffering draws frames for entire screen
    pygame.display.flip()
    # pygame.display.update() -> only updates a portion of the screen
# ends program when loops evaluates to false
pygame.quit()