import numpy as np
import random
from tqdm import tqdm

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)  # Initialize a 3x3 board with zeros
        self.current_winner = None  # Keep track of the winner

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)  # Reset the board to zeros
        self.current_winner = None

    def make_move(self, row, col, player):
        if self.board[row, col] == 0:
            self.board[row, col] = player
            if self.check_winner(row, col, player):
                self.current_winner = player
            return True
        return False

    def check_winner(self, row, col, player):
        # Check row
        if np.all(self.board[row, :] == player):
            return True
        # Check column
        if np.all(self.board[:, col] == player):
            return True
        # Check diagonals
        if row == col and np.all(np.diag(self.board) == player):
            return True
        if row + col == 2 and np.all(np.diag(np.fliplr(self.board)) == player):
            return True
        return False
    
    def is_full(self):
        return np.all(self.board != 0)
    
    def get_available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r, c] == 0]
    
    def get_state(self):
        return self.board.copy()


# Q-Learning Agent
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, letter='O'):
        self.name = "Q-Learning Agent"
        self.q_table = {}  # (state, action) -> Q-value
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration-exploitation trade-off
        self.letter = letter
        self.opponent_letter = 'X' if self.letter == 'O' else 'O'
    
    def get_q_value(self, state, action):
        return self.q_table.get((tuple(state.flatten()), action), 0.0)
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.get_available_moves(state))
        else:
            q_values = [self.get_q_value(state, action) for action in self.get_available_moves(state)]
            max_q_value = max(q_values)
            best_actions = [action for action, q_value in zip(self.get_available_moves(state), q_values) if q_value == max_q_value]
            return random.choice(best_actions) if best_actions else None
        
    def update_q_value(self, state, action, reward, next_state):
        next_q_values = [self.get_q_value(next_state, next_action) for next_action in self.get_available_moves(next_state)]
        max_next_q_value = max(next_q_values) if next_q_values else 0.0
        current_q_value = self.get_q_value(state, action)
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * max_next_q_value - current_q_value)
        self.q_table[(tuple(state.flatten()), action)] = new_q_value

    def get_available_moves(self, state):
        return [(r, c) for r in range(3) for c in range(3) if state[r, c] == 0]
    
# Training the Q-Learning Agent
def train_agent(episodes=1000000):
    agent = QLearningAgent()
    env = TicTacToe()
    for episode in tqdm(range(episodes)):
        env.reset()
        state = env.get_state()
        done = False
        while not done:
            action = agent.choose_action(state)
            reward = 0
            if env.make_move(action[0], action[1], 1 if agent.letter == 'O' else -1):
                reward = 1 if env.current_winner == 1 else -1 if env.current_winner == -1 else 0
                next_state = env.get_state()
                agent.update_q_value(state, action, reward, next_state)
                state = next_state
                done = env.current_winner is not None or env.is_full()
        agent.letter = 'X' if agent.letter == 'O' else 'O'
    print("Training complete.")
    return agent

# Example usage
if __name__ == "__main__":
    trained_agent = train_agent()
    print("Training complete. Q-table size:", len(trained_agent.q_table))
    
    # save the Q-table to a file
    import pickle
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(trained_agent.q_table, f)