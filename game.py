import pygame
import random

pygame.init()
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Anaya ka Pro Flappy Bird v2")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36, bold=True)
big_font = pygame.font.SysFont("Arial", 50, bold=True)

# Rang
sky_blue = (135, 206, 235)
yellow = (255, 223, 0)
green = (34, 139, 34)
dark_green = (0, 100, 0)
black = (0, 0, 0)
ground_color = (222, 184, 135)

# Bird - ab gol hai
bird_x = 100
bird_y = height // 2
bird_radius = 12
gravity = 0.15  # slow gravity
flap = -6
velocity = 0
wing_up = True  # wings ke liye

# Pipe
pipe_width = 70
pipe_gap = 180
pipe_distance = 280
pipes = []
for i in range(2):
    pipes.append({
        'x': width + i * pipe_distance,
        'y': random.randint(120, 380)
    })

score = 0
high_score = 0
game_over = False
frame_count = 0

def draw_pipe(pipe):
    # Pipe body
    pygame.draw.rect(screen, green, (pipe['x'], 0, pipe_width, pipe['y']))
    pygame.draw.rect(screen, green, (pipe['x'], pipe['y'] + pipe_gap, pipe_width, height))
    # Pipe top cap
    pygame.draw.rect(screen, dark_green, (pipe['x']-5, pipe['y']-20, pipe_width+10, 20))
    pygame.draw.rect(screen, dark_green, (pipe['x']-5, pipe['y'] + pipe_gap, pipe_width+10, 20))

def check_collision(pipe):
    if bird_x + bird_radius > pipe['x'] and bird_x - bird_radius < pipe['x'] + pipe_width:
        if bird_y - bird_radius < pipe['y'] or bird_y + bird_radius > pipe['y'] + pipe_gap:
            return True
    return False

running = True
while running:
    frame_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    bird_y = height // 2
                    velocity = 0
                    score = 0
                    game_over = False
                    pipes = []
                    for i in range(2):
                        pipes.append({
                            'x': width + i * pipe_distance,
                            'y': random.randint(120, 380)
                        })
                else:
                    velocity = flap

    if not game_over:
        # Gravity
        velocity += gravity
        bird_y += velocity

        # Pipe move
        for pipe in pipes:
            pipe['x'] -= 3.5
            if pipe['x'] < -pipe_width:
                pipe['x'] = width + pipe_distance
                pipe['y'] = random.randint(120, 380)
                score += 1
                if score > high_score:
                    high_score = score

            if check_collision(pipe):
                game_over = True

        if bird_y > height - 50 - bird_radius or bird_y < bird_radius:
            game_over = True

    # Drawing
    screen.fill(sky_blue)
    
    # Badal
    for i in range(3):
        pygame.draw.circle(screen, (255,255,255), (80 + i*120, 100 + i*20), 25)
        pygame.draw.circle(screen, (255,255,255), (100 + i*120, 100 + i*20), 30)
    
    # Pipe
    for pipe in pipes:
        draw_pipe(pipe)

    # Zameen
    pygame.draw.rect(screen, ground_color, (0, height - 50, width, 50))
    pygame.draw.line(screen, dark_green, (0, height - 50), (width, height - 50), 3)

    # Bird - ab gol + wings
    pygame.draw.circle(screen, yellow, (bird_x, int(bird_y)), bird_radius)
    pygame.draw.circle(screen, black, (bird_x + 5, int(bird_y) - 3), 2) # aankh
    # wings
    wing_y = int(bird_y) + (5 if wing_up else -5)
    pygame.draw.ellipse(screen, (255,200,0), (bird_x-8, wing_y, 10, 6))
    if frame_count % 10 == 0: # wings flap
        wing_up = not wing_up
    
    # Score
    score_text = font.render(f"Score: {score}", True, black)
    high_text = font.render(f"Best: {high_score}", True, black)
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 50))

    # Game Over Screen
    if game_over:
        over_text = big_font.render("GAME OVER", True, (200,0,0))
        restart_text = font.render("SPACE dabao dobara", True, black)
        screen.blit(over_text, (width//2 - 120, height//2 - 60))
        screen.blit(restart_text, (width//2 - 120, height//2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()