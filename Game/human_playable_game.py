import pygame, sys
from pygame.locals import *
import random, time, math

class Game:
    def __init__(self):
        # Initialize Pygame
        self.initialized = False
        self._initializeGame()

        # Screen information
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.GAME_OVER_SCREEN_DURATION = 3

        # Setting up game variables
        self.game_over = False
        self.score = 0
        self.PLAYER_DIMENTIONS = (80, 80)
        self.TARGET_DIMENTIONS = (40, 40)
        self.TARGET_NUMBER = 3
        self.SPEED = 5
        self.GAME_DURATION = 10

        #Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 60)
        self.font_small = pygame.font.SysFont("Verdana", 30)

        # Predefined some colors
        self.BLUE  = (0, 0, 255)
        self.RED   = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Creating player
        self.player = self.Player(self.PLAYER_DIMENTIONS, self.RED)
        self.player.moveTo(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2)

        #Creating Sprites Groups
        self.targets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        #Initializing Targets
        self._initializeTargets()


    class Target(pygame.sprite.Sprite):
        def __init__(self, dimensions, color):
            super().__init__() 
            self.width = dimensions[0]
            self.height = dimensions[1]
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.color = color

        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect)

        def moveTo(self, x, y):
            self.rect.center = (x, y)


    class Player(pygame.sprite.Sprite):
        def __init__(self, dimensions, color):
            super().__init__() 
            self.rect = pygame.Rect(0,0,dimensions[0],dimensions[1])
            self.color = color

        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect)  
        
        def moveTo(self, x, y):
            self.rect.center = (x, y)


    def _movePlayer(self):
        pressed_keys = pygame.key.get_pressed()

        if self.player.rect.top > 0:
            if pressed_keys[K_UP]:
                self.player.rect.move_ip(0, -5)

        if self.player.rect.bottom < self.SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.player.rect.move_ip(0,5)

        if self.player.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.player.rect.move_ip(-5, 0)

        if self.player.rect.right < self.SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.player.rect.move_ip(5, 0)

    def _initializeGame(self):
        if self.initialized:
            return
        self.initialized = True
        pygame.init()
        pygame.display.set_caption("Game")


    def _initializeTargets(self):
        # Calculate position of all targets
        for i in range(self.TARGET_NUMBER):
            newTarget = self.Target(self.TARGET_DIMENTIONS, self.BLUE)
            while True:
                newTarget.moveTo(random.randint(newTarget.width/2, self.SCREEN_WIDTH - newTarget.width/2),
                                    random.randint(newTarget.height/2, self.SCREEN_HEIGHT - newTarget.height/2))
                #check if newTarget is colliding with any other sprite
                collision = pygame.sprite.spritecollideany(newTarget, self.all_sprites)
                if not collision:
                    self.all_sprites.add(newTarget)
                    self.targets.add(newTarget)
                    break

    def _gameOver(self):
        self.game_over = True
        self.DISPLAY.fill(self.BLACK)
        text = self.font.render("Game Over", True, self.WHITE)
        text_rect = text.get_rect()
        text_x = self.DISPLAY.get_width() / 2 - text_rect.width / 2
        text_y = self.DISPLAY.get_height() / 2 - text_rect.height / 2
        self.DISPLAY.blit(text, [text_x, text_y])
        pygame.display.flip()

        timeToClose = self.GAME_OVER_SCREEN_DURATION
        while timeToClose > 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.reset()
                        self.play()
                        return
            self.clock.tick(self.FPS)
            timeToClose -= 1/self.FPS
        
        pygame.quit()
        sys.exit()
    
    def reset(self):
        self.score = 0
        self.game_over = False
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.targets.empty()
        self._initializeTargets()
        self.player.moveTo(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2)

    def play(self):
        # Initialize Pygame if not initialized
        if not self.initialized:
            self._initializeGame()

        # Game Loop
        playTime = self.GAME_DURATION
        while playTime > 0:     
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.reset()
                        playTime = self.GAME_DURATION

            #Draws the background
            self.DISPLAY.fill(self.BLACK)

            #Moves and Re-draws all Sprites
            self._movePlayer()
            self.player.draw(self.DISPLAY)
            for entity in self.targets:
                entity.draw(self.DISPLAY)

            #To be run if collision occurs between Player and Target
            collision = pygame.sprite.spritecollideany(self.player, self.targets)
            if collision:
                self.score += 1
                collision.kill()
                newTarget = self.Target(self.TARGET_DIMENTIONS, self.BLUE)
                while True:
                    newTarget.moveTo(random.randint(newTarget.width/2, self.SCREEN_WIDTH - newTarget.width/2),
                                        random.randint(newTarget.height/2, self.SCREEN_HEIGHT - newTarget.height/2))
                    #check if newTarget is colliding with any other sprite
                    collision = pygame.sprite.spritecollideany(newTarget, self.all_sprites)
                    if not collision:
                        self.all_sprites.add(newTarget)
                        self.targets.add(newTarget)
                        newTarget.draw(self.DISPLAY)
                        break

            #Draws the score
            scoreText = self.font.render("Score: " + str(self.score), True, self.WHITE)
            self.DISPLAY.blit(scoreText, (10,10))

            #Draws the timer
            timer = self.font_small.render(str(math.ceil(playTime)), True, self.WHITE)
            self.DISPLAY.blit(timer, (self.SCREEN_WIDTH/2 - timer.get_rect().width/2, 10))

            pygame.display.update()
            self.clock.tick(self.FPS)
            playTime -= 1/self.FPS  #Reduce the timer by 1/60 second per frame
        self.game_over = True
        self._gameOver()


    def GetScore(self):
        return self.score


if __name__ == "__main__":
    game = Game()
    game.play()
    print(game.GetScore())

