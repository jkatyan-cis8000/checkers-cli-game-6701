"""CLI user interface for Checkers game."""

import sys
from ..types_game import BoardState, Piece
from ..config import BOARD_SIZE, RED, WHITE
from ..service.game import Game


def display_board(board: BoardState) -> None:
    """Display the game board."""
    # Column headers
    print("  a b c d e f g h")
    
    for row in range(BOARD_SIZE):
        # Row number
        print(f"{BOARD_SIZE - row} ", end="")
        
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece is None:
                # Empty square - alternating pattern
                if (row + col) % 2 == 0:
                    print(". ", end="")  # Dark square
                else:
                    print("  ", end="")  # Light square (blank)
            else:
                # Piece
                symbol = "R" if piece.color == RED else "W"
                if piece.is_king:
                    symbol = symbol.lower()
                print(f"{symbol} ", end="")
        print(f"{BOARD_SIZE - row}")
    
    # Column headers
    print("  a b c d e f g h")
    print()


def parse_position(pos_str: str) -> tuple[int, int] | None:
    """Parse position string like 'e6' into (row, col) tuple."""
    if len(pos_str) != 2:
        return None
    
    col_char, row_char = pos_str.lower()
    
    if col_char not in 'abcdefgh':
        return None
    
    try:
        row = int(row_char)
    except ValueError:
        return None
    
    # Convert to 0-indexed: row 8 -> 0, row 1 -> 7
    if row < 1 or row > 8:
        return None
    
    col = ord(col_char) - ord('a')
    row = 8 - row
    
    return (row, col)


def get_move(game: Game, player: str) -> tuple[tuple[int, int], tuple[int, int]] | None:
    """Get a valid move from the user."""
    valid_moves = game.get_all_valid_moves(player)
    
    if not valid_moves:
        return None
    
    while True:
        print(f"Current player: {'Red' if player == RED else 'White'}")
        print("Enter move (e.g., 'e6f5') or 'q' to quit:")
        
        try:
            user_input = input().strip()
        except EOFError:
            return None
        
        if user_input.lower() == 'q':
            return None
        
        if len(user_input) != 4:
            print("Invalid format. Use 'fromto' (e.g., 'e6f5')")
            continue
        
        start_pos = parse_position(user_input[:2])
        end_pos = parse_position(user_input[2:])
        
        if start_pos is None or end_pos is None:
            print("Invalid position format. Use letters a-h and numbers 1-8")
            continue
        
        return (start_pos, end_pos)


def run_ui() -> None:
    """Run the CLI game interface."""
    game = Game()
    
    print("Welcome to Checkers!")
    print("Enter moves in from-to format (e.g., 'e6f5')")
    print()
    
    while True:
        display_board(game.board)
        
        winner = game.check_winner()
        if winner is not None:
            print(f"{'Red' if winner == RED else 'White'} wins!")
            break
        
        move_input = get_move(game, game.current_player)
        
        if move_input is None:
            print("Game ended.")
            break
        
        start, end = move_input
        move = game.get_valid_moves(game.current_player, start[0], start[1])
        
        # Find the matching move
        selected_move = None
        for m in move:
            if m.start == start and m.end == end:
                selected_move = m
                break
        
        if selected_move is None:
            print("Invalid move!")
            continue
        
        game.apply_move(selected_move)
        print()


if __name__ == "__main__":
    run_ui()
