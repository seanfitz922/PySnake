import pygame
import random

# Initialize pygame
pygame.init()

# Set up display dimensions and other constants
display_width = 900
display_height = 900
snake_block_size = 25  # Increase the snake size
snake_velocity = 15

# Set up colors and fonts
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set up display and clock
display = pygame.display.set_mode((display_width, display_height))

# Load the background image
background_image = pygame.image.load("checkered-background.jpg").convert()

# Resize the background image to match the display dimensions
background_image = pygame.transform.scale(background_image, (display_width, display_height))

clock = pygame.time.Clock()

# Set up fonts
font_style = pygame.font.SysFont("timesnewroman", 25)
score_font = pygame.font.SysFont("timesnewroman", 25)

# Initialize global variables
x1, y1 = display_width / 2, display_height / 2
x1_change, y1_change = 0, 0

current_score = 0

# Function to display player's score
def player_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    display.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_block_size, snake_list):
    for i in snake_list:
        pygame.draw.rect(display, green, [i[0], i[1], snake_block_size, snake_block_size])  # Set snake color to green

# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 4, display_height / 4])

# Function to generate apple's position
def generate_apple_position():
    apple_x = round(random.randrange(0, display_width - snake_block_size) / snake_block_size) * snake_block_size
    apple_y = round(random.randrange(0, display_height - snake_block_size) / snake_block_size) * snake_block_size
    return apple_x, apple_y

# Function to handle apple collision
def handle_apple_collision(apple_x, apple_y, length_of_snake):
    global current_score  # Use the global current_score variable

    if x1 == apple_x and y1 == apple_y:
        apple_x, apple_y = generate_apple_position()
        length_of_snake += 3
        current_score += 1
    return apple_x, apple_y, length_of_snake

# Function to handle player's movement
def handle_movement():
    global x1, y1, x1_change, y1_change

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x1_change, y1_change = -snake_block_size, 0
            elif event.key == pygame.K_d:
                x1_change, y1_change = snake_block_size, 0
            elif event.key == pygame.K_w:
                y1_change, x1_change = -snake_block_size, 0
            elif event.key == pygame.K_s:
                y1_change, x1_change = snake_block_size, 0

    x1 += x1_change
    y1 += y1_change

    # Check to see if player is off screen bounds
    if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
        return True

    return False

# Function to handle game over
def game_over(score):
    message("Game Over! Press W-Play Again or Q-Quit", red)
    player_score(score)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_w:
                    main_game_loop(1)

# Main game loop
def main_game_loop(initial_length_of_snake):
    global x1, y1, x1_change, y1_change, current_score

    # Reset the current score to 0
    current_score = 0

    game_over_flag = False
    x1, y1 = display_width / 2, display_height / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    length_of_snake = initial_length_of_snake

    apple_x, apple_y = generate_apple_position()

    while not game_over_flag:
        game_over_flag = handle_movement()

        display.blit(background_image, (0, 0))
        pygame.draw.rect(display, red, [apple_x, apple_y, snake_block_size, snake_block_size])
        snake_head = [x1, y1]
        snake_List.append(snake_head)

        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_over_flag = True

        draw_snake(snake_block_size, snake_List)
        player_score(current_score)  # Display the current score
        pygame.display.update()

        apple_x, apple_y, length_of_snake = handle_apple_collision(apple_x, apple_y, length_of_snake)

        clock.tick(snake_velocity)

    game_over(current_score)  # Display game over message with score

# Start the game loop with initial snake length of 1
main_game_loop(1)
