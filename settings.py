# file created by: Alec Borer

from random import randint

WIDTH = 1300
HEIGHT = 800
PLAYER_ACC = .5
PLAYER_FRICTION = -.2
PLAYER_JUMP = 20
PLAYER_GRAV = .8
BLACK = (0,0,0)
TEAL = (50, 120, 255)
RED = (255, 25, 25) 
WHITE = (255, 255, 255)
GREEN = (50, 255, 120)
RANDCOLOR = [randint(0,255), randint(0,255), randint(0,255)]
SCORE = 0
FPS = 60
RUNNING = True
PAUSED = False
FREEZE = False
VARIANT = ("normal", "bouncy")
ALIVE = True
MOB_GRAV = .4
MOB_JUMP = 10