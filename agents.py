import random

class random_agent:
    def __init__(self):
        self.name = "Random Agent"

    def get_move(self, game_state:list[list[str]]) -> tuple[int, int]:
        """generates random move for the agent by choosing a free field of the 3x3 tic-tac-toe grid.

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
        return random.choice(available_moves)

class minimax_agent:
    def __init__(self):
        self.name = "Minimax Agent"
        
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
            scores = {'X': -1, 'O': 1, 'draw': 0}
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
                            state[i][j] = 'O'
                            score = minimax(state, depth + 1, False)
                            state[i][j] = None
                            best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(3):
                    for j in range(3):
                        if state[i][j] is None:
                            state[i][j] = 'X'
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
            game_state[i][j] = 'O'
            score = minimax(game_state, 0, False)
            game_state[i][j] = None
            if score > best_score:
                best_score = score
                best_move = move
        return best_move