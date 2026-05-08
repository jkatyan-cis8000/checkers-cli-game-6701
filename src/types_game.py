"""Type definitions for Checkers game."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Piece:
    """Represents a game piece."""
    color: str  # "red" or "white"
    is_king: bool = False


@dataclass(frozen=True)
class Player:
    """Represents a player."""
    color: str  # "red" or "white"
    name: str


@dataclass(frozen=True)
class Move:
    """Represents a move from start to end position."""
    start: tuple[int, int]  # (row, col)
    end: tuple[int, int]    # (row, col)
    is_capture: bool = False
    captured_square: Optional[tuple[int, int]] = None


# Board is represented as 8x8 grid of Optional[Piece]
# None represents an empty square
BoardState = list[list[Optional[Piece]]]
