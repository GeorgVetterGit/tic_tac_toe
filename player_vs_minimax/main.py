# /// script
# dependencies = [
# "pygame-ce",
# "pickle",
# "numpy",
# ]
# ///

import pygame
import pickle
import numpy as np
import random
import asyncio

# Initialize PyGame
pygame.init()

clock = pygame.time.Clock()

# Set screen dimensions
screen_width = 400
menu_height = 100
screen_height = screen_width + menu_height
screen = pygame.display.set_mode((screen_width, screen_height))

#icon = pygame.image.load('/Users/georg/Projects/Tiny Games in Python/tic_tac_toe/tic_tac_toe/icon.png')
#pygame.display.set_icon(icon)  # Set the icon for the window

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

class q_learning_agent:
    def __init__(self):
        self.name = "Q-Learning Agent"
        with open('q_table.pkl', 'rb') as f:
            loaded_q_table = pickle.load(f)
        self.q_table = loaded_q_table  # Load the Q-table into the agent
    
    def get_move(self, game_state:list[list[str]]) -> tuple[int, int]:
        """Uses the Q-table to determine the best move for the agent.

        Args:
            game_state (list): A 3x3 list representing the current state of the game, where each element can be 'X', 'O', or None.
        Returns:
            tuple: A tuple (row, col) representing the chosen move, where row and col are indices of the grid.
        Raises:
            ValueError: If there are no available moves left in the game state.
        """
        
        available_moves = [(i, j) for i in range(3) for j in range(3) if game_state[i][j] is None]
        if not available_moves:
            raise ValueError("No available moves left")
        
        # Convert the game state to a tuple for hashing
        # This is necessary because lists are not hashable in Python

        # transform string entries in game_state to int. X = 1, O = -1, None = 0
        game_state = [[np.int64(1) if cell == 'X' else np.int64(-1) if cell == 'O' else np.int64(0) for cell in row] for row in game_state]

        state = tuple(tuple(row) for row in game_state)
        q_values = [self.q_table.get((state, move), 0.0) for move in available_moves]
        max_q_value = max(q_values)
        best_moves = [move for move, q_value in zip(available_moves, q_values) if q_value == max_q_value]
        
        return random.choice(best_moves) if best_moves else None

agent = q_learning_agent()  # Initialize the agent
game_over, grid, turn = initialize_game()  # Initialize the game
cool_down_time = 3  # Cool down time in seconds
start_wait = False  # Flag to indicate if we are waiting for the game to reset

def game_over_message(winner):
    """Display the game over message."""

    # rectangle behind game over message
    pygame.draw.rect(screen, COLORS['BLACK'], (38, screen_height // 2 - 32, screen_width - 76, menu_height + 4))

    # rectangle behind game over message
    pygame.draw.rect(screen, COLORS['BACKGROUND'], (40, screen_height // 2 - 30, screen_width - 80, menu_height))

    font = pygame.font.Font(None, 36)
    text = font.render(f"{winner} wins!", True, COLORS['RED'])
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    # write time till game reset is 3 seconds
    font = pygame.font.Font(None, 24)
    text = font.render("Resetting in 3 seconds...", True, COLORS['TEXT_COLOR'])
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
    screen.blit(text, text_rect)
    # update the display
    pygame.display.flip()

async def main():
    global game_over, grid, turn, agent, screen, screen_width, screen_height, menu_height, COLORS, cool_down_time, start_wait
    # Game loop
    running = True
    while running:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 'X':
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
            start_wait = True
        
        # Check for a draw
        if all(cell is not None for row in grid for cell in row):
            game_over = 'Nobody'
            start_wait = True

        if any(all(cell == 'O' for cell in row) for row in grid) or \
        any(all(grid[y][x] == 'O' for y in range(3)) for x in range(3)) or \
        all(grid[i][i] == 'O' for i in range(3)) or \
        all(grid[i][2 - i] == 'O' for i in range(3)):
            game_over = 'Agent O'
            start_wait = True

        # If the game is over, wait for a few seconds before resetting
        if start_wait:
            end_tick = pygame.time.get_ticks() + cool_down_time * 1000
            start_wait = False

        # Fill the background
        screen.fill(COLORS['BACKGROUND'])  # Black color

        # Draw the menu
        pygame.draw.rect(screen, COLORS['MENU'], (0, 0, screen_width, menu_height))
        font = pygame.font.Font(None, 25)
        text = font.render(f"Tic Tac Toe - Player X vs {agent.name} O", True, COLORS['TEXT_COLOR'])
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
        
        if game_over:
            # Display the game over message
            game_over_message(game_over)
            # Wait for the cool down time
            while pygame.time.get_ticks() < end_tick:
                await asyncio.sleep(0)
            # Reset the game
            game_over, grid, turn = initialize_game()

        # Update the display
        pygame.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())
