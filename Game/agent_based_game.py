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
    def __init__(
        self, runtime=15, fps=60, target_reward=100, move_reward=1, miss_reward=-1, visualize=False
    ):
        # Initialize Pygame after __main__ is executed
        self.initialized = False
        self._initializeGame()  # Sets the 'initialized' bool variable to true/ enables pygame modules to work / gives display window the name "game"
        self.visualize = visualize  # Automatically sets 'visualize' bool variable to False at the beggining of the game
        self.gameover = False  # Automatically sets 'gameover' bool variable to False at the beggining of the game

        # Screen information
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.DISPLAY = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )  # Opens a window of size 800x600 labeled "game"
        self.clock = (
            pygame.time.Clock()
        )  # Initializes a pyGame clock object which is used to control the fps the game is run at
        self.FPS = fps  # fps is set to 60 off the bat (from parameter)

        # Setting up game variables
        self.score = 0
        self.TARGET_REWARD = target_reward  # set to 100 from parameters
        self.MOVE_DIRECTION_REWARD = move_reward  # set to 1 from parameters
        self.MISS_REWARD = miss_reward  # set to -1 from parameters
        self.PLAYER_DIMENTIONS = (80, 80)  # The size of the snake head
        self.TARGET_DIMENTIONS = (40, 40)  # Size of the targets
        self.TARGET_NUMBER = 3  # Number of targets on the screen at once
        self.SPEED = 5
        self.GAME_DURATION = (
            runtime  # How long one game is (15 seconds from parameters)
        )
        self.GAME_DURATION_IN_FRAMES = (
            runtime * fps
        )  # How long training will be = total number of frames and how fast your computer can run thru them
        self.remainingTime = self.GAME_DURATION
        self.remainingFrames = self.GAME_DURATION_IN_FRAMES

        # Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 60)
        self.font_small = pygame.font.SysFont("Verdana", 30)

        # Predefined some colors
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # Creating player
        self.player = self.Player(
            self.PLAYER_DIMENTIONS, self.RED
        )  # Creates an object of the player class, (jumps to player function to create it)
        self.player.moveTo(
            self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
        )  # starts the snake head at the middle of the screen by calling moveTo()

        # Creating Sprites Groups
        self.targets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Creating Targets
        self._initializeTargets()

    class Target(pygame.sprite.Sprite):
        def __init__(self, dimensions, color):
            super().__init__()
            self.width = dimensions[0]
            self.height = dimensions[1]
            self.rect = pygame.Rect(
                0, 0, self.width, self.height
            )  # Creates a blue rectangle stored in the 'rect' variable of size 40x40 (target)
            self.color = color  # sets color to blue

        # Draws each target to the screen
        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect)

        # Used to generate where each target will be placed once created
        def moveTo(self, x, y):
            self.rect.center = (x, y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, dimensions, color):
            super().__init__()
            self.rect = pygame.Rect(
                0, 0, dimensions[0], dimensions[1]
            )  # Creates a red rectangle stored in the 'rect' variable of size 80x80 (snake head)
            self.color = color  # sets color to RED

        # Draws snake head on screen
        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect)

        # Moves the center of the snake head to coordinated fed to this function
        def moveTo(self, x, y):
            self.rect.center = (
                x,
                y,
            )  # Only used at the beggining of the game to establish where the snake will spawn in

    def _movePlayer(self, delta_x, delta_y):
        # Checks if moving the snake to new coordinates would move it outside the game boundaries,
        # and adjusts the movement so the snake stays in bounds
        pRect = self.player.rect
        if (
            pRect.top + delta_y < 0
        ):  # checks if the snake sprite is moving beyond the top edge of the window
            delta_y = -pRect.top
        if (
            pRect.bottom + delta_y > self.SCREEN_HEIGHT
        ):  # checks if the snake sprite is moving beyond the bottom edge of the window
            delta_y = self.SCREEN_HEIGHT - pRect.bottom
        if (
            pRect.left + delta_x < 0
        ):  # checks if the snake sprite is moving beyond the left edge of the window
            delta_x = -pRect.left
        if (
            pRect.right + delta_x > self.SCREEN_WIDTH
        ):  # checks if the snake sprite is moving beyond the right edge of the window
            delta_x = self.SCREEN_WIDTH - pRect.right

        self.player.rect.move_ip(
            delta_x, delta_y
        )  # Moves the snake to new position bc it won't go outside the border

    def _initializeGame(self):
        if self.initialized:
            return
        self.initialized = True
        pygame.init()  # Initializes all pygame.modules/Otherwise pygame modules wouldn't work
        pygame.display.set_caption(
            "Game"
        )  # Initializes the NAME of the window where the game will be played

    # Calculate position of all targets
    def _initializeTargets(self):
        for i in range(
            self.TARGET_NUMBER
        ):  # calculates the location of where our targets will spawn in  (number of targets is set at the start of the game)
            newTarget = self.Target(
                self.TARGET_DIMENTIONS, self.BLUE
            )  # Makes an object of the target class and stores it in variable "new Target" and jumps to Target() to create our new target
            while True:
                newTarget.moveTo(
                                int(random.randint(newTarget.width // 2, self.SCREEN_WIDTH - newTarget.width // 2)), #Calculates X
                                int(random.randint(newTarget.height // 2, self.SCREEN_HEIGHT - newTarget.height // 2))
                                )  # calculates y of each new target being created and uses the moveTo() to move the target there                
                
                #check if newTarget is colliding with any other sprite
                collision = pygame.sprite.spritecollideany(
                    newTarget, self.all_sprites
                )  # Checks if the newly created target will spawn in on an existing target or snake head
                if (
                    not collision
                ):  # If it doesn't add it to the all_sprites group and target group
                    self.all_sprites.add(newTarget)
                    self.targets.add(newTarget)
                    break  # If collision does occur then generate another target that doesn't spawn in ontop of other sprites

    # Ends the game
    def exit(self):
        pygame.quit()

    # Resets the game after every run
    def reset(self, visualizeNext=False):
        self.gameover = False
        self.visualize = visualizeNext
        self.score = 0
        self.remainingFrames = self.GAME_DURATION_IN_FRAMES
        self.remainingTime = self.GAME_DURATION
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.targets.empty()
        self._initializeTargets()
        self.player.moveTo(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

    def _getDistanceToClosestTarget(self):
        # Calculates the closest target to the player
        closestTarget = None
        distanceToClosestTarget = 0
        for target in self.targets:
            if closestTarget == None:
                closestTarget = target  # If there isn't a closestTarget yet, picks the first target in the targets list to begin calculation to find the closest
                distanceToClosestTarget = math.sqrt(
                    (target.rect.center[0] - self.player.rect.center[0]) ** 2
                    + (target.rect.center[1] - self.player.rect.center[1]) ** 2
                )
            else:
                # Calculate euclidean distance between player and target
                distanceToNewTarget = math.sqrt(
                    (target.rect.center[0] - self.player.rect.center[0]) ** 2
                    + (target.rect.center[1] - self.player.rect.center[1]) ** 2
                )
                if distanceToNewTarget < distanceToClosestTarget:
                    closestTarget = target
                    distanceToClosestTarget = distanceToNewTarget
        if closestTarget == None:
            return float("inf")
        return distanceToClosestTarget

    # This function Runs after every move the snake makes
    # This function moves the snake according to what action is passed
    # This fucntion detects if collision occured if so add reward/calls for more targets to be generated
    # This function also rewards negetive points if no target was eatin during said action
    # This function also returns the state of the game (where the target is in relation to the snake)
    # This function also vizualises the game/checks if its game over
    def act(self, action: Action):
        if self.gameover:
            return (self.getState()[0], 0, True, self.score)
        for (
            event
        ) in (
            pygame.event.get()
        ):  # Looks through pyGame eventQueue and check if any of the events were 'quit' (clicking X to close window)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        reward = 0
        self.gameover = False

        distanceToTargetBefore = self._getDistanceToClosestTarget()

        # Move snake according to action
        if action == Action.UP:
            self._movePlayer(
                0, -self.SPEED
            )  # speed is set to 5 from initial game setup (speed = the number of pixels the snake head moves)
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

        distanceToTargetAfter = self._getDistanceToClosestTarget()
        # If player is closer to the target than in the previous frame, give reward
        if distanceToTargetAfter < distanceToTargetBefore:
            reward = self.MOVE_DIRECTION_REWARD
        else:
            reward = self.MISS_REWARD

        # To be run if collision occurs between Player and Target
        collision = pygame.sprite.spritecollideany(self.player, self.targets)
        if collision:
            self.score += 1  # If the snake moved and ate a target add 1 to the score
            reward += self.TARGET_REWARD
            collision.kill()
            newTarget = self.Target(self.TARGET_DIMENTIONS, self.BLUE)
            while True:
                newTarget.moveTo(
                                int(random.randint(newTarget.width // 2, self.SCREEN_WIDTH - newTarget.width // 2)),
                                int(random.randint(newTarget.height // 2, self.SCREEN_HEIGHT - newTarget.height // 2))
                            )
                # check if newTarget is colliding with any other sprite
                collision = pygame.sprite.spritecollideany(newTarget, self.all_sprites)
                if not collision:
                    self.all_sprites.add(newTarget)
                    self.targets.add(newTarget)
                    newTarget.draw(self.DISPLAY)
                    break

        # Runs after everytime the snake moves
        (
            newState,
            target,
        ) = (
            self.getState()
        )  # Returns state of the game (i.e. where the closest target is according to the snake) (ex. (1,-1) = closest target is to the bottom right)
        # returns closest target as well

        # Visualize the game if 'vizualization' variable = true, at the beginning parameters
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
                pygame.draw.line(
                    self.DISPLAY,
                    self.GREEN,
                    self.player.rect.center,
                    target.rect.center,
                    2,
                )
            # draw score
            scoreText = self.font_small.render(
                "Score: " + str(self.score), True, self.WHITE
            )
            self.DISPLAY.blit(scoreText, (10, 10))
            # Draws the timer
            timer = self.font_small.render(
                str(math.ceil(self.remainingTime)), True, self.WHITE
            )
            self.DISPLAY.blit(
                timer, (self.SCREEN_WIDTH / 2 - timer.get_rect().width / 2, 10)
            )
            # draw state
            stateText = self.font_small.render(
                "State: " + str(newState), True, self.WHITE
            )
            self.DISPLAY.blit(
                stateText, (self.SCREEN_WIDTH - stateText.get_rect().width, 10)
            )

            pygame.display.update()
            self.clock.tick(self.FPS)
            self.remainingTime -= 1 / self.FPS

            if self.remainingTime <= 0:
                self.gameover = True
        else:  ######comes here if the game is not being vizualized######
            self.remainingFrames -= 1
            if self.remainingFrames <= 0:
                self.gameover = True
        return (newState, reward, self.gameover, self.score)

    # State = (x, y), where
    # x is direction on horizontal axis
    # y is direction on vertical axis
    # x and y are integers in discrete range [-1, 1] where 1 is positive direction, 0 is neutral, -1 is negative direction.
    # For example if the closest target is to the bottom right of the player, the state of the game will be (1, -1)
    def getState(self):
        # Calculates the closest target to the player
        closestTarget = None
        distanceToClosestTarget = 0
        for target in self.targets:
            if closestTarget == None:
                closestTarget = target  # If there isn't a closestTarget yet, picks the first target in the targets list to begin calculation to find the closest
                distanceToClosestTarget = math.sqrt(
                    (target.rect.center[0] - self.player.rect.center[0]) ** 2
                    + (target.rect.center[1] - self.player.rect.center[1]) ** 2
                )
            else:
                # Calculate euclidean distance between player and target
                distanceToNewTarget = math.sqrt(
                    (target.rect.center[0] - self.player.rect.center[0]) ** 2
                    + (target.rect.center[1] - self.player.rect.center[1]) ** 2
                )
                if distanceToNewTarget < distanceToClosestTarget:
                    closestTarget = target
                    distanceToClosestTarget = distanceToNewTarget
        if closestTarget == None:
            return (0, 0), None

        # Calculate the state of the game in horizontal axis
        if self.player.rect.x < closestTarget.rect.x:
            x = 1
        elif self.player.rect.x > closestTarget.rect.x:
            x = -1
        else:
            x = 0

        # Calculate the state of the game in vertical axis
        if self.player.rect.y > closestTarget.rect.y:
            y = 1
        elif self.player.rect.y < closestTarget.rect.y:
            y = -1
        else:
            y = 0


        # if self.player.rect.right < closestTarget.rect.left:
        #     x = 1
        # elif self.player.rect.left > closestTarget.rect.right:
        #     x = -1
        # else:
        #     x = 0

        # # Calculate the state of the game in vertical axis
        # if self.player.rect.top > closestTarget.rect.bottom:
        #     y = 1
        # elif self.player.rect.bottom < closestTarget.rect.top:
        #     y = -1
        # else:
        #     y = 0

        return (x, y), closestTarget

    # Returns current game score
    def getScore(self):
        return self.score


######### When running the program will start here ##################
if __name__ == "__main__":
    game = (
        Game()
    )  # creating a game with default parameters/ creates snake head and targets and window to play game on
    # This part below will run after all the above has been completed
    gameover = False
    totalReward = 0

    # this is an example of the game you would use to train the agent
    # this game is not visualized, so it runs much faster
    # it can calculate frames at the maximum speed your machine can handle
    # it can play "15 second" game in 0.01 seconds, so you don't have to spend hours waiting for the agent to learn
    print("Non-visualized game")

    # sets the current time to 'startTime' variable in seconds
    startTime = time.time()
    ################################### THIS ACTS AS THE MAIN GAME LOOP ##########################################
    while not gameover:
        action = random.choice(
            list(Action)
        )  # makes the agent pick an action from the actions list (i.e. Up,Down,Left,Right......) and stores it in action variable

        state, reward, gameover, score = game.act(
            action
        )  # Then call game.act(action) to perform the action
        # game.act(action) returns a tuple (current state, reward, gameover, score)

        totalReward += (
            reward  # Then you can do whatever you want with the returned values
        )

        print(
            f"Action: {action}, State: {state}, Total Reward: {totalReward}, Score: {score}"
        )

    endTime = time.time()
    print(
        f"Time taken: {endTime - startTime}"
    )  # Pritns out how much time has taken since the beginning and end of the game

    ########### This part below Runs at the end of training, so the trainer (us) can see how well the agent has been trained ############################

    # this game is visualized, so it runs exactly as fast as a human would play it
    # so it would play "15 second" game in 15 seconds
    gameover = False
    game.reset(visualizeNext=True)
    print("\n\nVisualized game")

    while not gameover:
        action = Action.DOWN_RIGHT
        state, reward, gameover, score = game.act(action)
        totalReward += reward
        # print(f"Action: {action}, State: {state}, Total Reward: {totalReward}, Score: {score}")
