import pygame, json
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
    end_game,
    draw_snake,
    player_score,
)
from SnakeAI import AI 

# Set up colors and fonts
white = (255, 255, 255)
red = (213, 50, 80)

# Initialize pygame
pygame.init()

score_font = pygame.font.SysFont("timesnewroman", 25)

# Load the best genes from the JSON file
with open('best_genes.json', 'r') as file:
    best_genes = json.load(file)

# Create an instance of the AI class with the loaded genes
ai_agent = AI(best_genes)

# Main game loop
game_over_flag = False
for game in range(10):
    
    current_score = 0

    game_over_flag = False
    x1, y1 = display_width / 2, display_height / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    apple_x, apple_y = generate_apple_position()

    while not game_over_flag:
        snake_head_x, snake_head_y = x1, y1
        game_over_flag = end_game()

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
        player_score(current_score, display, score_font) 
        pygame.display.update()        
        # Calculate repulsion factors
        apple_attraction = 1  # Adjust this weight as needed
        apple_attraction = 1  # Adjust this weight as needed
        wall_repulsion = ai_agent.calculate_wall_repulsion(x1, y1, display_width, display_height)
        snake_repulsion = ai_agent.calculate_snake_repulsion(x1, y1, snake_list)

        # Update AI action based on the current position and apple position
        ai_action = ai_agent.determine_action(
            x1, y1, apple_x, apple_y, x1_change, y1_change, snake_list
        )

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
            current_score +=1

        clock.tick(snake_velocity)