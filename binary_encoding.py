import chess
import chess.pgn

def encode_message_in_pgn(board, message):
    # Convert the message into binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    game = chess.pgn.Game()
    node = game
    for bit in binary_message:
        # Make a random legal move
        move = list(board.legal_moves)[0]
        board.push(move)
        node = node.add_variation(move)
        
        # Encode the bit as a comment
        if bit == "1":
            node.comment = "Check this out!"  # Represents "1"
        else:
            node.comment = "Nothing special here."  # Represents "0"

    return game

# Example usage
board = chess.Board()
secret_message = "Hi"
game = encode_message_in_pgn(board, secret_message)
print(game)