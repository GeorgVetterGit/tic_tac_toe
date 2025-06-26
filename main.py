import pygame

# Initialize PyGame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Tic Tac Toe")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill((0, 0, 0))  # Black color

    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit()
