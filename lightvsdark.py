import chess
import chess.pgn

def is_light_square(square):
    """Check if a square is light-colored."""
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    return (rank + file) % 2 == 0

def encode_with_square_colors(message):
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    # Convert the message into binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    for bit in binary_message:
        legal_moves = list(board.legal_moves)
        if bit == "1":
            # Find the first move to a light square
            move = next((m for m in legal_moves if is_light_square(m.to_square)), None)
        else:
            # Find the first move to a dark square
            move = next((m for m in legal_moves if not is_light_square(m.to_square)), None)
        
        if move is None:
            raise ValueError(f"No legal moves available for encoding bit '{bit}'")

        # Push the selected move to the board and add it to the PGN
        board.push(move)
        node = node.add_variation(move)

    return game

#if __name__ == "__main__":
    # Example: Convert the message into binary (e.g., "1010")
   # secret_message = "1010"
    
   # board = chess.Board()
    #game = encode_with_square_colors(board, secret_message)
    #print(game)