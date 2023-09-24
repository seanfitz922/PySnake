import pygame
import random
from enum import Enum

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

# Set up display and clock
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

# Load the background image
background_image = pygame.image.load("checkered-background.jpg").convert()
background_image = pygame.transform.scale(background_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Fonts
font_style = pygame.font.SysFont("timesnewroman", 25)
score_font = pygame.font.SysFont("timesnewroman", 25)

# Helper function to display messages
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [DISPLAY_WIDTH / 4, DISPLAY_HEIGHT / 4])

# Function to display player's score
def player_score(score):
    value = score_font.render("Score: " + str(score), True, BLACK)
    display.blit(value, [0, 0])

# idea for enum taken from https://github.com/patrickloeber/snake-ai-pytorch/blob/main/snake_game_human.py
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Helper class for the snake
class Snake:
    def __init__(self):
        self.x = DISPLAY_WIDTH / 2
        self.y = DISPLAY_HEIGHT / 2
        self.x_change = 0
        self.y_change = 0
        self.length = 1
        self.snake_list = []
        self.direction = None
        self.frame_iteration = 0

    def change_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.direction = Direction.LEFT
            elif event.key == pygame.K_d:
                self.direction = Direction.RIGHT
            elif event.key == pygame.K_w:
                self.direction = Direction.UP
            elif event.key == pygame.K_s:
                self.direction = Direction.DOWN

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += SNAKE_BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            self.x -= SNAKE_BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            self.y += SNAKE_BLOCK_SIZE
        elif self.direction == Direction.UP:
            self.y -= SNAKE_BLOCK_SIZE

    # Inside the Snake class
    def check_collision(self):
        if (
            self.x >= DISPLAY_WIDTH
            or self.x < 0
            or self.y >= DISPLAY_HEIGHT
            or self.y < 0
        ):
            return True

        for segment in self.snake_list[:-1]:
            if segment == [self.x, self.y]:
                return True

        return False


    def draw(self):
        snake_head = [self.x, self.y]
        self.snake_list.append(snake_head)

        if len(self.snake_list) > self.length:
            del self.snake_list[0]

        for segment in self.snake_list:
            pygame.draw.rect(display, GREEN, [segment[0], segment[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

    # Helper function to generate apple's position
    def generate_apple_position(self):  
        apple_x = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        apple_y = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        return apple_x, apple_y

def handle_game_over():
    display_message("Game Over! Press W-Play Again or Q-Quit", RED)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_w:
                    game_loop(1)

def game_loop(initial_length_of_snake):
    snake = Snake()
    current_score = 0
    apple_x, apple_y = snake.generate_apple_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            snake.change_direction(event)

        snake.move()

        if snake.check_collision():
            handle_game_over()

        display.blit(background_image, (0, 0))
        pygame.draw.rect(display, RED, [apple_x, apple_y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        if snake.x == apple_x and snake.y == apple_y:
            apple_x, apple_y = snake.generate_apple_position()
            snake.length += 3
            current_score += 1

        snake.draw()
        player_score(current_score)
        pygame.display.update()
        clock.tick(SNAKE_VELOCITY)

# Start the game loop with an initial snake length of 1
game_loop(1)

