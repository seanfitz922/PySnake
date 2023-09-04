import pygame
from PySnake import (
    display_width,
    display_height,
    snake_block_size,
    background_image,
    snake_velocity,
    clock,
    display,
    snake_block_size,
    generate_apple_position,
    handle_apple_collision,
    handle_movement,
    draw_snake,
    player_score,
)
from SnakeAI import AI

# Set up colors and fonts
white = (255, 255, 255)
red = (213, 50, 80)

# Initialize pygame
pygame.init()

# Initialize global variables
x1, y1 = display_width / 2, display_height / 2
x1_change, y1_change = 0, 0

current_score = 0
score_font = pygame.font.SysFont("timesnewroman", 25)

# Create an instance of the AI class with initial genes
ai_agent = AI(["up", "down", "left", "right"])

# Main game loop
game_over_flag = False
for game in range(10):

    # Generate initial apple position
    apple_x, apple_y = generate_apple_position()

    # Reset the current score to 0
    current_score = 0

    game_over_flag = False
    x1, y1 = display_width / 2, display_height / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    apple_x, apple_y = generate_apple_position()

    while not game_over_flag:
        game_over_flag = handle_movement()

        display.blit(background_image, (0, 0))
        pygame.draw.rect(display, red, [apple_x, apple_y, snake_block_size, snake_block_size])
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_over_flag = True

        draw_snake(display, snake_block_size, snake_list)
        player_score(current_score, display, score_font)  # Display the current score
        pygame.display.update()

        apple_x, apple_y, length_of_snake = handle_apple_collision(apple_x, apple_y, length_of_snake)

        # Update AI action based on the current position and apple position
        ai_action = ai_agent.determine_action(x1, y1, apple_x, apple_y)

        # Use AI action for movement
        if ai_action == "up":
            y1_change, x1_change = -snake_block_size, 0
        elif ai_action == "down":
            y1_change, x1_change = snake_block_size, 0
        elif ai_action == "left":
            y1_change, x1_change = 0, -snake_block_size
        elif ai_action == "right":
            y1_change, x1_change = 0, snake_block_size

        # Update snake's position
        x1 += x1_change
        y1 += y1_change

        # Check if the snake goes out of bounds
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_over_flag = True

        # Check if the snake eats the apple
        if (x1, y1) == (apple_x, apple_y):
            apple_x, apple_y = generate_apple_position()
            length_of_snake += 1

        clock.tick(snake_velocity)
