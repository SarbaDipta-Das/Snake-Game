import pygame
import sys
import random
import time

# --- Initialization ---
# Check for initializing errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f"[!] Had {check_errors[1]} errors when initialising pygame, exiting...")
    sys.exit(-1)
else:
    print("[+] Pygame initialised successfully")

# --- Game Window ---
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
pygame.display.set_caption('Snake Game by AI')
game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Colors (RGB) ---
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# --- Game Variables ---
# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Snake properties
GRID_SIZE = 20
# Ensure snake starts on the grid
snake_pos = [100, 60] 
snake_body = [[100, 60], [100 - GRID_SIZE, 60], [100 - (2 * GRID_SIZE), 60]]

# Food properties
food_pos = [random.randrange(1, (SCREEN_WIDTH // GRID_SIZE)) * GRID_SIZE,
            random.randrange(1, (SCREEN_HEIGHT // GRID_SIZE)) * GRID_SIZE]
food_spawn = True

# Direction
direction = 'RIGHT'
change_to = direction

# Score
score = 0

# --- Game Over Function ---
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over!', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0) # Using 0 for final score position
    pygame.display.flip()
    
    time.sleep(3) # Wait for 3 seconds before closing
    pygame.quit()
    sys.exit()

# --- Score Function ---
def show_score(choice):
    score_font = pygame.font.SysFont('consolas', 20)
    score_surface = score_font.render('Score : ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()

    if choice == 1: # Display during the game
        score_rect.midtop = (80, 10)
    else: # Display at game over
        score_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)

    game_window.blit(score_surface, score_rect)

# --- Main Game Loop ---
while True:
    # --- Event Handler ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if (event.key == pygame.K_UP or event.key == ord('w')) and direction != 'DOWN':
                change_to = 'UP'
            if (event.key == pygame.K_DOWN or event.key == ord('s')) and direction != 'UP':
                change_to = 'DOWN'
            if (event.key == pygame.K_LEFT or event.key == ord('a')) and direction != 'RIGHT':
                change_to = 'LEFT'
            if (event.key == pygame.K_RIGHT or event.key == ord('d')) and direction != 'LEFT':
                change_to = 'RIGHT'

    # Making sure the snake cannot move in the opposite direction instantaneously
    direction = change_to

    # --- Snake Movement ---
    if direction == 'UP':
        snake_pos[1] -= GRID_SIZE
    if direction == 'DOWN':
        snake_pos[1] += GRID_SIZE
    if direction == 'LEFT':
        snake_pos[0] -= GRID_SIZE
    if direction == 'RIGHT':
        snake_pos[0] += GRID_SIZE

    # --- Snake Growth ---
    # Insert new head position
    snake_body.insert(0, list(snake_pos))
    # Check if snake ate food
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        # If no food is eaten, remove the last segment of the snake
        snake_body.pop()

    # --- Respawn Food ---
    if not food_spawn:
        food_pos = [random.randrange(1, (SCREEN_WIDTH // GRID_SIZE)) * GRID_SIZE,
                    random.randrange(1, (SCREEN_HEIGHT // GRID_SIZE)) * GRID_SIZE]
    food_spawn = True

    # --- Drawing ---
    game_window.fill(BLACK) # Clear the screen
    
    # Draw the snake
    for pos in snake_body:
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))

    # Draw the food
    pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0], food_pos[1], GRID_SIZE, GRID_SIZE))

    # --- Game Over Conditions ---
    # 1. Collision with window boundaries
    if snake_pos[0] < 0 or snake_pos[0] > SCREEN_WIDTH - GRID_SIZE:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > SCREEN_HEIGHT - GRID_SIZE:
        game_over()
        
    # 2. Collision with its own body
    # Slicing the list to check the head against the rest of the body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Display score
    show_score(1)

    # Refresh game screen
    pygame.display.update()

    # Control the game speed
    fps_controller.tick(15)