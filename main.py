import subprocess # This library would be used to open the game FOOTSIES.exe
import time # This would be used to delay keyboard presses and wait for the game to launch
from pymem  import Pymem # This library allows for the manipulation for processes in Windows
import keyboard # This library will allows the program to send keybaord inputs to the game
# We can use these two libraries to force the installation of the necessary libraries
import os
import sys


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




GAME_PATH = "[GAME PATH GOES HERE]" # For this project I'm going to assume that the game is going on desktop

# Below are going to be addresses for getting the distances of the Player 1 (bot) and Player 2 (CPU or Human)
P1_X_ADDRESS = 0 # Replace with real base memory addresses
P2_X_ADDRESS = 0 #  ''                                      ''

def get_distances(): # Using the memory addresses, we can then calculate the distances 
    pass

