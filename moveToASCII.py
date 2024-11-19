import chess
import chess.pgn

# Constants
ASCII_MIN = 32  # Space (' ')
ASCII_MAX = 126  # Tilde ('~')
BOARD_SIZE = 64  # Number of squares on a chessboard
QUEENS_GAMBIT_LENGTH = 3  # Number of moves in the Queen's Gambit opening

#opening
queens_gambit = ["d4", "d5", "c4"]

def map_ascii_to_square(ascii_val, attempt=0):
    """
    Maps an ASCII value to a chessboard square index using modular arithmetic.
    Adds the attempt to handle shifted mappings.
    """
    return (ascii_val - ASCII_MIN + attempt) % BOARD_SIZE


def encode_message_to_game(message):
    """
    Encodes a message into a PGN game by converting each character into legal chess moves.
    Ensures all characters are encoded by remapping unreachable targets.
    """
    
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    for open_move in queens_gambit:
        move = board.parse_san(open_move)  # Parse the move in SAN notation
        board.push(move)                  # Make the move on the board
        node = node.add_variation(move)   # Add the move to the PGN

    for char in message:
        # Get the ASCII value of the character
        ascii_val = ord(char)

        # Ensure the character is within the printable range
        if ASCII_MIN <= ascii_val <= ASCII_MAX:
            attempt = 0  # Start with the first mapping attempt
            while True:
                # Map the ASCII value to a square
                square_index = map_ascii_to_square(ascii_val, attempt)
                col = chess.square_file(square_index)  # Column (0-7)
                row = chess.square_rank(square_index)  # Row (0-7)

                # Try to find a legal move to this square
                target_square = chess.square(col, row)
                legal_move_found = False

                for move in board.legal_moves:
                    if move.to_square == target_square:
                        board.push(move)  # Update the board
                        node = node.add_variation(move)  # Add move to the PGN game
                        legal_move_found = True
                        break

                if legal_move_found:
                    # Store the attempt as a comment in the PGN
                    node.comment = str(attempt)
                    break  # Stop retrying once the move is encoded
                else:
                    attempt += 1  # Retry with a shifted mapping
        else:
            print(f"Warning: Character '{char}' is out of the printable ASCII range.")

    return game


def decode_game_to_message(game):
    """
    Decodes a PGN game file into a message by analyzing the target squares of the moves.
    Skips the initial Queen's Gambit moves and processes the rest directly.
    """
    # Open the PGN file and parse the game
    #with open(pgn_file_path, "r") as pgn_file:
    #    game = chess.pgn.read_game(pgn_file)

    # Extract all moves from the game
    moves = []
    comments = []
    node = game
    while node.variations:
        move = node.variations[0].move
        comment = node.variations[0].comment  # Retrieve the attempt comment
        moves.append((move, int(comment) if comment.isdigit() else 0))
        node = node.variations[0]

    # Skip the Queen's Gambit moves
    moves = moves[QUEENS_GAMBIT_LENGTH:]

    # Decode each move
    message = ""
    for move, attempt in moves:
        target_square = move.to_square
        square_index = chess.square_file(target_square) + (chess.square_rank(target_square) * 8)

        # Reverse the attempt offset to get the original ASCII value
        ascii_val = (square_index - attempt) % BOARD_SIZE + ASCII_MIN
        print(ascii_val)
        if ASCII_MIN <= ascii_val <= ASCII_MAX:  # Ensure it's within the printable range
            message += chr(ascii_val)
        else:
            message += "?"  # Placeholder for invalid characters

    return message

game = encode_message_to_game("Hello World")
print(game)
message = decode_game_to_message(game)
print(message)