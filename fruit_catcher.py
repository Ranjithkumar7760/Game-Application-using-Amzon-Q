import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (75, 225, 75)
BLUE = (65, 105, 225)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (135, 206, 235)

# Load or create images
def create_basket_image():
    basket_surf = pygame.Surface((100, 60), pygame.SRCALPHA)
    # Draw basket base
    pygame.draw.rect(basket_surf, (139, 69, 19), (0, 40, 100, 20), border_radius=5)  # Brown base
    # Draw basket weaving
    for i in range(5):
        pygame.draw.rect(basket_surf, (205, 133, 63), (5 + i*20, 10, 10, 40), border_radius=3)  # Vertical weaving
    pygame.draw.rect(basket_surf, (205, 133, 63), (5, 20, 90, 8), border_radius=2)  # Horizontal weaving
    pygame.draw.rect(basket_surf, (205, 133, 63), (5, 35, 90, 8), border_radius=2)  # Horizontal weaving
    return basket_surf

def create_fruit_images():
    fruit_images = []
    # Apple (red)
    apple = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(apple, RED, (20, 20), 18)
    pygame.draw.rect(apple, (101, 67, 33), (18, 0, 4, 10))  # stem
    fruit_images.append(apple)
    
    # Orange
    orange = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(orange, ORANGE, (20, 20), 18)
    pygame.draw.rect(orange, (101, 67, 33), (18, 0, 4, 8))  # stem
    fruit_images.append(orange)
    
    # Banana (yellow)
    banana = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.arc(banana, YELLOW, (5, 5, 30, 30), 0.3, 4.0, 5)
    fruit_images.append(banana)
    
    # Blueberry
    blueberry = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(blueberry, BLUE, (20, 20), 15)
    fruit_images.append(blueberry)
    
    # Grape
    grape = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(grape, PURPLE, (20, 20), 16)
    fruit_images.append(grape)
    
    return fruit_images

# Create background
def create_background():
    bg = pygame.Surface((WIDTH, HEIGHT))
    # Sky gradient
    for y in range(HEIGHT):
        # Create a gradient from light blue to darker blue
        color_val = 255 - int(y * 0.3)
        if color_val < 100:
            color_val = 100
        bg.fill((100, color_val, 255), (0, y, WIDTH, 1))
    
    # Draw clouds
    for _ in range(5):
        cloud_x = random.randint(0, WIDTH)
        cloud_y = random.randint(20, 200)
        cloud_size = random.randint(40, 100)
        pygame.draw.ellipse(bg, WHITE, (cloud_x, cloud_y, cloud_size*2, cloud_size))
        pygame.draw.ellipse(bg, WHITE, (cloud_x + cloud_size//2, cloud_y - cloud_size//4, cloud_size*2, cloud_size))
        pygame.draw.ellipse(bg, WHITE, (cloud_x - cloud_size//2, cloud_y - cloud_size//4, cloud_size*2, cloud_size))
    
    # Draw grass
    pygame.draw.rect(bg, GREEN, (0, HEIGHT-30, WIDTH, 30))
    
    return bg

# Create images
basket_image = create_basket_image()
fruit_images = create_fruit_images()
background = create_background()

# Try to load sound effects
try:
    catch_sound = pygame.mixer.Sound("catch.wav")
    miss_sound = pygame.mixer.Sound("miss.wav")
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    sounds_loaded = True
except:
    sounds_loaded = False

# Player (basket)
basket_width = 100
basket_height = 60
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 8

# Fruits
fruits = []
fruit_types = len(fruit_images)
fruit_size = 20
fruit_speed = 3
fruit_spawn_rate = 60  # frames
fruit_timer = 0
max_fruit_speed = 10

# Particle effects
particles = []

# Game variables
score = 0
misses = 0
max_misses = 3
font = pygame.font.SysFont("comicsansms", 36)
small_font = pygame.font.SysFont("comicsansms", 24)
title_font = pygame.font.SysFont("comicsansms", 72)
clock = pygame.time.Clock()
game_over = False
game_started = False

def draw_basket():
    screen.blit(basket_image, (basket_x, basket_y))

def spawn_fruit():
    x = random.randint(fruit_size, WIDTH - fruit_size)
    fruit_type = random.randint(0, fruit_types-1)
    fruits.append([x, -fruit_size, fruit_speed, fruit_type])

def draw_fruits():
    for fruit in fruits:
        fruit_type = fruit[3]
        screen.blit(fruit_images[fruit_type], (fruit[0] - 20, fruit[1] - 20))

def create_particles(x, y, color):
    num_particles = 15
    for _ in range(num_particles):
        particle_x = x
        particle_y = y
        direction_x = random.uniform(-3, 3)
        direction_y = random.uniform(-3, 3)
        particle_size = random.randint(2, 6)
        particle_life = random.randint(20, 40)
        particles.append([particle_x, particle_y, direction_x, direction_y, particle_size, particle_life, color])

def update_particles():
    for particle in particles[:]:
        particle[0] += particle[2]  # x position
        particle[1] += particle[3]  # y position
        particle[5] -= 1  # life
        
        if particle[5] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle[6], (int(particle[0]), int(particle[1])), particle[4])

def update_fruits():
    global score, misses, fruit_speed
    
    for i, fruit in enumerate(fruits[:]):
        fruit[1] += fruit[2]  # Move fruit down
        
        # Check if fruit is caught
        if (basket_x < fruit[0] < basket_x + basket_width and 
            basket_y < fruit[1] < basket_y + basket_height):
            fruits.remove(fruit)
            score += 1
            
            # Create particles for visual effect
            fruit_type = fruit[3]
            if fruit_type == 0:  # Apple
                color = RED
            elif fruit_type == 1:  # Orange
                color = ORANGE
            elif fruit_type == 2:  # Banana
                color = YELLOW
            elif fruit_type == 3:  # Blueberry
                color = BLUE
            else:  # Grape
                color = PURPLE
                
            create_particles(fruit[0], fruit[1], color)
            
            # Play sound if available
            if sounds_loaded:
                catch_sound.play()
                
            # Increase speed every 5 points
            if score % 5 == 0 and fruit_speed < max_fruit_speed:
                fruit_speed += 0.5
        
        # Check if fruit is missed
        elif fruit[1] > HEIGHT:
            fruits.remove(fruit)
            misses += 1
            
            # Play sound if available
            if sounds_loaded:
                miss_sound.play()

def show_start_screen():
    # Draw background
    screen.blit(background, (0, 0))
    
    # Title
    title_text = title_font.render("Fruit Catcher", True, (50, 50, 150))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
    
    # Instructions
    instruction1 = font.render("Catch falling fruits with your basket", True, BLACK)
    instruction2 = font.render("Use LEFT and RIGHT arrow keys to move", True, BLACK)
    instruction3 = font.render("Miss 3 fruits and it's game over!", True, BLACK)
    instruction4 = font.render("Press SPACE to start", True, (200, 0, 0))
    
    screen.blit(instruction1, (WIDTH//2 - instruction1.get_width()//2, HEIGHT//2))
    screen.blit(instruction2, (WIDTH//2 - instruction2.get_width()//2, HEIGHT//2 + 50))
    screen.blit(instruction3, (WIDTH//2 - instruction3.get_width()//2, HEIGHT//2 + 100))
    screen.blit(instruction4, (WIDTH//2 - instruction4.get_width()//2, HEIGHT//2 + 170))
    
    # Draw sample fruits
    for i in range(fruit_types):
        screen.blit(fruit_images[i], (WIDTH//2 - 100 + i*50, HEIGHT//2 + 230))

def show_game_over():
    # Play game over sound if available
    if sounds_loaded and misses >= max_misses:
        game_over_sound.play()
        
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    game_over_text = title_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70))

def reset_game():
    global score, misses, fruits, fruit_speed, game_over, particles
    score = 0
    misses = 0
    fruits = []
    particles = []
    fruit_speed = 3
    game_over = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
    
    if not game_started:
        show_start_screen()
    elif not game_over:
        # Move basket
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed
        
        # Spawn fruits
        fruit_timer += 1
        if fruit_timer >= fruit_spawn_rate:
            spawn_fruit()
            fruit_timer = 0
        
        # Update game elements
        update_fruits()
        update_particles()
        
        # Check for game over
        if misses >= max_misses:
            game_over = True
        
        # Draw everything
        screen.blit(background, (0, 0))
        draw_basket()
        draw_fruits()
        draw_particles()
        
        # Display score and misses
        score_text = font.render(f"Score: {score}", True, BLACK)
        misses_text = font.render(f"Misses: {misses}/{max_misses}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (WIDTH - misses_text.get_width() - 10, 10))
    else:
        # Draw game elements in background
        screen.blit(background, (0, 0))
        draw_basket()
        draw_fruits()
        draw_particles()
        
        # Display score and misses
        score_text = font.render(f"Score: {score}", True, BLACK)
        misses_text = font.render(f"Misses: {misses}/{max_misses}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (WIDTH - misses_text.get_width() - 10, 10))
        
        # Show game over screen
        show_game_over()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()