"""Configuration constants for Checkers game."""

from .types_game import Piece, Player

# Board dimensions
BOARD_SIZE = 8

# Player colors
RED = "red"
WHITE = "white"

# Empty square representation
EMPTY = None

# Initial board setup - positions where pieces start
# Red pieces at top rows (0-2), White pieces at bottom rows (5-7)
INITIAL_RED_POSITIONS = [
    (0, 1), (0, 3), (0, 5), (0, 7),
    (1, 0), (1, 2), (1, 4), (1, 6),
    (2, 1), (2, 3), (2, 5), (2, 7),
]

INITIAL_WHITE_POSITIONS = [
    (5, 0), (5, 2), (5, 4), (5, 6),
    (6, 1), (6, 3), (6, 5), (6, 7),
    (7, 0), (7, 2), (7, 4), (7, 6),
]

# Create initial players
PLAYER_RED = Player(color=RED, name="Red")
PLAYER_WHITE = Player(color=WHITE, name="White")
