import chess
import chess.pgn

# Constants
ASCII_MIN = 32  # Space (' ')
ASCII_MAX = 126  # Tilde ('~')
BOARD_SIZE = 64  # Number of squares on a chessboard
QUEENS_GAMBIT_LENGTH = 3  # Number of moves in the Queen's Gambit opening

#opening
queens_gambit = ["d4", "d5", "c4"]

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
        # Convert lowercase letters to uppercase
        char = char.upper()


        # Get the ASCII value of the character
        ascii_val = ord(char)

        # Ensure the character is within the printable range
        if ASCII_MIN <= ascii_val <= ASCII_MAX:
            adjusted_ascii = ascii_val - ASCII_MIN
            attempt = 0  # Start with attempt = 0

            while True:
                # Map the adjusted ASCII value to a square index
                square_index = (adjusted_ascii + attempt) % BOARD_SIZE

                # Get the target square
                target_square = square_index

                # Try to find a legal move to the target square
                legal_move_found = False
                for move in board.legal_moves:
                    if move.to_square == target_square:
                        board.push(move)
                        node = node.add_variation(move)
                        # Store the attempt offset in the comment
                        node.comment = str(attempt)
                        legal_move_found = True
                        break

                if legal_move_found:
                    break  # Move encoded successfully
                else:
                    attempt += 1  # Try next attempt

        else:
            print(f"Warning: Character '{char}' is out of the printable ASCII range.")

    return game


def decode_game_to_message(pgn_file_path):
    """
    Decodes a PGN game file into a message by analyzing the target squares of the moves.
    Skips the initial Queen's Gambit moves and processes the rest directly.
    """
    # Open the PGN file and parse the game
    with open(pgn_file_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)

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
        # Extract the target square
        target_square = move.to_square
        square_index = target_square

        # Reconstruct the adjusted ASCII value
        adjusted_ascii = (square_index - attempt) % BOARD_SIZE

        # Reconstruct the original ASCII value
        ascii_val = adjusted_ascii + ASCII_MIN

        # Append the character to the message
        if ASCII_MIN <= ascii_val <= ASCII_MAX:
            message += chr(ascii_val)
        else:
            message += "?"  # Placeholder for invalid characters

    return message

# Test Case
#game = encode_message_to_game("Hello World")
#print(game)
#message = decode_game_to_message(game)
#print(message)