"""Validation functions for Checkers moves."""

from ..service.game import Game
from ..types_game import Move


def validate_move(game: Game, start: tuple[int, int], end: tuple[int, int]) -> Move | None:
    """Validate a move and return Move object if valid."""
    valid_moves = game.get_valid_moves(game.current_player, start[0], start[1])
    
    # Find matching move
    for move in valid_moves:
        if move.start == start and move.end == end:
            return move
    
    return None
