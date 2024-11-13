import chess
import chess.pgn
import random

# Define possible comments
one_comment = [
    "Check this out!",
    "ha!",
]

zero_comment = [
    "Nothing special here",
    "boring...",
]

# Opening
french_defense = ["e4", "e6", "d4", "d5"]

def comment_encode(message):
    # Convert the message into binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    for open_move in french_defense:
        move = board.parse_san(open_move)  # Parse the move in SAN notation
        board.push(move)                  # Make the move on the board
        node = node.add_variation(move)   # Add the move to the PGN

    for bit in binary_message:
        # Make a random legal move
        move = random.choice(list(board.legal_moves))
        board.push(move)
        node = node.add_variation(move)
        
        # Encode the bit as a comment
        if bit == "1":
            node.comment = random.choice(list(one_comment))
        else:
            node.comment = random.choice(list(zero_comment))

    return game

def comment_decode(filename):
    binary = ""

    # Open the PGN file and parse each game
    with open(filename, "r") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # End of file

            # Traverse through each move in the game
            node = game
            while node.variations:
                node = node.variation(0)  # Move to the next node
                if node.comment:
                    if node.comment in one_comment:
                        binary = binary + "1"
                    elif node.comment in zero_comment:
                        binary = binary + "0"

    message = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

    return message


# Example usage
#board = chess.Board()
#secret_message = "Hi"
#game = encode_message_in_pgn(board, secret_message)
#print(game)