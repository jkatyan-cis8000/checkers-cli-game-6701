"""Game service for Checkers - core business logic."""

from ..types_game import Piece, Move, BoardState, Player
from ..config import BOARD_SIZE, EMPTY, RED, WHITE


class Game:
    """Manages Checkers game state and rules."""
    
    def __init__(self):
        """Initialize a new game with standard starting position."""
        self.board: BoardState = self._create_initial_board()
        self.current_player = RED
        self.red_pieces_remaining = 12
        self.white_pieces_remaining = 12
    
    def _create_initial_board(self) -> BoardState:
        """Create 8x8 board with initial piece placement."""
        board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        # Place red pieces (top rows, odd columns on even rows, even columns on odd rows)
        for row, col in [(0, 1), (0, 3), (0, 5), (0, 7),
                         (1, 0), (1, 2), (1, 4), (1, 6),
                         (2, 1), (2, 3), (2, 5), (2, 7)]:
            board[row][col] = Piece(color=RED, is_king=False)
        
        # Place white pieces (bottom rows)
        for row, col in [(5, 0), (5, 2), (5, 4), (5, 6),
                         (6, 1), (6, 3), (6, 5), (6, 7),
                         (7, 0), (7, 2), (7, 4), (7, 6)]:
            board[row][col] = Piece(color=WHITE, is_king=False)
        
        return board
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    
    def get_piece(self, row: int, col: int) -> Piece | None:
        """Get piece at position."""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def get_valid_moves(self, player: str, row: int, col: int) -> list[Move]:
        """Get all valid moves for a piece."""
        piece = self.get_piece(row, col)
        if piece is None or piece.color != player:
            return []
        
        moves = []
        
        # Determine valid directions based on piece type
        directions = []
        # RED pieces are at top (rows 0-2) and move down (+1)
        # WHITE pieces are at bottom (rows 5-7) and move up (-1)
        if piece.color == RED or piece.is_king:
            directions.append((1, -1))   # Down-left
            directions.append((1, 1))    # Down-right
        if piece.color == WHITE or piece.is_king:
            directions.append((-1, -1))  # Up-left
            directions.append((-1, 1))   # Up-right
        
        for dr, dc in directions:
            # Check simple move
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col) and self.board[new_row][new_col] is EMPTY:
                moves.append(Move(start=(row, col), end=(new_row, new_col)))
            
            # Check capture move
            jump_row, jump_col = row + 2 * dr, col + 2 * dc
            if self.is_valid_position(jump_row, jump_col):
                mid_row, mid_col = row + dr, col + dc
                mid_piece = self.get_piece(mid_row, mid_col)
                if (mid_piece is not None and 
                    mid_piece.color != player and 
                    self.board[jump_row][jump_col] is EMPTY):
                    moves.append(Move(
                        start=(row, col),
                        end=(jump_row, jump_col),
                        is_capture=True,
                        captured_square=(mid_row, mid_col)
                    ))
        
        return moves
    
    def get_all_valid_moves(self, player: str) -> list[Move]:
        """Get all valid moves for a player."""
        all_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == player:
                    all_moves.extend(self.get_valid_moves(player, row, col))
        return all_moves
    
    def apply_move(self, move: Move) -> bool:
        """Apply a move to the board. Returns True if move was valid."""
        piece = self.get_piece(move.start[0], move.start[1])
        
        # Validate move exists
        valid_moves = self.get_valid_moves(self.current_player, move.start[0], move.start[1])
        if move not in valid_moves:
            return False
        
        # Move the piece
        self.board[move.end[0]][move.end[1]] = piece
        self.board[move.start[0]][move.start[1]] = EMPTY
        
        # Handle capture
        if move.is_capture and move.captured_square is not None:
            self.board[move.captured_square[0]][move.captured_square[1]] = EMPTY
            if self.current_player == RED:
                self.white_pieces_remaining -= 1
            else:
                self.red_pieces_remaining -= 1
        
        # Handle kinging
        if piece.color == RED and move.end[0] == 0:
            self.board[move.end[0]][move.end[1]] = Piece(color=RED, is_king=True)
        elif piece.color == WHITE and move.end[0] == BOARD_SIZE - 1:
            self.board[move.end[0]][move.end[1]] = Piece(color=WHITE, is_king=True)
        
        # Switch turns
        self.current_player = WHITE if self.current_player == RED else RED
        
        return True
    
    def check_winner(self) -> str | None:
        """Check if there's a winner. Returns winning color or None."""
        if self.red_pieces_remaining == 0:
            return WHITE
        if self.white_pieces_remaining == 0:
            return RED
        
        red_moves = self.get_all_valid_moves(RED)
        white_moves = self.get_all_valid_moves(WHITE)
        
        if self.current_player == RED and len(red_moves) == 0:
            return WHITE
        if self.current_player == WHITE and len(white_moves) == 0:
            return RED
        
        return None
