import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Rush")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player properties
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT // 2 - player_height // 2
player_speed = 5
score = 0

# Load images
coin_image = pygame.image.load("coin.png")
tree_image = pygame.image.load("tree.png")
train_image = pygame.image.load("train.png")

# Scale images to fit properly
coin_image = pygame.transform.scale(coin_image, (30, 30))
tree_image = pygame.transform.scale(tree_image, (60, 60))
train_image = pygame.transform.scale(train_image, (100, 50))

# Font for displaying text
font = pygame.font.SysFont("Arial", 30)

# Function to create coins
def create_coin():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(-100, -30)
    return pygame.Rect(x, y, 30, 30)

# Function to create obstacles (trees and trains)
def create_obstacle():
    if random.choice([True, False]):
        x = random.randint(0, WIDTH - 60)
        y = random.randint(-100, -60)
        return pygame.Rect(x, y, 60, 60), 'tree'
    else:
        x = random.randint(0, WIDTH - 100)
        y = random.randint(-100, -50)
        return pygame.Rect(x, y, 100, 50), 'train'

# Game Loop
def game_loop():
    global player_x, player_y, score
    running = True
    clock = pygame.time.Clock()

    # Create coins and obstacles
    coins = [create_coin() for _ in range(5)]
    obstacles = [create_obstacle() for _ in range(5)]

    # Main game loop
    while running:
        screen.fill(WHITE)

        # Use a solid color background (light gray)
        background_image = pygame.Surface((WIDTH, HEIGHT))
        background_image.fill((200, 200, 200))  # Light gray color
        screen.blit(background_image, (0, 0))  # Fill the screen with gray

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key press detection for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Prevent player from going out of bounds
        player_x = max(0, min(player_x, WIDTH - player_width))
        player_y = max(0, min(player_y, HEIGHT - player_height))

        # Move coins down
        for coin in coins[:]:
            coin.y += 3
            if coin.y > HEIGHT:
                coin.y = random.randint(-100, -30)
                coin.x = random.randint(0, WIDTH - 30)

            # Check if player collects the coin
            if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(coin):
                coins.remove(coin)
                score += 1
                coins.append(create_coin())  # Add a new coin

            screen.blit(coin_image, coin.topleft)

        # Move obstacles down and check for collisions
        for obstacle, type_ in obstacles[:]:
            obstacle.y += 5
            if obstacle.y > HEIGHT:
                obstacle.y = random.randint(-100, -50)
                obstacle.x = random.randint(0, WIDTH - 100)

            if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(obstacle):
                text = font.render("Game Over!", True, (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
                break

            if type_ == 'tree':
                screen.blit(tree_image, obstacle.topleft)
            else:
                screen.blit(train_image, obstacle.topleft)

        # Draw player
        pygame.draw.rect(screen, BLUE, pygame.Rect(player_x, player_y, player_width, player_height))

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.flip()

        # Set the FPS (Frames per second)
        clock.tick(60)

# Start the game
game_loop()

# Quit Pygame
pygame.quit()
sys.exit()
