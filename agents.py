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