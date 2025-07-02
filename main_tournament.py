import pygame
import agents
import numpy as np

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
          'BLUE': (0, 0, 255),
          'BACKGROUND': (32, 32, 32),
          'MENU': (18, 18, 18),
          'X_COLOR': (220, 120, 120),
          'O_COLOR': (120, 160, 220),
          'LINE_COLOR': (6, 64, 64),
          'TEXT_COLOR': (229, 229, 229)}  


def initialize_game():
    """Reset the game grid and turn."""
    global grid, turn, agent
    grid = [[None for _ in range(3)] for _ in range(3)]

    if np.random.rand() < 0.5:
        turn = 'O'
        agent = agent_o
    else:
        turn = 'X'
        agent = agent_x
    return 0

game_history = []  # To keep track of the game history
game_count = 0  # To count the number of games played

agent_x = agents.random_agent()  # Initialize the agent for 'X'
agent_o = agents.random_agent()  # Initialize the agent for 'O'

rounds = initialize_game()  # Initialize the game
init_turn = turn  # Store the initial turn

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
    if turn == 'O':
        # Get the agent's move
        try:
            move = agent.get_move(grid)
            cell_x, cell_y = move
            # Check if the cell is already occupied
            if grid[cell_x][cell_y] is None:
                # Mark the cell with 'O'
                grid[cell_x][cell_y] = 'O'
                # Switch turn to 'X'
                turn = 'X'
                agent = agent_x  # Switch to the agent for 'X'
        except ValueError:
            print("No available moves left for the agent.")
            running = False
    elif turn == 'X':
        # Get the agent's move
        try:
            move = agent.get_move(grid)
            cell_x, cell_y = move
            # Check if the cell is already occupied
            if grid[cell_x][cell_y] is None:
                # Mark the cell with 'X'
                grid[cell_x][cell_y] = 'X'
                # Switch turn to 'O'
                turn = 'O'
                agent = agent_o  # Switch to the agent for 'O'
        except ValueError:
            print("No available moves left for the agent.")
            running = False

    # Check if the game should end
    if any(all(cell == 'X' for cell in row) for row in grid) or \
       any(all(grid[y][x] == 'X' for y in range(3)) for x in range(3)) or \
       all(grid[i][i] == 'X' for i in range(3)) or \
       all(grid[i][2 - i] == 'X' for i in range(3)):
        print(f"{agent_x.name} X wins!")
        game_history.append((game_count, rounds, init_turn, agent_x.name, 'X'))  # Record the game result
        rounds = initialize_game()  # Reset the game
        init_turn = turn  # Store the initial turn
        game_count += 1

    
    # Check for a draw
    if all(cell is not None for row in grid for cell in row):
        print("It's a draw!")
        game_history.append((game_count, rounds, init_turn, None, 'Draw'))  # Record the game result
        rounds = initialize_game()  # Reset the game
        init_turn = turn  # Store the initial turn
        game_count += 1


    if any(all(cell == 'O' for cell in row) for row in grid) or \
       any(all(grid[y][x] == 'O' for y in range(3)) for x in range(3)) or \
       all(grid[i][i] == 'O' for i in range(3)) or \
       all(grid[i][2 - i] == 'O' for i in range(3)):
        print(f"{agent_o.name} O wins!")
        game_history.append((game_count, rounds, init_turn, agent_o.name, 'O'))  # Record the game result
        rounds = initialize_game()  # Reset the game
        init_turn = turn  # Store the initial turn
        game_count += 1

    
    rounds += 1

    if game_count >= 10000:  # Limit the number of games to 100
        print("Reached the maximum number of games.")
        running = False

    # Fill the background
    screen.fill(COLORS['BACKGROUND'])  # Black color

    # Draw the menu
    pygame.draw.rect(screen, COLORS['MENU'], (0, 0, screen_width, menu_height))
    font = pygame.font.Font(None, 20)
    text = font.render(f"Tic Tac Toe - {agent_x.name} X vs {agent_o.name} O", True, COLORS['TEXT_COLOR'])
    text_rect = text.get_rect(center=(screen_width // 2, menu_height // 2))
    screen.blit(text, text_rect)

    # Draw the grid
    for x in range(1, 3):
        pygame.draw.line(screen, COLORS['LINE_COLOR'], (x * screen_width // 3, menu_height), (x * screen_width // 3, screen_height), 2)
    for y in range(1, 3):
        pygame.draw.line(screen, COLORS['LINE_COLOR'], (0, y * screen_width // 3 + menu_height), (screen_width, y * screen_width // 3 + menu_height), 2)   
    
    # Draw the grid cells
    for y in range(3):
        for x in range(3):
            if grid[y][x] == 'X':
                pygame.draw.line(screen, COLORS['X_COLOR'], 
                                 (x * screen_width // 3 + 10, 
                                  y * screen_width // 3 + menu_height + 10), 
                                 (x * screen_width // 3 + screen_width // 3 - 10, 
                                  y * screen_width // 3 + menu_height + screen_width // 3 - 10), 
                                 15)
                pygame.draw.line(screen, COLORS['X_COLOR'], 
                                 (x * screen_width // 3 + screen_width // 3 - 10, 
                                  y * screen_width // 3 + menu_height + 10), 
                                 (x * screen_width // 3 + 10, 
                                  y * screen_width // 3 + menu_height + screen_width // 3 - 10), 
                                 15)
    for y in range(3):
        for x in range(3):
            if grid[y][x] == 'O':
                pygame.draw.circle(screen, COLORS['O_COLOR'], 
                                   (x * screen_width // 3 + screen_width // 6, 
                                    y * screen_width // 3 + menu_height + screen_width // 6), 
                                   screen_width // 6 - 10, 
                                   15)

    # Update the display
    pygame.display.flip()

with open(f'/Users/georg/Projects/Tiny Games in Python/tic_tac_toe/tic_tac_toe/results/{agent_x.name}_vs_{agent_o.name}.txt', 'w') as f:
    for game in game_history:
        f.write(f"{game[0]}, {game[1]}, {game[2]}, {game[3]}, {game[4]}\n")

# Quit PyGame
pygame.quit()
