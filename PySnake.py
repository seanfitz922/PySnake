import pygame
import os
import random

pygame.init()
pygame.font.init()

width, height = 900, 900
WIN = pygame.display.set_mode((width, height))

# Create two font objects for displaying the score and the end game
score = pygame.font.SysFont('timesnewroman', 40)
end_game = pygame.font.SysFont('timesnewroman', 100)

top_border = pygame.Rect(0, 0, width, 10)
bottom_border = pygame.Rect(0, height - 10, width, 10)
left_border = pygame.Rect(0, 0, 10, height)  # Left border rectangle
right_border = pygame.Rect(width - 10, 0, 10, height)  # Right border rectangle

snake_size = 40
snake_width, snake_height = 50, 50
snake_x = width // 2 - snake_size // 2
snake_y = height // 2 - snake_size // 2
snake = pygame.Rect(snake_x, snake_y, snake_width, snake_height)

snake_segments = [snake]

apple_size = 20
apple_width, apple_height = 10, 10
apple_x = random.randint(0, width - apple_width)
apple_y = random.randint(0, height - apple_height)

apple_hit = pygame.USEREVENT + 1
snake_hit = pygame.USEREVENT + 2
apple_score = 0
apple_moved_by_timer = False 

FPS = 60
velocity = 5
last_direction = None

red_ = (255, 0, 0)
blue_ = (0, 0, 10)
black_ = (0, 0, 0)
white_ = (255, 255, 255)
light_green_ = (144, 238, 144)
dark_green_ = (1, 50, 32)

def draw_window(snake_segments, apple, apple_score):
    WIN.fill(light_green_)

    score_text = score.render("Score: " + str(apple_score), 1, white_)
    WIN.blit(score_text, (10, 10))

    pygame.draw.rect(WIN, white_, top_border)
    pygame.draw.rect(WIN, white_, bottom_border)
    pygame.draw.rect(WIN, white_, left_border)
    pygame.draw.rect(WIN, white_, right_border)
    
    # Draw the entire snake's body
    draw_snake(snake_segments)
    
    pygame.draw.rect(WIN, red_, apple)
    pygame.display.update()

def draw_game_over():
    draw_text = end_game.render("Game Over", 1, white_)
    WIN.blit(draw_text, (width//2 - draw_text.get_width() /2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_snake(snake_segments):
    for segment in snake_segments:
        pygame.draw.rect(WIN, dark_green_, segment)

def update_snake_segments():
    for i in range(len(snake_segments) - 1, 0, -1):
        snake_segments[i] = snake_segments[i - 1].copy()

def snake_handle_movement(keys_pressed, snake):
    global last_direction

    if snake.x < 11 or snake.x > width - 65 or snake.y < 11 or snake.y > width - 65:
        pygame.event.post(pygame.event.Event(snake_hit))

    else: 
        if keys_pressed[pygame.K_a]:
            last_direction = 'left'
        elif keys_pressed[pygame.K_d]:
            last_direction = 'right'
        elif keys_pressed[pygame.K_w]:
            last_direction = 'up'
        elif keys_pressed[pygame.K_s]:
            last_direction = 'down'

        if last_direction == 'left':
            snake.x -= velocity
        elif last_direction == 'right':
            snake.x += velocity
        elif last_direction == 'up':
            snake.y -= velocity
        elif last_direction == 'down':
            snake.y += velocity

def generate_random_apple_position():
    apple_x = random.randint(30, width - apple_width - 30)
    apple_y = random.randint(30, height - apple_height - 30)
    return apple_x, apple_y

def handle_apple(apple, snake):
    global apple_moved_by_timer, apple_score, snake_segments

    if apple.colliderect(snake):
        if not apple_moved_by_timer:  # Check if the apple was not moved by the timer
            apple_score += 1  # Increase the score only if not moved by timer
        pygame.time.set_timer(apple_hit, 0)
        pygame.event.post(pygame.event.Event(apple_hit))

        # Add multiple segments to the snake's body
        num_new_segments = 10
        for _ in range(num_new_segments):
            new_segment = snake_segments[-1].copy()
            snake_segments.append(new_segment)

    else:
        apple_moved_by_timer = False  # Reset the flag when apple is not hit

def main():

    apple_x, apple_y = generate_random_apple_position()

    pygame.time.set_timer(apple_hit, 5000)

    apple = pygame.Rect(apple_x, apple_y, apple_width, apple_height)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == apple_hit:
                apple_x, apple_y = generate_random_apple_position()
                apple.x = apple_x
                apple.y = apple_y
                apple_moved_by_timer = True
                pygame.time.set_timer(apple_hit, 4000)

            elif event.type == snake_hit:
                draw_game_over()
                run = False  
                break

        keys_pressed = pygame.key.get_pressed()
        snake_handle_movement(keys_pressed, snake)
        update_snake_segments()
        handle_apple(apple, snake)
        draw_window(snake_segments, apple, apple_score)

    # Make sure to call pygame.quit() when the game loop ends
    pygame.quit()

if __name__ == "__main__":
    main()
