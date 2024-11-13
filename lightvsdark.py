import chess
import chess.pgn
import random

sicilian_defense = ["e4", "c5", "Nf3", "d6"]

def is_light_square(square):
    """Check if a square is light-colored."""
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    return (rank + file) % 2 == 0

def encode_with_square_colors(message):
    game = chess.pgn.Game()
    node = game
    board = chess.Board()

    for open_move in sicilian_defense:
        move = board.parse_san(open_move)  # Parse the move in SAN notation
        board.push(move)                  # Make the move on the board
        node = node.add_variation(move)   # Add the move to the PGN

    binary_message = ''.join(format(ord(char), '08b') for char in message)

    for bit in binary_message:
        # Filter legal moves based on the current bit
        if bit == "1":
            # Collect moves that land on light squares
            moves = [m for m in board.legal_moves if is_light_square(m.to_square)]
        else:
            # Collect moves that land on dark squares
            moves = [m for m in board.legal_moves if not is_light_square(m.to_square)]
        
        if not moves:
            raise ValueError(f"No legal moves available for encoding bit '{bit}'")

        # Choose a random move from the filtered list
        move = random.choice(moves)
        
        # Push the selected move to the board and add it to the PGN
        board.push(move)
        node = node.add_variation(move)

    return game