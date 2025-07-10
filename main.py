import pygame
import numpy as np
import agents

# Initialize PyGame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 400
MENU_HEIGHT = 100
SCREEN_HEIGHT = SCREEN_WIDTH + MENU_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon = pygame.image.load('/Users/georg/Projects/Tiny Games in Python/tic_tac_toe/tic_tac_toe/icon.png')
pygame.display.set_icon(icon)  # Set the icon for the window

# Set window title
pygame.display.set_caption("Tic Tac Toe")

COLORS = {'BLACK': (0, 0, 0),
          'WHITE': (255, 255, 255),
          'RED': (255, 0, 0),
          'GREEN': (0, 255, 0),
          'BLUE': (0, 0, 255),
          'BACKGROUND': (32, 32, 32),
          'MENU': (18, 18, 18),
          'X_COLOR': (220, 120, 120),
          'O_COLOR': (120, 160, 220),
          'LINE_COLOR': (6, 64, 64),
          'TEXT_COLOR': (229, 229, 229)}  

def initialize_game():
    """Reset the game grid and turn."""
    global grid, turn
    grid = [[None for _ in range(3)] for _ in range(3)]  # Initialize a 3x3 grid
    # set turn variable
    if np.random.rand() < 0.5:
        turn = 'O'  # Agent starts with 'O'
    else:
        turn = 'X'  # Player starts with 'X'
    return '', grid, turn

agent = agents.MinimaxAgent()  # Initialize the agent
game_over, grid, turn = initialize_game()  # Initialize the game

def game_over_message(winner):
    """Display the game over message."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"{winner} wins!", True, COLORS['RED'])
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    # write time till game reset is 3 seconds
    font = pygame.font.Font(None, 24)
    text = font.render("Resetting in 3 seconds...", True, COLORS['TEXT_COLOR'])
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(text, text_rect)
    # update the display
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn == 'X':
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            # Check if the click is within the grid area
            if mouse_y > MENU_HEIGHT:
                # Calculate the grid cell based on mouse position
                cell_x = mouse_x // (SCREEN_WIDTH // 3)
                cell_y = (mouse_y - MENU_HEIGHT) // (SCREEN_WIDTH // 3)

                # Check if the cell is already occupied
                if grid[cell_y][cell_x] is None:
                    # Mark the cell with 'X'
                    grid[cell_y][cell_x] = 'X'
                    # Switch turn to 'O'
                    turn = 'O'
                

    if turn == 'O':
        # Get the agent's move
        try:
            move = agent.get_move(grid)
            cell_x, cell_y = move
            # Check if the cell is already occupied
            if grid[cell_x][cell_y] is None:
                # Mark the cell with 'O'
                grid[cell_x][cell_y] = 'O'
                turn = 'X' # Switch turn to 'X'
        except ValueError:
            game_over = 'Nobody' # If no moves left, it's a draw

    # Check if the game should end
    if any(all(cell == 'X' for cell in row) for row in grid) or \
       any(all(grid[y][x] == 'X' for y in range(3)) for x in range(3)) or \
       all(grid[i][i] == 'X' for i in range(3)) or \
       all(grid[i][2 - i] == 'X' for i in range(3)):
        game_over = 'Player X'
    
    # Check for a draw
    if all(cell is not None for row in grid for cell in row):
        game_over = 'Nobody'

    if any(all(cell == 'O' for cell in row) for row in grid) or \
       any(all(grid[y][x] == 'O' for y in range(3)) for x in range(3)) or \
       all(grid[i][i] == 'O' for i in range(3)) or \
       all(grid[i][2 - i] == 'O' for i in range(3)):
        game_over = 'Agent O'

    # Fill the background
    screen.fill(COLORS['BACKGROUND'])  # Black color

    # Draw the menu
    pygame.draw.rect(screen, COLORS['MENU'], (0, 0, SCREEN_WIDTH, MENU_HEIGHT))
    font = pygame.font.Font(None, 25)
    text = font.render(f"Tic Tac Toe - Player X vs {agent.name} O", True, COLORS['TEXT_COLOR'])
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, MENU_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Draw the grid
    for x in range(1, 3):
        pygame.draw.line(screen, COLORS['LINE_COLOR'], (x * SCREEN_WIDTH // 3, MENU_HEIGHT), (x * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 2)
    for y in range(1, 3):
        pygame.draw.line(screen, COLORS['LINE_COLOR'], (0, y * SCREEN_WIDTH // 3 + MENU_HEIGHT), (SCREEN_WIDTH, y * SCREEN_WIDTH // 3 + MENU_HEIGHT), 2)   
    
    # Draw the grid cells
    for y in range(3):
        for x in range(3):
            if grid[y][x] == 'X':
                pygame.draw.line(screen, COLORS['X_COLOR'], 
                                 (x * SCREEN_WIDTH // 3 + 10, 
                                  y * SCREEN_WIDTH // 3 + MENU_HEIGHT + 10), 
                                 (x * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 3 - 10, 
                                  y * SCREEN_WIDTH // 3 + MENU_HEIGHT + SCREEN_WIDTH // 3 - 10), 
                                 15)
                pygame.draw.line(screen, COLORS['X_COLOR'], 
                                 (x * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 3 - 10, 
                                  y * SCREEN_WIDTH // 3 + MENU_HEIGHT + 10), 
                                 (x * SCREEN_WIDTH // 3 + 10, 
                                  y * SCREEN_WIDTH // 3 + MENU_HEIGHT + SCREEN_WIDTH // 3 - 10), 
                                 15)
    for y in range(3):
        for x in range(3):
            if grid[y][x] == 'O':
                pygame.draw.circle(screen, COLORS['O_COLOR'], 
                                   (x * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 6, 
                                    y * SCREEN_WIDTH // 3 + MENU_HEIGHT + SCREEN_WIDTH // 6), 
                                   SCREEN_WIDTH // 6 - 10, 
                                   15)
    
    if game_over:
        # Display the game over message
        game_over_message(game_over)
        # Reset the game
        game_over, grid, turn = initialize_game()

    # Update the display
    pygame.display.flip()

# Quit PyGame
pygame.quit()
