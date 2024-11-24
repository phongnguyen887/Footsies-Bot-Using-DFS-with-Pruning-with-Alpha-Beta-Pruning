import subprocess # This library would be used to open the game FOOTSIES.exe
import time # This would be used to delay keyboard presses and wait for the game to launch
from  # This library allows for the manipulation for processes in Windows
import keyboard # This library will allows the program to send keybaord inputs to the game



# Frame data for moves
FRAME_DATA = {
    "neutral_attack": { # this is the low kick attack, this can go into a KO attack
        "command": "Neutral + Attack",
        "startup": 5,
        "active": 2,
        "recovery": 16,
        "on_hit": -1,
        "on_block": -3,
        "on_guard_break": 18,
        "properties": "Can cancel into neutral special move by pressing attack on hit and on block",
        "KO": False # this means that this move ALONE won't KO the opponent
    },
    "forward_or_backward_attack": { # This is the knee attack, this can go into a KO attack
        "command": "Forward or Backward + Attack",
        "startup": 4,
        "active": 3,
        "recovery": 15,
        "on_hit": -1,
        "on_block": -3,
        "on_guard_break": 18,
        "properties": "Can cancel into neutral special move by pressing attack on hit and on block",
        "KO": False # this means that this move ALONE won't KO the opponent

    },
    "hold_attack_release": { # This is the high kick attack
        "command": "Hold Attack then Neutral + Release",
        "startup": 12,
        "active": 4,
        "recovery": 29,
        "on_hit": None,
        "on_block": -10,
        "on_guard_break": 3,
        "properties": None, 
        "KO": True # This move will KO the opponent
    },
    "hold_attack_direction_release": { # this is the uppercut-type move
        "command": "Hold Attack then Forward or Backward + Release",
        "startup": 3,
        "active": 6,
        "recovery": 47,
        "on_hit": None,
        "on_block": -30,
        "on_guard_break": -18,
        "properties": "1F-6F full invincibility", 
        "KO": True # this move will KO the opponent
    },
    "forward_x2": { # foward dash
        "command": "Forward x2",
        "startup": None,
        "active": None,
        "recovery": 16,
        "on_hit": None,
        "on_block": None,
        "on_guard_break": None,
        "properties": None
    },
    "backward_x2": { # back dash
        "command": "Backward x2",
        "startup": None,
        "active": None,
        "recovery": 22,
        "on_hit": None,
        "on_block": None,
        "on_guard_break": None,
        "properties": "1F-4F full invincibility"
    }
}

GAME_PATH = "C:\Users\mrale\OneDrive\Desktop\FOOTSIES_v1_5_0\FOOTSIES.exe" # For this project I'm going to assume that the game is going on desktop

# Virtual grid and character positions
GRID_SIZE = 100  # Total number of grid cells
bot_position = 20  # Initial position of the bot
opponent_position = 80  # Initial position of the opponent (CPU)

# Launch the game
def launch_game():
    subprocess.Popen(GAME_PATH, shell=True)
    time.sleep(5)  # Allow the game to load

# Calculate distance based on positions
def calculate_distance():
    global bot_position, opponent_position
    return abs(bot_position - opponent_position)

# Perform an action using the keyboard and update grid positions
def perform_action(action):
    global bot_position
    if action == 'neutral_attack':
        keyboard.press_and_release('space')  # Simulate attack key
    elif action == 'forward_or_backward_attack':
        keyboard.press_and_release('space')  # Forward/backward attacks use same button
    elif action == 'hold_attack_release':
        keyboard.press_and_release('space')  # Hold attack key
    elif action == 'hold_attack_direction_release':
        keyboard.press_and_release('space')  # Simulate uppercut key
    elif action == 'move_forward':
        keyboard.press('d')
        time.sleep(0.1)
        keyboard.release('d')
        bot_position = min(bot_position + 1, GRID_SIZE - 1)  # Update position
    elif action == 'move_backward':
        keyboard.press('a')
        time.sleep(0.1)
        keyboard.release('a')
        bot_position = max(bot_position - 1, 0)  # Update position

# Evaluate the game state
def evaluate_game_state(state):
    # Prioritize moves with potential to K.O.
    if state['distance'] < 10 and any(FRAME_DATA[move]['KO'] for move in get_possible_moves(state, 'AI')):
        return 100  # High priority for K.O. moves
    optimal_distance = 10
    distance_score = max(0, optimal_distance - abs(state['distance'] - optimal_distance))
    frame_adv_score = 10 if state['ai_frame_advantage'] else -10
    return distance_score + frame_adv_score

# Get possible moves
def get_possible_moves(state, player):
    moves = list(FRAME_DATA.keys())
    if player == 'AI' and state['distance'] < FRAME_DATA['neutral_attack']['range'] and state['opponent_move'] == 'neutral_attack':
        moves.remove('move_forward')  # Avoid moving into attack range
    return moves

# Simulate a move and return the new game state
def simulate_move(state, move):
    new_state = state.copy()
    if move in FRAME_DATA:
        move_data = FRAME_DATA[move]
        new_state['distance'] = max(0, state['distance'] - move_data.get('range', 0))
        new_state['ai_frame_advantage'] = move_data.get('on_hit', 0) >= 0
    return new_state

# Minimax with alpha-beta pruning
def minimax_alpha_beta(state, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_game_state(state)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(state, 'AI'):
            new_state = simulate_move(state, move)
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(state, 'Opponent'):
            new_state = simulate_move(state, move)
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Main loop
def main():
    global bot_position, opponent_position
    launch_game()

    while True:
        # Calculate distance and construct the game state
        distance = calculate_distance()
        game_state = {
            'distance': distance,
            'ai_frame_advantage': True,  # Assume AI starts with frame advantage
            'opponent_move': 'idle',  # Replace with actual detection if possible
        }

        # Determine the best move using Minimax
        best_move = None
        best_score = float('-inf')
        for move in get_possible_moves(game_state, 'AI'):
            new_state = simulate_move(game_state, move)
            score = minimax_alpha_beta(new_state, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
            if score > best_score:
                best_score = score
                best_move = move

        # Perform the best move
        if best_move:
            perform_action(best_move)

        # Assume opponent's movement is controlled by the game
        time.sleep(0.05)

if __name__ == "__main__":
    main()