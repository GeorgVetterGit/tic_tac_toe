import pygame

# Initialize PyGame
pygame.init()

# Set screen dimensions
screen_width = 400
menu_height = 100
screen_height = screen_width + menu_height
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Tic Tac Toe")

COLORS = {'BLACK': (0, 0, 0),
          'WHITE': (255, 255, 255),
          'RED': (255, 0, 0),
          'GREEN': (0, 255, 0),
          'BLUE': (0, 0, 255)}

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(COLORS['WHITE'])  # Black color

    # Draw the grid
    for x in range(1, 3):
        pygame.draw.line(screen, COLORS['BLACK'], (x * screen_width // 3, menu_height), (x * screen_width // 3, screen_height), 2)
    for y in range(1, 3):
        pygame.draw.line(screen, COLORS['BLACK'], (0, y * screen_width // 3 + menu_height), (screen_width, y * screen_width // 3 + menu_height), 2)   

    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit()
