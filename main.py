from pynput.keyboard import Key, Controller, Listener as KeyboardListener
import win32com.client
import subprocess
import random
import time

# Initialize the keyboard controller
keyboard = Controller()

# Key mappings for keyboard input simulation
KEY_MAPPING = {
    "a": "a",         # Move left
    "d": "d",         # Move right
    "space": Key.space  # Attack
}

# Frame data for moves with attributes affecting decision-making
FRAME_DATA = {
    "neutral_attack": {
        "state": "idle",
        "command": "Neutral + Attack",
        "startup": 5,          # Frames before move becomes active
        "active": 2,           # Frames during which the move is active
        "recovery": 16,        # Frames before the bot can act again
        "can_cancel": True,    # Indicates if the move can cancel into another
        "KO": False,           # Whether the move can cause a KO
    },
    "forward_attack": {
        "state": "forward",
        "command": "Forward + Attack",
        "startup": 4,
        "active": 3,
        "recovery": 15,
        "can_cancel": True,
        "KO": False,
    },
    "backward_attack": {
        "state": "backward",
        "command": "Backward + Attack",
        "startup": 6,
        "active": 2,
        "recovery": 20,
        "can_cancel": True,
        "KO": False,
    },
}

# Global flags and constants
game_starting = False
KEYPRESS_DURATION = 0.1  # Duration for which keys are held down (in seconds)
ACTION_COOLDOWN = 0.2  # Minimum cooldown between actions (in seconds)
MOVEMENT_PRIORITY_INTERVAL = 1.5  # Time interval to ensure periodic movement (in seconds)

# Function to focus the game window
def focus_game_window():
    """
    Brings the game window to the foreground so that key presses are directed to it.
    """
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.AppActivate("FOOTSIES")  # Replace with your game's window title
        print("Game window focused.")
    except Exception as e:
        print(f"Failed to focus game window: {e}")

# Function to launch the game
def launch_game():
    """
    Launches the game executable using subprocess.
    """
    try:
        game_process = subprocess.Popen(r"C:\Users\mrale\OneDrive\Desktop\FOOTSIES_v1_5_0\FOOTSIES.exe", shell=True)
        if game_process is None:
            raise ValueError("Failed to start the game process.")
        print("Game launched.")
        return game_process
    except Exception as e:
        print(f"Error launching the game: {e}")
        return None

# Tree structure for Minimax decision-making
class TreeNode:
    def __init__(self, name, value=None):
        self.name = name       # Name of the move/action
        self.value = value     # Evaluated score of the move
        self.children = []     # Possible subsequent moves

    def add_child(self, child_node):
        """
        Adds a child node to the current node, representing a subsequent move.
        """
        self.children.append(child_node)

# Function to create a decision tree for attacks
def create_tree_for_attack():
    """
    Constructs a tree representing the possible sequences of attacks.
    """
    root = TreeNode("Root")

    # First level
    attack = TreeNode("neutral_attack")
    forward_attack = TreeNode("forward_attack")
    backward_attack = TreeNode("backward_attack")
    root.add_child(attack)
    root.add_child(forward_attack)
    root.add_child(backward_attack)

    # Second level for each branch
    for parent in [attack, forward_attack, backward_attack]:
        parent.add_child(TreeNode("neutral_attack"))
        parent.add_child(TreeNode("forward_attack"))
        parent.add_child(TreeNode("backward_attack"))

    return root

# Assign evaluation scores to tree nodes
def assign_tree_values(tree, move_names):
    """
    Assigns evaluation scores to leaf nodes in the tree based on move attributes.
    """
    for i, child in enumerate(tree.children):
        for j, grandchild in enumerate(child.children):
            move_name = move_names[i][j]
            grandchild.value = evaluation_function(move_name)

# Function to evaluate moves
def evaluation_function(move_name):
    """
    Calculates a score for a move based on its frame data, prioritizing aggressive moves.
    """
    move_data = FRAME_DATA[move_name]
    score = (
        (20 / (move_data["startup"] + 1)) +  # Favor faster startup
        (10 * move_data["active"]) -         # Prioritize active frames
        (move_data["recovery"] / 4)          # Reduce penalty for recovery
    )
    if move_data["can_cancel"]:
        score += 25  # Bonus for cancellable moves
    if move_data["KO"]:
        score += 30  # Bonus for KO moves
    return score

# Minimax algorithm with alpha-beta pruning
def minimax_alpha_beta(node, depth, is_maximizing, alpha, beta):
    """
    Recursive Minimax algorithm with alpha-beta pruning for optimal decision-making.
    """
    if not node.children:
        return node.value, node

    best_node = None
    if is_maximizing:
        max_eval = float('-inf')
        for child in node.children:
            eval, _ = minimax_alpha_beta(child, depth + 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_node = child
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_node
    else:
        min_eval = float('inf')
        for child in node.children:
            eval, _ = minimax_alpha_beta(child, depth + 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_node = child
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_node

# Function to perform actions
def perform_action(action):
    """
    Executes the specified action by simulating key presses.
    """
    focus_game_window()
    if action == 'neutral_attack':
        keyboard.press(KEY_MAPPING["space"])
        time.sleep(KEYPRESS_DURATION)
        keyboard.release(KEY_MAPPING["space"])
        print("Performed neutral attack.")
    elif action == 'forward_attack':
        keyboard.press(KEY_MAPPING["d"])
        keyboard.press(KEY_MAPPING["space"])
        time.sleep(KEYPRESS_DURATION)
        keyboard.release(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["d"])
        print("Performed forward attack.")
    elif action == 'backward_attack':
        keyboard.press(KEY_MAPPING["a"])
        keyboard.press(KEY_MAPPING["space"])
        time.sleep(KEYPRESS_DURATION)
        keyboard.release(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["a"])
        print("Performed backward attack.")
    elif action == 'move_left':
        keyboard.press(KEY_MAPPING["a"])
        time.sleep(KEYPRESS_DURATION)
        keyboard.release(KEY_MAPPING["a"])
        print("Moved left.")
    elif action == 'move_right':
        keyboard.press(KEY_MAPPING["d"])
        time.sleep(KEYPRESS_DURATION)
        keyboard.release(KEY_MAPPING["d"])
        print("Moved right.")
    else:
        print(f"Unknown action: {action}")

# Start game on Enter key press
def on_key_press(key):
    """
    Starts the bot when the Enter key is pressed.
    """
    global game_starting
    if key == Key.enter:
        game_starting = True
        print("Game starting...")
        return False

# Decision tree initialization
move_names = [
    ["neutral_attack", "forward_attack", "backward_attack"],
    ["forward_attack", "neutral_attack", "backward_attack"],
    ["backward_attack", "neutral_attack", "forward_attack"],
]
tree = create_tree_for_attack()
assign_tree_values(tree, move_names)

# Main loop
def main():
    global game_starting

    game_process = launch_game()
    if not game_process:
        print("Failed to launch the game. Exiting.")
        return

    print("Press Enter to start the bot...")
    with KeyboardListener(on_press=on_key_press) as listener:
        listener.join()

    last_action_time = 0
    last_movement_time = 0

    try:
        while True:
            if game_process.poll() is not None:
                print("Game has exited. Shutting down the bot...")
                break

            current_time = time.time()

            # Ensure periodic movement
            if current_time - last_movement_time >= MOVEMENT_PRIORITY_INTERVAL:
                selected_move = random.choice(["move_left", "move_right"])
                print(f"Prioritized movement: {selected_move}")
                perform_action(selected_move)
                last_movement_time = current_time
                continue

            # Regular decision-making with cooldown
            if current_time - last_action_time >= ACTION_COOLDOWN:
                if random.random() < 0.10:  # 10% chance for random movement
                    selected_move = random.choice(["move_left", "move_right"])
                    print(f"Random movement: {selected_move}")
                else:  # 90% aggressive strategy
                    optimize_value, best_node = minimax_alpha_beta(tree, depth=0, is_maximizing=True, alpha=float('-inf'), beta=float('inf'))
                    selected_move = best_node.name
                    print(f"Optimized value: {optimize_value}, Best move: {selected_move}")

                perform_action(selected_move)
                last_action_time = current_time

    except KeyboardInterrupt:
        print("Exiting due to user interruption.")
    finally:
        if game_process.poll() is None:
            game_process.terminate()
        print("Bot terminated.")

if __name__ == "__main__":
    main()
