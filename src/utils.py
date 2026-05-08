"""Utility functions for Checkers game."""

from ..types_game import BoardState, Piece


def count_pieces(board: BoardState, color: str) -> int:
    """Count pieces of a given color on the board."""
    count = 0
    for row in board:
        for piece in row:
            if piece is not None and piece.color == color:
                count += 1
    return count


def is_valid_position(row: int, col: int, size: int = 8) -> bool:
    """Check if position is within board bounds."""
    return 0 <= row < size and 0 <= col < size
