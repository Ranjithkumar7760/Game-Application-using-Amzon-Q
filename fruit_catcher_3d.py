import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher 3D")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (75, 225, 75)
BLUE = (65, 105, 225)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Create simple 3D-like basket
def create_basket_3d():
    # We'll create multiple surfaces for different angles
    basket_images = []
    
    # Simple basket colors
    dark_brown = (139, 69, 19)    # Brown for outline
    light_brown = (205, 133, 63)  # Light brown for fill
    
    # Create 5 angles of the basket for 3D effect
    for angle in range(-30, 31, 15):
        basket_surf = pygame.Surface((120, 80), pygame.SRCALPHA)
        
        # Calculate perspective distortion
        left_height = 40 - angle/2
        right_height = 40 + angle/2
        
        # Draw 3D basket base shape
        points = [
            (10, 60),  # Bottom left
            (110, 60),  # Bottom right
            (100, 60 - right_height),  # Top right
            (20, 60 - left_height)   # Top left
        ]
        
        # Draw basket base
        pygame.draw.polygon(basket_surf, light_brown, points)
        
        # Draw basket outline
        pygame.draw.lines(basket_surf, dark_brown, True, points, 3)
        
        # Draw simple handle
        handle_height = 20
        handle_width = 60
        handle_x = 30 + angle/2
        handle_y = 60 - (left_height + right_height)/2 - handle_height
        
        # Simple arc handle
        pygame.draw.arc(basket_surf, dark_brown, 
                       (handle_x, handle_y, handle_width, handle_height*2), 
                       math.pi, 2*math.pi, 3)
        
        # Simple vertical lines for basic weave pattern
        for i in range(6):
            x_pos = 20 + i * 15
            pygame.draw.line(basket_surf, dark_brown, 
                           (x_pos, 60 - left_height + (right_height - left_height) * (i/5)), 
                           (x_pos, 60), 2)
        
        # Simple horizontal lines
        for j in range(2):
            y_pos = 60 - (left_height + right_height) * (j+1) / 3
            pygame.draw.line(basket_surf, dark_brown, (20, y_pos), (100, y_pos), 2)
        
        basket_images.append(basket_surf)
    
    return basket_images

# Create rotating fruit images
def create_fruit_images():
    # We'll create multiple rotation frames for each fruit
    fruit_types = []
    
    # Apple (red)
    apple_frames = []
    for angle in range(0, 360, 45):  # 8 rotation frames
        apple = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Main apple body
        pygame.draw.circle(apple, RED, (25, 25), 20)
        # Highlight to give 3D effect
        highlight_pos = (25 + 8*math.cos(math.radians(angle)), 25 + 8*math.sin(math.radians(angle)))
        pygame.draw.circle(apple, (255, 150, 150), highlight_pos, 7)
        # Stem
        stem_pos = (25 + 5*math.sin(math.radians(angle)), 25 - 15*math.cos(math.radians(angle)))
        pygame.draw.line(apple, BROWN, (25, 5), stem_pos, 3)
        apple_frames.append(apple)
    fruit_types.append(apple_frames)
    
    # Orange
    orange_frames = []
    for angle in range(0, 360, 45):
        orange = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(orange, ORANGE, (25, 25), 20)
        # Highlight
        highlight_pos = (25 + 8*math.cos(math.radians(angle)), 25 + 8*math.sin(math.radians(angle)))
        pygame.draw.circle(orange, (255, 200, 100), highlight_pos, 7)
        orange_frames.append(orange)
    fruit_types.append(orange_frames)
    
    # Banana (yellow)
    banana_frames = []
    for angle in range(0, 360, 45):
        banana = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Rotate the banana
        start_angle = angle / 180 * math.pi
        end_angle = (angle + 180) / 180 * math.pi
        pygame.draw.arc(banana, YELLOW, (5, 5, 40, 40), start_angle, end_angle, 10)
        banana_frames.append(banana)
    fruit_types.append(banana_frames)
    
    # Blueberry
    blueberry_frames = []
    for angle in range(0, 360, 45):
        blueberry = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(blueberry, BLUE, (25, 25), 18)
        # Highlight
        highlight_pos = (25 + 7*math.cos(math.radians(angle)), 25 + 7*math.sin(math.radians(angle)))
        pygame.draw.circle(blueberry, (100, 150, 255), highlight_pos, 6)
        blueberry_frames.append(blueberry)
    fruit_types.append(blueberry_frames)
    
    # Grape
    grape_frames = []
    for angle in range(0, 360, 45):
        grape = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Main grape
        pygame.draw.circle(grape, PURPLE, (25, 25), 18)
        # Highlight for 3D effect
        highlight_pos = (25 + 7*math.cos(math.radians(angle)), 25 + 7*math.sin(math.radians(angle)))
        pygame.draw.circle(grape, (180, 100, 180), highlight_pos, 6)
        grape_frames.append(grape)
    fruit_types.append(grape_frames)
    
    return fruit_types

# Create animated background
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
    
    # Draw grass with 3D effect
    for y in range(HEIGHT-30, HEIGHT):
        # Darker at the bottom for 3D effect
        darkness = (y - (HEIGHT-30)) / 30  # 0 to 1
        green_val = 225 - int(darkness * 100)
        bg.fill((75, green_val, 75), (0, y, WIDTH, 1))
    
    return bg

# Create images
basket_images = create_basket_3d()
fruit_images = create_fruit_images()
background = create_background()

# Player (basket)
basket_width = 120
basket_height = 80
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 8
basket_angle_index = 2  # Middle angle (straight)
basket_angle_target = 2
basket_angle_change_speed = 0.2

# Fruits
fruits = []
fruit_types = len(fruit_images)
fruit_size = 25
fruit_speed = 3
fruit_spawn_rate = 60  # frames
fruit_timer = 0
max_fruit_speed = 10

# Particle effects
particles = []

# Shadow effects
shadows = []

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
time_elapsed = 0

def draw_basket():
    # Calculate basket angle based on movement
    global basket_angle_index, basket_angle_target
    
    # Draw shadow
    shadow_height = 10
    shadow_width = basket_width - 20
    shadow_surf = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, shadow_width, shadow_height))
    screen.blit(shadow_surf, (basket_x + 10, basket_y + basket_height - 5))
    
    # Draw the basket with current angle
    screen.blit(basket_images[int(basket_angle_index)], (basket_x, basket_y))
    
    # Smoothly transition to target angle
    if basket_angle_index < basket_angle_target:
        basket_angle_index = min(basket_angle_index + basket_angle_change_speed, basket_angle_target)
    elif basket_angle_index > basket_angle_target:
        basket_angle_index = max(basket_angle_index - basket_angle_change_speed, basket_angle_target)

def spawn_fruit():
    x = random.randint(fruit_size, WIDTH - fruit_size)
    fruit_type = random.randint(0, fruit_types-1)
    rotation_frame = random.randint(0, 7)  # Random starting rotation
    rotation_speed = random.uniform(0.1, 0.3)  # Random rotation speed
    fruits.append([x, -fruit_size, fruit_speed, fruit_type, rotation_frame, rotation_speed])

def draw_fruits():
    for fruit in fruits:
        fruit_type = fruit[3]
        rotation_frame = int(fruit[4]) % 8
        
        # Draw shadow that gets bigger as fruit gets closer to ground
        shadow_size = fruit_size * (0.5 + 0.5 * (fruit[1] / HEIGHT))
        shadow_surf = pygame.Surface((shadow_size*2, shadow_size/2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, shadow_size*2, shadow_size/2))
        screen.blit(shadow_surf, (fruit[0] - shadow_size, HEIGHT - 25))
        
        # Draw fruit with current rotation frame
        fruit_img = fruit_images[fruit_type][rotation_frame]
        screen.blit(fruit_img, (fruit[0] - 25, fruit[1] - 25))

def create_particles(x, y, color):
    num_particles = 20
    for _ in range(num_particles):
        particle_x = x
        particle_y = y
        direction_x = random.uniform(-3, 3)
        direction_y = random.uniform(-5, 0)  # Mostly upward
        particle_size = random.randint(2, 6)
        particle_life = random.randint(20, 40)
        particles.append([particle_x, particle_y, direction_x, direction_y, particle_size, particle_life, color])

def update_particles():
    for particle in particles[:]:
        particle[0] += particle[2]  # x position
        particle[1] += particle[3]  # y position
        particle[3] += 0.1  # gravity
        particle[5] -= 1  # life
        
        if particle[5] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle[6], (int(particle[0]), int(particle[1])), particle[4])

def update_fruits():
    global score, misses, fruit_speed
    
    for fruit in fruits[:]:
        fruit[1] += fruit[2]  # Move fruit down
        fruit[4] += fruit[5]  # Rotate fruit
        
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
            
            # Increase speed every 5 points
            if score % 5 == 0 and fruit_speed < max_fruit_speed:
                fruit_speed += 0.5
        
        # Check if fruit is missed
        elif fruit[1] > HEIGHT:
            fruits.remove(fruit)
            misses += 1

def show_start_screen():
    # Draw animated background
    screen.blit(background, (0, 0))
    
    # Animated title
    title_y_offset = math.sin(time_elapsed / 500) * 10
    title_text = title_font.render("Fruit Catcher 3D", True, (50, 50, 150))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4 + title_y_offset))
    
    # Instructions with 3D shadow effect
    instructions = [
        "Catch falling fruits with your basket",
        "Use LEFT and RIGHT arrow keys to move",
        "Miss 3 fruits and it's game over!",
        "Press SPACE to start"
    ]
    
    for i, text in enumerate(instructions):
        # Shadow text (offset)
        shadow = font.render(text, True, (100, 100, 100))
        screen.blit(shadow, (WIDTH//2 - shadow.get_width()//2 + 3, HEIGHT//2 + i*50 + 3))
        
        # Main text
        color = BLACK if i < 3 else (200, 0, 0)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 + i*50))
    
    # Draw rotating sample fruits
    for i in range(fruit_types):
        rotation_frame = int(time_elapsed / 100) % 8
        screen.blit(fruit_images[i][rotation_frame], (WIDTH//2 - 125 + i*60, HEIGHT//2 + 230))

def show_game_over():
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Animated game over text
    scale = 1.0 + 0.1 * math.sin(time_elapsed / 200)
    game_over_text = title_font.render("GAME OVER", True, RED)
    scaled_width = int(game_over_text.get_width() * scale)
    scaled_height = int(game_over_text.get_height() * scale)
    scaled_text = pygame.transform.scale(game_over_text, (scaled_width, scaled_height))
    
    screen.blit(scaled_text, (WIDTH//2 - scaled_width//2, HEIGHT//2 - 100))
    
    # Score with 3D effect
    score_shadow = font.render(f"Final Score: {score}", True, (50, 50, 50))
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_shadow, (WIDTH//2 - score_text.get_width()//2 + 3, HEIGHT//2 + 3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    
    # Instructions
    restart_text = font.render("Press R to restart or Q to quit", True, WHITE)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70))

def reset_game():
    global score, misses, fruits, fruit_speed, game_over, particles
    score = 0
    misses = 0
    fruits = []
    particles = []
    fruit_speed = 3
    game_over = False

# Animated clouds
clouds = []
for _ in range(5):
    cloud_x = random.randint(0, WIDTH)
    cloud_y = random.randint(20, 200)
    cloud_size = random.randint(40, 100)
    cloud_speed = random.uniform(0.2, 0.5)
    clouds.append([cloud_x, cloud_y, cloud_size, cloud_speed])

def update_clouds():
    for cloud in clouds:
        cloud[0] += cloud[3]
        if cloud[0] > WIDTH + cloud[2]:
            cloud[0] = -cloud[2] * 2
            cloud[1] = random.randint(20, 200)

def draw_clouds():
    for cloud in clouds:
        pygame.draw.ellipse(screen, WHITE, (cloud[0], cloud[1], cloud[2]*2, cloud[2]))
        pygame.draw.ellipse(screen, WHITE, (cloud[0] + cloud[2]//2, cloud[1] - cloud[2]//4, cloud[2]*2, cloud[2]))
        pygame.draw.ellipse(screen, WHITE, (cloud[0] - cloud[2]//2, cloud[1] - cloud[2]//4, cloud[2]*2, cloud[2]))

# Main game loop
running = True
while running:
    time_elapsed += clock.get_time()
    
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
    
    # Draw sky gradient background
    screen.blit(background, (0, 0))
    
    # Update and draw animated clouds
    update_clouds()
    draw_clouds()
    
    if not game_started:
        show_start_screen()
    elif not game_over:
        # Move basket
        keys = pygame.key.get_pressed()
        moving = False
        
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
            basket_angle_target = 0  # Tilt left
            moving = True
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed
            basket_angle_target = 4  # Tilt right
            moving = True
            
        if not moving:
            basket_angle_target = 2  # Center
        
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
        
        # Draw game elements
        draw_fruits()
        draw_basket()
        draw_particles()
        
        # Display score and misses with 3D shadow effect
        score_shadow = font.render(f"Score: {score}", True, (50, 50, 50))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_shadow, (13, 13))
        screen.blit(score_text, (10, 10))
        
        misses_shadow = font.render(f"Misses: {misses}/{max_misses}", True, (50, 50, 50))
        misses_text = font.render(f"Misses: {misses}/{max_misses}", True, BLACK)
        screen.blit(misses_shadow, (WIDTH - misses_text.get_width() - 7, 13))
        screen.blit(misses_text, (WIDTH - misses_text.get_width() - 10, 10))
    else:
        # Draw game elements in background
        draw_fruits()
        draw_basket()
        draw_particles()
        
        # Show game over screen
        show_game_over()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()