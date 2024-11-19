import binary_encoding
import chess.pgn
import lightvsdark
import moveToASCII
import pieces

OPENINGS = {
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"], 
    "Sicilian Defense": ["e4", "c5", "Nf3", "d6"], # light vs dark binary
    "French Defense": ["e4", "e6", "d4", "d5"], # comment binary
    "Queen's Gambit": ["d4", "d5", "c4"], # move based ASCII
    #"King's Indian Defense": ["d4", "Nf6", "c4", "g6"],
}

def detect_opening(moves):
    """
    Check if the list of moves matches any known opening.
    """
    for opening_name, opening_moves in OPENINGS.items():
        if moves[:len(opening_moves)] == opening_moves:
            return opening_name
    return None

def perform_action(opening_name, game):
    """
    Perform an action if a specific opening is detected.
    """
    message = ""
    print(f"Detected opening: {opening_name}")
    if opening_name == "French Defense":
        message = binary_encoding.comment_decode(game)
    elif opening_name == "Sicilian Defense":
        message = lightvsdark.decode(game)
    elif opening_name == "Queen's Gambit":
        message = moveToASCII.decode_game_to_message(game)
    elif opening_name == "Ruy Lopez":
        message = pieces.decode_with_piece_type_mapping(game)
    # Add your custom action here. For example:
    # Run a function, log information, or analyze the game further.
    # This is a placeholder for whatever action you want to perform.
    return message

def check_pgn_for_openings(pgn_file_path):
    """
    Check each game in the PGN file for specific openings.
    """
    message = ""
    with open(pgn_file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # End of file reached

            # Collect the first few moves to check for an opening
            moves = []
            node = game
            while not node.is_end() and len(moves) < 5:
                next_node = node.variation(0)
                moves.append(node.board().san(next_node.move))
                node = next_node

            # Detect if the moves match any known opening
            opening_name = detect_opening(moves)
            if opening_name:
                message = perform_action(opening_name, pgn_file_path)
    return message

if __name__ == "__main__":
    filename = input("Please enter the name of the file (ex test.pgn): ")
    # add check here for specific openings in order to call specific decode functions
    message = check_pgn_for_openings(filename)
    print("Decoded Message: " + message)