import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

#Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Setting up game variables
TARGET_DIMENTIONS = (40, 40)
TARGET_NUMBER = 1
SPEED = 5
SCORE = 0
TIME = 30

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 30)

#Create a black screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")


class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.width = TARGET_DIMENTIONS[0]
        self.height = TARGET_DIMENTIONS[1]
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

    def moveTo(self, x, y):
        self.rect.center = (x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.rect = pygame.Rect(0,0,80,80)
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    def update(self, surface):
        self.move()
        self.draw(surface)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)

        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)   

        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)  


def GetScore():
    return SCORE

player = Player()  #Creating object of player class

#Creating Sprites Groups
targets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Calculate position of all targets before drawing them on screen (make sure they won't spawn in colliding with eachother)
for i in range(TARGET_NUMBER):
    newTarget = Target() #object of Target() class
    while True:
        newTarget.moveTo(random.randint(newTarget.width/2, SCREEN_WIDTH - newTarget.width/2),  #x cordinate
                            random.randint(newTarget.height/2, SCREEN_HEIGHT - newTarget.height/2))   #y cordinate
        #check if newTarget is colliding with any other sprite already on the screen
        collision = pygame.sprite.spritecollideany(newTarget, all_sprites)
        if not collision:
            all_sprites.add(newTarget)
            targets.add(newTarget)
            break

#Game Loop
while TIME > 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #Draws the background
    DISPLAYSURF.fill(BLACK)

    #Draws the score
    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(scores, (10,10))

    #Draws the timer
    timer = font_small.render(str(int(TIME)), True, WHITE)
    DISPLAYSURF.blit(timer, (SCREEN_WIDTH//2 - 30, 10))

    #Moves and Re-draws all Sprites
    player.update(DISPLAYSURF)
    for entity in targets:
        entity.draw(DISPLAYSURF)

    #To be run if collision occurs between Player and Target
    collision = pygame.sprite.spritecollideany(player, targets)
    if collision:
        SCORE += 1
        collision.kill()
        newTarget = Target()
        while True:
            newTarget.moveTo(random.randint(newTarget.width/2, SCREEN_WIDTH - newTarget.width/2),
                                random.randint(newTarget.height/2, SCREEN_HEIGHT - newTarget.height/2))
            #check if newTarget is colliding with any other sprite
            collision = pygame.sprite.spritecollideany(newTarget, all_sprites)
            if not collision:
                all_sprites.add(newTarget)
                targets.add(newTarget)
                newTarget.draw(DISPLAYSURF)
                break

    pygame.display.update()
    FramePerSec.tick(FPS)
    TIME -= 1/60  #Reduce the timer by 1/60 second per frame

#Draw Game Over screen
DISPLAYSURF.fill(BLACK)
game_over = font.render("Game End", True, WHITE)
DISPLAYSURF.blit(game_over, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 30))
pygame.display.update()
time.sleep(5) #Time the game takes before closing itself 

pygame.quit()
sys.exit()