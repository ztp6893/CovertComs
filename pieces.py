import chess
import chess.pgn
import random

#opening
ruy_lopez = ["e4", "e5", "Nf3", "Nc6", "Bb5"]

def encode_with_piece_type_mapping(message):
    """
    Encode a message using moves in a chess game where specific pieces represent binary 1 or 0.
    """
    game = chess.pgn.Game()
    node = game
    board = chess.Board()

    for open_move in ruy_lopez:
        move = board.parse_san(open_move)  # Parse the move in SAN notation
        board.push(move)                   # Make the move on the board
        node = node.add_variation(move)    # Add the move to the PGN

    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    i = 0
    while i < len(binary_message):
        bit = binary_message[i]
        
        # Select piece type based on the current bit
        if bit == "1":
            # Pieces representing '1': Pawn, Rook, Bishop
            pieces_for_1 = {chess.PAWN, chess.ROOK, chess.BISHOP}
            moves = [m for m in board.legal_moves if board.piece_type_at(m.from_square) in pieces_for_1]
        else:
            # Pieces representing '0': Knight, Queen, King
            pieces_for_0 = {chess.KNIGHT, chess.QUEEN, chess.KING}
            moves = [m for m in board.legal_moves if board.piece_type_at(m.from_square) in pieces_for_0]
        
        # If no moves available for the current bit, raise an error
        if not moves:
            raise ValueError(f"No legal moves available for encoding bit '{bit}'")

        # Choose a random move from the filtered list
        move = random.choice(moves)
        board.push(move)
        node = node.add_variation(move)
        i += 1  # Move to the next bit

    return game

def decode_with_piece_type_mapping(pgn_file_path):
    """
    Decode the message from a chess game by reading moves based on piece type.
    """

    # Open the PGN file and parse the game
    with open(pgn_file_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    binary_message = ""
    board = chess.Board()
    move_number = 0

    for move in game.mainline_moves():
        if move_number < 5:
            move_number += 1
            board.push(move)
            continue
        piece_type = board.piece_type_at(move.from_square)
        
        # Pieces representing '1': Pawn, Rook, Bishop
        if piece_type in {chess.PAWN, chess.ROOK, chess.BISHOP}:
            binary_message += "1"
        # Pieces representing '0': Knight, Queen, King
        elif piece_type in {chess.KNIGHT, chess.QUEEN, chess.KING}:
            binary_message += "0"
        
        board.push(move)

    # Split binary into 8-bit chunks and decode to characters
    chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chars)

    return decoded_message

# Test Case
#if __name__ == "__main__":
#    # Encode a message
#    message = "Hello Test"
#    game = encode_with_piece_type_mapping(message)
#    print("Encoded Game in PGN format:")
#    print(game)
#
#    # Decode the message
#    decoded_message = decode_with_piece_type_mapping(game)
#    print("\nDecoded Message:")
#    print(decoded_message)