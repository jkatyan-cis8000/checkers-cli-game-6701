# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types.py: Type definitions for Piece (color, is_king), Player (color, name), Move (start, end, is_capture, captured_square)
- src/config.py: Constants - BOARD_SIZE=8, PLAYER1, PLAYER2, EMPTY, piece colors
- src/service/game.py: Game class with board state, valid move generation, apply_move, check_winner, kinging logic
- src/service/validator.py: Move validation - checks if moves follow Checkers rules (diagonal moves, capture mechanics, king movement)
- src/ui/cli.py: CLI rendering (8x8 board with pieces), move input parsing (e.g., "e6f5"), game loop
- src/runtime/main.py: Entry point, creates game, runs UI loop
- src/utils.py: Helper functions (parse_position notation like "e6" to (row,col))

## Interfaces

### Types exposed:
- Piece(color: str, is_king: bool)
- Player(color: str, name: str)
- Move(start: tuple, end: tuple, is_capture: bool = False, captured_square: tuple | None = None)
- BoardState(grid: list[list[Piece | None]])

### Game service:
- Game.move(piece_pos, target_pos) -> Move | None: Validates and applies move, returns Move or None if invalid
- Game.get_valid_moves(player) -> list[Move]: Returns all valid moves for a player
- Game.check_winner() -> str | None: Returns winner color or None if game ongoing
- Game.is_valid_position(row, col) -> bool
- Game.get_piece(row, col) -> Piece | None

### UI:
- display_board(board: BoardState) -> None
- parse_move_input(input_str: str) -> tuple[tuple[int,int], tuple[int,int]] | None
- get_player_input() -> str

## Shared Data Structures

```python
# Piece representation
class Piece:
    color: str  # "red" or "white"
    is_king: bool

# Move representation
class Move:
    start: tuple[int, int]  # (row, col)
    end: tuple[int, int]    # (row, col)
    is_capture: bool
    captured_square: tuple[int, int] | None

# Board state
BoardState = list[list[Piece | None]]  # 8x8 grid
```

## External Dependencies

- None required - pure Python standard library implementation
