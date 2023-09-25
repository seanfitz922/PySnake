import pygame
import random
from enum import Enum
import numpy as np

# Constants
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 900
SNAKE_BLOCK_SIZE = 25
SNAKE_VELOCITY = 15
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Initialize pygame
pygame.init()

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Load the background image
background_image = pygame.image.load("checkered-background.jpg").convert()
background_image = pygame.transform.scale(background_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Fonts
font_style = pygame.font.SysFont("timesnewroman", 25)
score_font = pygame.font.SysFont("timesnewroman", 25)

# Idea for enum taken from https://github.com/patrickloeber/snake-ai-pytorch/blob/main/snake_game_human.py
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Helper class for the snake
class Snake:
    def __init__(self):
        # Set up display and clock
        self.clock = pygame.time.Clock()
        self.reset()  # Initialize with a reset

    def reset(self):
        self.x = DISPLAY_WIDTH / 2
        self.y = DISPLAY_HEIGHT / 2
        self.snake_head = [self.x, self.y]
        self.apple_x, self.apple_y = self.generate_apple_position()
        self.length = 1
        self.snake_list = []
        self.frame_iterations = 0
        self.current_score = 0
        self.direction = Direction.RIGHT
        
    def move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_direction = clock_wise[idx] # no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx] # right turn r -> d > -> l -> u
        else:
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx] # left turn r -> u > -> l -> d

        self.direction = new_direction
        
        if self.direction == Direction.RIGHT:
            self.x += SNAKE_BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            self.x -= SNAKE_BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            self.y += SNAKE_BLOCK_SIZE
        elif self.direction == Direction.UP:
            self.y -= SNAKE_BLOCK_SIZE

    def check_collision(self, point = None):
        if point is None:
            point = self.snake_head
        if (
            point[0] >= DISPLAY_WIDTH
            or point[0] < 0
            or point[1] >= DISPLAY_HEIGHT
            or point[1] < 0
        ):
            return True

        for segment in self.snake_list[:-1]:
            if segment == [self.x, self.y]:
                return True

        return False

    def draw(self):
        if len(self.snake_list) > self.length:
            del self.snake_list[0]
        for segment in self.snake_list:
            pygame.draw.rect(display, GREEN, [segment[0], segment[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

    def generate_apple_position(self):  
        x = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        y = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        return x, y

    def play_step(self, action):
        self.frame_iterations +=1

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.move(action)
            self.snake_head = [self.x, self.y]
            self.snake_list.append(self.snake_head)
            reward = 0

            game_over = False
            if self.check_collision():
                reward = -10
                game_over = True
                return reward, game_over, self.current_score

            display.blit(background_image, (0, 0))
            pygame.draw.rect(display, RED, [self.apple_x, self.apple_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

            if self.x == self.apple_x and self.y == self.apple_y:
                self.apple_x, self.apple_y = self.generate_apple_position()
                reward = 10
                self.length += 3
                self.current_score += 1

            self.draw()
            pygame.display.update()
            self.clock.tick(SNAKE_VELOCITY)

            return reward, game_over, self.current_score

