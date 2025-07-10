# /// script
# dependencies = [
# "pygame-ce",
# "numpy",
# ]
# ///

import asyncio
import pygame
import numpy as np

# Initialize PyGame
pygame.init()

clock = pygame.time.Clock()

# Set screen dimensions
SCREEN_WIDTH = 400
MENU_HEIGHT = 100
SCREEN_HEIGHT = SCREEN_WIDTH + MENU_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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

class MinimaxAgent:
    """Minimax Agent for Tic Tac Toe game."""
    def __init__(self, letter='O'):
        self.name = "Minimax Agent"
        self.letter = letter  # 'O' for the agent, 'X' for the opponent
        
    def get_move(self, game_state:list[list[str]]) -> tuple[int, int]:
        """Uses the minimax algorithm to determine the best move for the agent.

        Args:
            game_state (list): A 3x3 list representing the current state of the game, where each element can be 'X', 'O', or None.
        Returns:
            tuple: A tuple (row, col) representing the chosen move, where row and col are indices of the grid.
        Raises:
            ValueError: If there are no available moves left in the game state.
        """
        
        def minimax(state, depth, is_maximizing):
            """Minimax algorithm to evaluate the best move for the agent.
            Args:
                state (list): The current state of the game.
                depth (int): The current depth of the search tree.
                is_maximizing (bool): True if the current player is the maximizing player (the agent), False otherwise.
            Returns:
                int: The score of the current state.
            """
            if self.letter == 'O':
                scores = {'X': -1, 'O': 1, 'draw': 0}
            else:
                scores = {'X': 1, 'O': -1, 'draw': 0}

            winner = check_winner(state)
            if winner:
                return scores[winner]
            if all(cell is not None for row in state for cell in row):
                return scores['draw']

            if is_maximizing:
                best_score = float('-inf')
                for i in range(3):
                    for j in range(3):
                        if state[i][j] is None:
                            state[i][j] = self.letter
                            score = minimax(state, depth + 1, False)
                            state[i][j] = None
                            best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(3):
                    for j in range(3):
                        if state[i][j] is None:
                            state[i][j] = 'X' if self.letter == 'O' else 'O'
                            score = minimax(state, depth + 1, True)
                            state[i][j] = None
                            best_score = min(score, best_score)
                return best_score

        def check_winner(state):
            # Check rows and columns
            for i in range(3):
                if state[i][0] == state[i][1] == state[i][2] and state[i][0] is not None:
                    return state[i][0]
                if state[0][i] == state[1][i] == state[2][i] and state[0][i] is not None:
                    return state[0][i]
            # Check diagonals
            if state[0][0] == state[1][1] == state[2][2] and state[0][0] is not None:
                return state[0][0]
            if state[0][2] == state[1][1] == state[2][0] and state[0][2] is not None:
                return state[0][2]
            return None

        available_moves = [(i, j) for i in range(3) for j in range(3) if game_state[i][j] is None]
        if not available_moves:
            raise ValueError("No available moves left")
        best_move = None
        best_score = float('-inf')
        for move in available_moves:
            i, j = move
            game_state[i][j] = self.letter
            score = minimax(game_state, 0, False)
            game_state[i][j] = None
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

agent = MinimaxAgent()  # Initialize the agent
game_over, grid, turn = initialize_game()  # Initialize the game
COOL_DOWN_TIME = 3  # Cool down time in seconds
start_wait = False  # Flag to indicate if we are waiting for the game to reset

def game_over_message(winner):
    """Display the game over message."""

    # rectangle behind game over message
    pygame.draw.rect(screen, COLORS['BLACK'], (38, SCREEN_HEIGHT // 2 - 32, SCREEN_WIDTH - 76, MENU_HEIGHT + 4))

    # rectangle behind game over message
    pygame.draw.rect(screen, COLORS['BACKGROUND'], (40, SCREEN_HEIGHT // 2 - 30, SCREEN_WIDTH - 80, MENU_HEIGHT))

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

async def main():
    global game_over, grid, turn, agent, screen, SCREEN_WIDTH, SCREEN_HEIGHT, MENU_HEIGHT, COLORS, COOL_DOWN_TIME, start_wait
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
            end_tick = pygame.time.get_ticks() + COOL_DOWN_TIME * 1000
            start_wait = False

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
            # Wait for the cool down time
            while pygame.time.get_ticks() < end_tick:
                await asyncio.sleep(0)
            # Reset the game
            game_over, grid, turn = initialize_game()

        # Update the display
        pygame.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())
