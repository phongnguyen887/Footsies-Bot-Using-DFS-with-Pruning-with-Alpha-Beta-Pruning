from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key, Controller
import win32gui
import win32com.client
import subprocess
import random

# Initialize thae keyboard controller
keyboard = Controller()

# Key mappings
KEY_MAPPING = {
    "a": "a",         # Move left
    "d": "d",         # Move right
    "space": Key.space  # Attack
}

# Frame data for moves
FRAME_DATA = {
    "neutral_attack": {
        "state": "idle",
        "command": "Neutral + Attack",
        "startup": 5,
        "active": 2,
        "recovery": 16,
        "can_cancel": True,  # Can cancel into another move
        "KO": False,
    },
    "move_left": {
        "state": "moving",
        "command": "Move Left",
        "startup": 0,
        "active": 0,
        "recovery": 0,
        "can_cancel": False,
        "KO": False,
    },
    "move_right": {
        "state": "moving",
        "command": "Move Right",
        "startup": 0,
        "active": 0,
        "recovery": 0,
        "can_cancel": False,
        "KO": False,
    },
    "forward_attack": {
        "state": "forward",
        "command": "Forward + Attack",
        "startup": 4,
        "active": 3,
        "recovery": 15,
        "can_cancel": True,  # Can cancel into another move
        "KO": False,
    },
    "backward_attack": {
        "state": "backward",
        "command": "Backward + Attack",
        "startup": 6,
        "active": 2,
        "recovery": 20,
        "can_cancel": True,  # Can cancel into another move
        "KO": False,
    },
}

game_starting = 'False'

# Focus the game window
def focus_game_window():
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.AppActivate("FOOTSIES")  # Replace with your game's window title
        print("Game window focused.")
    except Exception as e:
        print(f"Failed to focus game window: {e}")


# Launch the game
def launch_game():
    try:
        game_process = subprocess.Popen(r"GAME_PATH", shell=True)
        if game_process is None:
            raise ValueError("Failed to start the game process.")
        print("Game launched.")
        return game_process
    except Exception as e:
        print(f"Error launching the game: {e}")
        return None


def evaluation_function():
    pass

def build_tree():
    pass

def minimax_alpha_beta():
    pass

# Perform an action using `pynput`
def perform_action(action):
    focus_game_window()  # Ensure the game is focused before sending input
    if action == 'neutral_attack':
        keyboard.press(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["space"])
        print("Pressed 'space' - Performed neutral attack")
    elif action == 'move_right':
        keyboard.press(KEY_MAPPING["d"])
        keyboard.release(KEY_MAPPING["d"])
        print("Pressed 'd' - Moved right")
    elif action == 'move_left':
        keyboard.press(KEY_MAPPING["a"])
        keyboard.release(KEY_MAPPING["a"])
        print("Pressed 'a' - Moved left")
    elif action == 'forward_attack':
        keyboard.press(KEY_MAPPING["d"])
        keyboard.press(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["space"])
        if FRAME_DATA["forward_attack"]["can_cancel"]:
            keyboard.press(KEY_MAPPING["space"])  # Perform cancel attack
            keyboard.release(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["d"])
        print("Pressed 'd' and 'space' twice - Performed forward attack combo")
    elif action == 'backward_attack':
        keyboard.press(KEY_MAPPING["a"])
        keyboard.press(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["space"])
        if FRAME_DATA["backward_attack"]["can_cancel"]:
            keyboard.press(KEY_MAPPING["space"])  # Perform cancel attack
            keyboard.release(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["a"])
        print("Pressed 'a' and 'space' twice - Performed backward attack combo")
    else:
        print(f"Unknown action: {action}")


# Get possible moves based on the bot's movement state
def get_possible_moves(movement_state):
    if movement_state == 'idle':
        return ["neutral_attack", "move_left", "move_right"]
    return ["forward_attack", "backward_attack", "move_left", "move_right"]

click_count = 0
def on_click(x, y, button, pressed):
    global game_starting
    global click_count
    if pressed:  # Mouse clicked
        click_count += 1
        print(f"Mouse clicked at ({x}, {y}). Starting the game...")
        if click_count >= 2:
            game_starting = True
            return False 

# Main loop
def main():
    # Launch the game and start the bot immediately
    game_process = launch_game()
    if not game_process:
        print("Failed to launch the game. Exiting.")
        return
    
    print("Waiting for mouse click to start the game...")
    with MouseListener(on_click=on_click) as listener:
        listener.join()  # Wait until the listener stops

    movement_state = 'idle'
    
    try:
        while True:
            # Check if the game has exited
            if game_process.poll() is not None:
                print("Game has exited. Shutting down the bot...")
                break
              
            # Get possible moves
            possible_moves = get_possible_moves(movement_state)

            # Randomize move selection
            selected_move = random.choice(possible_moves)

            # Perform the selected move
            perform_action(selected_move)

            # Update movement state for next iteration
            if selected_move in ["move_left", "move_right"]:
                movement_state = "moving"
            else:
                movement_state = "idle"

    except KeyboardInterrupt:
        print("Exiting due to user interruption.")
    finally:
        if game_process.poll() is None:
            game_process.terminate()
        print("Bot and game process terminated.")


if __name__ == "__main__":
    main()
