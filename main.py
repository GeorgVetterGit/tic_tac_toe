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

grid = [[None for _ in range(3)] for _ in range(3)]  # Initialize a 3x3 grid

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            # Check if the click is within the grid area
            if mouse_y > menu_height:
                # Calculate the grid cell based on mouse position
                cell_x = mouse_x // (screen_width // 3)
                cell_y = (mouse_y - menu_height) // (screen_width // 3)

                # Check if the cell is already occupied
                if grid[cell_y][cell_x] is None:
                    # Mark the cell with 'X'
                    grid[cell_y][cell_x] = 'X'
                

    # Check if the game should end
    if any(all(cell == 'X' for cell in row) for row in grid) or \
       any(all(grid[y][x] == 'X' for y in range(3)) for x in range(3)) or \
       all(grid[i][i] == 'X' for i in range(3)) or \
       all(grid[i][2 - i] == 'X' for i in range(3)):
        print("Player X wins!")
        running = False
    
    # Check for a draw
    if all(cell is not None for row in grid for cell in row):
        print("It's a draw!")
        running = False

    if any(all(cell == 'O' for cell in row) for row in grid) or \
       any(all(grid[y][x] == 'O' for y in range(3)) for x in range(3)) or \
       all(grid[i][i] == 'O' for i in range(3)) or \
       all(grid[i][2 - i] == 'O' for i in range(3)):
        print("Computer wins!")
        running = False

    # Fill the background
    screen.fill(COLORS['WHITE'])  # Black color

    # Draw the grid
    for x in range(1, 3):
        pygame.draw.line(screen, COLORS['BLACK'], (x * screen_width // 3, menu_height), (x * screen_width // 3, screen_height), 2)
    for y in range(1, 3):
        pygame.draw.line(screen, COLORS['BLACK'], (0, y * screen_width // 3 + menu_height), (screen_width, y * screen_width // 3 + menu_height), 2)   
    
    # Draw the grid cells
    for y in range(3):
        for x in range(3):
            if grid[y][x] == 'X':
                pygame.draw.line(screen, COLORS['BLACK'], 
                                 (x * screen_width // 3 + 10, 
                                  y * screen_width // 3 + menu_height + 10), 
                                 (x * screen_width // 3 + screen_width // 3 - 10, 
                                  y * screen_width // 3 + menu_height + screen_width // 3 - 10), 
                                 15)
                pygame.draw.line(screen, COLORS['BLACK'], 
                                 (x * screen_width // 3 + screen_width // 3 - 10, 
                                  y * screen_width // 3 + menu_height + 10), 
                                 (x * screen_width // 3 + 10, 
                                  y * screen_width // 3 + menu_height + screen_width // 3 - 10), 
                                 15)

    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit()
