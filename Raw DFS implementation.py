from pynput.keyboard import Key, Controller, Listener as KeyboardListener
import win32com.client
import subprocess
import time

# Initialize the keyboard controller
keyboard = Controller()

# Key mappings for keyboard input simulation
KEY_MAPPING = {
    "a": "a",         # Move left
    "d": "d",         # Move right
    "space": Key.space  # Attack
}

# Move definitions (no evaluation or additional metadata)
MOVES = [
    "neutral_attack",
    "forward_attack",
    "backward_attack",
    "move_left",
    "move_right",
]

# Global flags and constants
game_starting = False
KEYPRESS_DURATION = 0.1  # Duration for which keys are held down (in seconds)
ACTION_COOLDOWN = 0.2  # Minimum cooldown between actions (in seconds)

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

# DFS implementation to iterate through moves
def dfs_moves(moves, depth):
    """
    Perform a raw DFS through the list of moves. Each move is executed in sequence,
    simulating depth-first exploration of all moves.
    """
    if depth == 0 or not moves:
        return

    for move in moves:
        # Perform the action corresponding to the current move
        perform_action(move)
        time.sleep(ACTION_COOLDOWN)  # Add a cooldown between actions

        # Recursively explore the same moves with one less depth
        dfs_moves(moves, depth - 1)

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

    try:
        while True:
            if game_process.poll() is not None:
                print("Game has exited. Shutting down the bot...")
                break

            print("Starting DFS on moves...")
            dfs_moves(MOVES, depth=3)  # Start DFS with the moves list and a depth of 3
            time.sleep(1)  # Wait a bit before restarting DFS

    except KeyboardInterrupt:
        print("Exiting due to user interruption.")
    finally:
        if game_process.poll() is None:
            game_process.terminate()
        print("Bot terminated.")

if __name__ == "__main__":
    main()
