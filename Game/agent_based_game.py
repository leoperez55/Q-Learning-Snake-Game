import pygame, sys
from pygame.locals import *
import random, time, math
from enum import Enum

class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8

class Game:
    def __init__(self, runtime=15, fps=60, target_reward=100, miss_reward=-1, visualize=False):
        # Initialize Pygame
        self.initialized = False
        self._initializeGame()
        self.visualize = visualize

        # Screen information
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = fps

        # Setting up game variables
        self.score = 0
        self.TARGET_REWARD = target_reward
        self.MISS_REWARD = miss_reward
        self.PLAYER_DIMENTIONS = (80, 80)
        self.TARGET_DIMENTIONS = (40, 40)
        self.TARGET_NUMBER = 3
        self.SPEED = 5
        self.GAME_DURATION = runtime
        self.GAME_DURATION_IN_FRAMES = runtime * fps
        self.remainingTime = self.GAME_DURATION
        self.remainingFrames = self.GAME_DURATION_IN_FRAMES

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


    def _movePlayer(self, delta_x, delta_y):
        # transform raw movment to legal movment that's bound by the screen
        pRect = self.player.rect
        if pRect.top + delta_y < 0:
            delta_y = -pRect.top
            print(f"top: {pRect.top}")
            print(f"bottom: {pRect.bottom}")
            print(f"center: {pRect.center}")
        if pRect.bottom + delta_y > self.SCREEN_HEIGHT:
            delta_y = self.SCREEN_HEIGHT - pRect.bottom
        if pRect.left + delta_x < 0:
            delta_x = -pRect.left
        if pRect.right + delta_x > self.SCREEN_WIDTH:
            delta_x = self.SCREEN_WIDTH - pRect.right

        self.player.rect.move_ip(delta_x, delta_y)



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

    def exit(self):
        pygame.quit()
    
    def reset(self, visualizeNext=False):
        self.visualize = visualizeNext
        self.score = 0
        self.remainingFrames = self.GAME_DURATION_IN_FRAMES
        self.remainingTime = self.GAME_DURATION
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.targets.empty()
        self._initializeTargets()
        self.player.moveTo(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2)

    
    def act(self, action: Action):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        reward = 0
        gameover = False
        #Move player according to action
        if action == Action.UP:
            self._movePlayer(0, -self.SPEED)
        elif action == Action.DOWN:
            self._movePlayer(0, self.SPEED)
        elif action == Action.LEFT:
            self._movePlayer(-self.SPEED, 0)
        elif action == Action.RIGHT:
            self._movePlayer(self.SPEED, 0)
        elif action == Action.UP_LEFT:
            self._movePlayer(-self.SPEED, -self.SPEED)
        elif action == Action.UP_RIGHT:
            self._movePlayer(self.SPEED, -self.SPEED)
        elif action == Action.DOWN_LEFT:
            self._movePlayer(-self.SPEED, self.SPEED)
        elif action == Action.DOWN_RIGHT:
            self._movePlayer(self.SPEED, self.SPEED)

        #To be run if collision occurs between Player and Target
        collision = pygame.sprite.spritecollideany(self.player, self.targets)
        if collision:
            self.score += 1
            reward = self.TARGET_REWARD # Reward for hitting a target
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
        else:
            reward = self.MISS_REWARD # Reward for NOT hitting a target

        newState, target = self.getState()

        # Visualize if requested
        if self.visualize:
            # draw background
            self.DISPLAY.fill(self.BLACK)
            # draw targets
            for sprite in self.targets:
                sprite.draw(self.DISPLAY)
            # draw player
            self.player.draw(self.DISPLAY)
            # draw a line from player to current target
            if target:
                pygame.draw.line(self.DISPLAY, self.GREEN, self.player.rect.center, target.rect.center, 2)
            # draw score
            scoreText = self.font_small.render("Score: " + str(self.score), True, self.WHITE)
            self.DISPLAY.blit(scoreText, (10, 10))
            #Draws the timer
            timer = self.font_small.render(str(math.ceil(self.remainingTime)), True, self.WHITE)
            self.DISPLAY.blit(timer, (self.SCREEN_WIDTH/2 - timer.get_rect().width/2, 10))
            # draw state
            stateText = self.font_small.render("State: " + str(newState), True, self.WHITE)
            self.DISPLAY.blit(stateText, (self.SCREEN_WIDTH - stateText.get_rect().width, 10))

            pygame.display.update()
            self.clock.tick(self.FPS)
            self.remainingTime -= 1/self.FPS

            if self.remainingTime <= 0:
                gameover = True
                self.reset()
        else:
            self.remainingFrames -= 1
            if self.remainingFrames <= 0:
                gameover = True
                self.reset()
        return (newState, reward, gameover, self.score)

        # State = (x, y), where
        # x is direction on horizontal axis
        # y is direction on vertical axis
        # x and y are integers in discrete range [-1, 1] where 1 is positive direction, 0 is neutral, -1 is negative direction.
        # For example if the closest target is to the bottom right of the player, the state of the game will be (1, -1)
    def getState(self):
        # Get the closest target to the player
        closestTarget = None
        distanceToClosestTarget = 0
        for target in self.targets:
            if closestTarget == None:
                closestTarget = target
                distanceToClosestTarget = math.sqrt((target.rect.center[0] - self.player.rect.center[0])**2 + (target.rect.center[1] - self.player.rect.center[1])**2)
            else:
                # Calculate euclidean distance between player and target
                distanceToNewTarget = math.sqrt((target.rect.center[0] - self.player.rect.center[0])**2 + (target.rect.center[1] - self.player.rect.center[1])**2)
                if distanceToNewTarget < distanceToClosestTarget:
                    closestTarget = target
                    distanceToClosestTarget = distanceToNewTarget
        if closestTarget == None:
            return (0, 0), None
        
        # Calculate the state of the game in horizontal axis
        if self.player.rect.right < closestTarget.rect.left:
            x = 1
        elif self.player.rect.left > closestTarget.rect.right:
            x = -1
        else:
            x = 0
        
        # Calculate the state of the game in vertical axis
        if self.player.rect.top > closestTarget.rect.bottom:
            y = 1
        elif self.player.rect.bottom < closestTarget.rect.top:
            y = -1
        else:
            y = 0

        return (x, y), closestTarget

    def getScore(self):
        return self.score


if __name__ == "__main__":
    import random
    import time

    # State space
    state_space = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))

    # Action space
    action_space = list(Action)

    # Initialize the Q-table with all zeros
    Q = {}
    for state in state_space:
        for action in action_space:
            Q[(state, action)] = 0

    # Q-learning hyperparameters
    alpha = 0.4
    gamma = 0.99
    epsilon_start = 1.0
    epsilon_end = 0.01
    epsilon_decay = 0.995
    episodes = 100

    game = Game(visualize=False)

    # Training loop
    epsilon = epsilon_start
    for episode in range(episodes):
        game.reset()
        gameover = False

        while not gameover:
            state, _ = game.getState()

            # Epsilon-greedy action selection
            if random.uniform(0, 1) < epsilon:
                action = random.choice(action_space)
            else:
                action = max(action_space, key=lambda a: Q[(state, a)])

            # Perform the action and receive the new state, reward, and gameover status
            _, reward, gameover, _ = game.act(action)
            next_state, _ = game.getState()

            # Update the Q-value for the current state-action pair using the Q-learning update rule
            old_q_value = Q[(state, action)]
            next_q_value = max([Q[(next_state, a)] for a in action_space])
            Q[(state, action)] = old_q_value + alpha * (reward + gamma * next_q_value - old_q_value)

        # Decay epsilon to balance exploration and exploitation
        epsilon = max(epsilon_end, epsilon * epsilon_decay)

    # Test the trained agent
    game.reset(visualizeNext=True)
    gameover = False
    total_reward = 0

    while not gameover:
        state, _ = game.getState()
        state_action = state

        action = max(Action, key=lambda a: Q.get(state_action + (a,), 0))

        _, reward, gameover, _ = game.act(action)
        total_reward += reward

    print(f"Total Reward (Test): {total_reward}")