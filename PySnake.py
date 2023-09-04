import pygame, random, math

# Set up display dimensions and other constants
display_width = 900
display_height = 900
snake_block_size = 25  # Increase the snake size
snake_velocity = 15

# Set up colors and fonts
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Initialize global variables
x1, y1 = display_width / 2, display_height / 2
x1_change, y1_change = 0, 0

current_score = 0

display = pygame.display.set_mode((display_width, display_height))

# Load the background image
background_image = pygame.image.load("checkered-background.jpg").convert()

# Resize the background image to match the display dimensions
background_image = pygame.transform.scale(background_image, (display_width, display_height))

clock = pygame.time.Clock()

# Function to display player's score
def player_score(score, display, score_font):
    value = score_font.render("Score: " + str(score), True, white)
    display.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(display, snake_block_size, snake_list):
    for i in snake_list:
        pygame.draw.rect(display, green, [i[0], i[1], snake_block_size, snake_block_size])

# Function to generate apple's position
def generate_apple_position():
    apple_x = round(random.randrange(0, display_width - snake_block_size) / snake_block_size) * snake_block_size
    apple_y = round(random.randrange(0, display_height - snake_block_size) / snake_block_size) * snake_block_size
    return apple_x, apple_y

# Function to handle apple collision
def handle_apple_collision(apple_x, apple_y, length_of_snake):
    global current_score

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

    if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
        return True

    return False
